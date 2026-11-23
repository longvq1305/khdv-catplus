"""
CatPlus Service Science Project (INT3501) - Group 20 (Strict Academic Version)
Integrated MILP Tutor-Student Matching Optimization (L5) with exact CatPlus
Class.clean() constraints (ONE_ON_ONE = 1, GROUP = 3..5) and Rolling-Batch
coupled with SimPy Human-in-the-Loop Process Queue Simulation (L4).
"""

import os
import json
import numpy as np
import simpy
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Segoe UI"]
plt.rcParams["axes.unicode_minus"] = False

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# 14 weekly teaching time slots (Mon-Fri 18:00 & 19:45, Sat-Sun morning/afternoon/evening)
SLOTS = [
    "T2_18h00", "T2_19h45",
    "T3_18h00", "T3_19h45",
    "T4_18h00", "T4_19h45",
    "T5_18h00", "T5_19h45",
    "T6_18h00", "T6_19h45",
    "T7_09h00", "T7_14h30",
    "CN_09h00", "CN_19h45",
]
SLOT_WEIGHTS = np.array([
    0.05, 0.08,
    0.05, 0.08,
    0.05, 0.08,
    0.05, 0.08,
    0.06, 0.09,
    0.10, 0.08,
    0.08, 0.07,
])
SLOT_WEIGHTS /= SLOT_WEIGHTS.sum()


def generate_cohort(rng, n_students=60, n_tutors=10, max_prefs=3):
    """
    Generate one monthly cohort (30 days) of student intake requests and tutors.
    Follows CatPlus academic_app/models.py:
      - education_level in {THCS, THPT}
      - class_type in {ONE_ON_ONE (cap=1), GROUP (quorum=3, cap=5)}
    """
    students = []
    for i in range(n_students):
        level = "THCS" if rng.random() < 0.55 else "THPT"
        mode = "ONE_ON_ONE" if rng.random() < 0.40 else "GROUP"
        r_flex = rng.random()
        if r_flex < 0.20:
            k_avail = 1
        elif r_flex < 0.65:
            k_avail = 2
        else:
            k_avail = 3
        all_slots = rng.choice(len(SLOTS), size=k_avail, replace=False, p=SLOT_WEIGHTS).tolist()
        k_used = min(k_avail, max_prefs)
        chosen_slots = all_slots[:k_used]
        prefs = {slot_idx: [100, 80, 60][rank] for rank, slot_idx in enumerate(chosen_slots)}
        students.append({
            "id": i,
            "arrival_day": float(rng.uniform(0, 30)),
            "level": level,
            "mode": mode,
            "prefs": prefs,
            "slot_order": chosen_slots,
            "all_slots": all_slots,
        })
    students.sort(key=lambda s: s["arrival_day"])
    for idx, s in enumerate(students):
        s["id"] = idx

    tutors = []
    for t in range(n_tutors):
        r_lvl = rng.random()
        if r_lvl < 0.50:
            levels = {"THCS", "THPT"}
        elif r_lvl < 0.80:
            levels = {"THCS"}
        else:
            levels = {"THPT"}
        n_free = int(rng.integers(5, 8))
        free_slots = rng.choice(len(SLOTS), size=n_free, replace=False, p=SLOT_WEIGHTS).tolist()
        tutors.append({
            "id": t,
            "levels": levels,
            "free_slots": free_slots,
            "max_classes": int(rng.integers(3, 6)),
        })

    return students, tutors


def solve_as_is_greedy(students, tutors):
    """
    AS-IS Manual Sequential (FCFS) Process:
    1) CSKH initially asks for 1 preferred slot (slot_order[0]).
    2) Manager tries to match sequentially:
       - For ONE_ON_ONE: assigns the first available compatible tutor.
       - For GROUP: joins an existing GROUP class of same (level, slot) with < 5 students,
         or reserves a tentative DRAFT group class with a free tutor.
    3) If Slot 1 fails, CSKH contacts parent again (Rework round 2) to ask for Slot 2
       (if the student has a 2nd slot).
    4) At the end of the enrollment window, any tentative DRAFT group class that failed
       to reach the minimum quorum of 3 students (per Class.clean(): 3 <= max_students <= 5)
       cannot open as a standalone group unless its students can be shifted in a 2nd-chance
       manual check to another open group; otherwise those students drop out as
       CLOSED_LOST (CENTER_CANNOT_SERVE / SCHEDULE_MISMATCH).
    """
    tutor_slot_used = set()
    tutor_class_count = {t["id"]: 0 for t in tutors}
    # list of group classes: {tutor_id, slot, level, students: [ (student_dict, fit_score, rounds) ]}
    group_classes = []
    one_on_one_matches = []  # (student_dict, fit_score, rounds)
    unmatched_initial = []   # (student_dict, rounds)

    for s in students:
        assigned = False
        rounds_used = 0
        # AS-IS: up to 2 manual rounds
        candidate_slots = s["all_slots"][:2]
        for r_idx, slot in enumerate(candidate_slots):
            rounds_used = r_idx + 1
            if s["mode"] == "GROUP":
                # Check existing group class with < 5 students
                found_g = None
                for g in group_classes:
                    if g["slot"] == slot and g["level"] == s["level"] and len(g["students"]) < 5:
                        found_g = g
                        break
                if found_g is not None:
                    score = [100, 80, 60][r_idx]
                    found_g["students"].append((s, score, rounds_used))
                    assigned = True
                    break

                # Otherwise open a tentative DRAFT group class with first free tutor
                for t in tutors:
                    if s["level"] in t["levels"] and slot in t["free_slots"]:
                        if (t["id"], slot) not in tutor_slot_used and tutor_class_count[t["id"]] < t["max_classes"]:
                            tutor_slot_used.add((t["id"], slot))
                            tutor_class_count[t["id"]] += 1
                            score = [100, 80, 60][r_idx]
                            group_classes.append({
                                "tutor_id": t["id"],
                                "slot": slot,
                                "level": s["level"],
                                "students": [(s, score, rounds_used)],
                            })
                            assigned = True
                            break
                if assigned:
                    break
            else:
                # ONE_ON_ONE
                for t in tutors:
                    if s["level"] in t["levels"] and slot in t["free_slots"]:
                        if (t["id"], slot) not in tutor_slot_used and tutor_class_count[t["id"]] < t["max_classes"]:
                            tutor_slot_used.add((t["id"], slot))
                            tutor_class_count[t["id"]] += 1
                            score = [100, 80, 60][r_idx]
                            one_on_one_matches.append((s, score, rounds_used))
                            assigned = True
                            break
                if assigned:
                    break

        if not assigned:
            unmatched_initial.append((s, rounds_used))

    # Enforce Class.clean() quorum rule for GROUP classes: 3 <= size <= 5
    valid_groups = [g for g in group_classes if len(g["students"]) >= 3]
    under_quorum_groups = [g for g in group_classes if len(g["students"]) < 3]

    # Manual rescue attempt: Manager tries to move students from under-quorum groups
    # into valid_groups if they share a 2nd preferred slot with space < 5
    rescued_matches = []
    failed_quorum_students = []
    for g in under_quorum_groups:
        for (s, orig_score, r_used) in g["students"]:
            rescued = False
            for alt_rank, alt_slot in enumerate(s["all_slots"][:2]):
                for vg in valid_groups:
                    if vg["slot"] == alt_slot and vg["level"] == s["level"] and len(vg["students"]) < 5:
                        vg["students"].append((s, [100, 80, 60][alt_rank], r_used + 1))
                        rescued = True
                        break
                if rescued:
                    break
            if not rescued:
                failed_quorum_students.append((s, r_used + 1))

    # Compile final AS-IS outcomes
    student_outcomes = {}
    fit_scores_matched = []
    closed_lost_reasons = {"SCHEDULE_MISMATCH": 0, "CENTER_CANNOT_SERVE": 0}

    for (s, score, r_used) in one_on_one_matches:
        student_outcomes[s["id"]] = {"matched": True, "score": score, "rework_loops": r_used - 1}
        fit_scores_matched.append(score)

    for vg in valid_groups:
        for (s, score, r_used) in vg["students"]:
            student_outcomes[s["id"]] = {"matched": True, "score": score, "rework_loops": r_used - 1}
            fit_scores_matched.append(score)

    for (s, r_used) in unmatched_initial + failed_quorum_students:
        student_outcomes[s["id"]] = {"matched": False, "score": 0, "rework_loops": max(1, r_used - 1)}
        if len(s["all_slots"]) == 1:
            closed_lost_reasons["SCHEDULE_MISMATCH"] += 1
        else:
            closed_lost_reasons["CENTER_CANNOT_SERVE"] += 1

    matched_count = len(fit_scores_matched)
    total_fit_all = sum(fit_scores_matched) / len(students)
    return {
        "n_students": len(students),
        "matched": matched_count,
        "match_rate": matched_count / len(students) * 100.0,
        "avg_fit_matched": float(np.mean(fit_scores_matched)) if fit_scores_matched else 0.0,
        "avg_fit_all": float(total_fit_all),
        "closed_lost": closed_lost_reasons,
        "student_outcomes": student_outcomes,
        "active_group_classes": len(valid_groups),
        "active_1on1_classes": len(one_on_one_matches),
    }


def solve_to_be_milp(students, tutors, penalty_unmatched=1000.0, fit_weight=1.0, class_cost=0.05, min_group_size=3, max_group_size=5):
    """
    TO-BE Global / Batch MILP Model (Slide L5):
    Enforces exact CatPlus Class.clean() constraints:
      - ONE_ON_ONE class capacity: exactly 1 student
      - GROUP class capacity: between min_group_size (3) and max_group_size (5) students!
        3 * y_{k, lvl, GROUP} <= sum_{i} x_{i,k} <= 5 * y_{k, lvl, GROUP}
      - Virtual class variable u_i in {0, 1} with penalty P (Slide L5 P8)
    """
    n_s = len(students)
    ts_pairs = []
    for t in tutors:
        for slot in t["free_slots"]:
            ts_pairs.append((t["id"], slot, t["levels"]))

    configs = [
        ("THCS", "ONE_ON_ONE", 1, 1),
        ("THPT", "ONE_ON_ONE", 1, 1),
        ("THCS", "GROUP", min_group_size, max_group_size),
        ("THPT", "GROUP", min_group_size, max_group_size),
    ]

    x_vars = []
    x_index = {}
    for i, s in enumerate(students):
        for k, (tid, slot, t_levels) in enumerate(ts_pairs):
            if slot in s["prefs"] and s["level"] in t_levels:
                idx = len(x_vars)
                x_vars.append((i, k, slot, s["level"], s["mode"], s["prefs"][slot]))
                x_index[(i, k)] = idx

    n_x = len(x_vars)
    u_offset = n_x
    n_u = n_s

    y_vars = []
    y_index = {}
    y_offset = u_offset + n_u
    for k, (tid, slot, t_levels) in enumerate(ts_pairs):
        for (lvl, mode, l_cap, u_cap) in configs:
            if lvl in t_levels:
                idx = y_offset + len(y_vars)
                y_vars.append((k, tid, slot, lvl, mode, l_cap, u_cap))
                y_index[(k, lvl, mode)] = idx

    total_vars = y_offset + len(y_vars)

    c_obj = np.zeros(total_vars)
    for idx, (_, _, _, _, _, fit) in enumerate(x_vars):
        c_obj[idx] = -float(fit_weight * fit)
    for i in range(n_s):
        c_obj[u_offset + i] = float(penalty_unmatched)
    for idx_rel in range(len(y_vars)):
        c_obj[y_offset + idx_rel] = float(class_cost)  # cost of opening a tutor class slot

    rows, cols, vals, lbs, ubs = [], [], [], [], []
    row_idx = 0

    # 1) Each student i assigned to at most 1 tutor-slot OR u_i = 1
    for i in range(n_s):
        for k in range(len(ts_pairs)):
            if (i, k) in x_index:
                rows.append(row_idx)
                cols.append(x_index[(i, k)])
                vals.append(1.0)
        rows.append(row_idx)
        cols.append(u_offset + i)
        vals.append(1.0)
        lbs.append(1.0)
        ubs.append(1.0)
        row_idx += 1

    # 2) Each tutor-slot k opens at most 1 class configuration
    for k in range(len(ts_pairs)):
        cfg_indices = [y_index[(k, lvl, mode)] for (lvl, mode, _, _) in configs if (k, lvl, mode) in y_index]
        if cfg_indices:
            for yi in cfg_indices:
                rows.append(row_idx)
                cols.append(yi)
                vals.append(1.0)
            lbs.append(0.0)
            ubs.append(1.0)
            row_idx += 1

    # 3) Upper & Lower capacity bounds per (k, lvl, mode):
    #    l_cap * y <= sum x <= u_cap * y
    #    -> Upper: sum x - u_cap * y <= 0
    #    -> Lower: sum x - l_cap * y >= 0
    for (k, tid, slot, lvl, mode, l_cap, u_cap) in y_vars:
        yi = y_index[(k, lvl, mode)]
        compat_x = [
            x_index[(i, k)]
            for i, s in enumerate(students)
            if (i, k) in x_index and s["level"] == lvl and s["mode"] == mode
        ]
        if compat_x:
            # Upper bound: sum x - u_cap * y <= 0
            for xi in compat_x:
                rows.append(row_idx)
                cols.append(xi)
                vals.append(1.0)
            rows.append(row_idx)
            cols.append(yi)
            vals.append(-float(u_cap))
            lbs.append(-np.inf)
            ubs.append(0.0)
            row_idx += 1

            # Lower bound (quorum): sum x - l_cap * y >= 0
            if l_cap > 1:
                for xi in compat_x:
                    rows.append(row_idx)
                    cols.append(xi)
                    vals.append(1.0)
                rows.append(row_idx)
                cols.append(yi)
                vals.append(-float(l_cap))
                lbs.append(0.0)
                ubs.append(np.inf)
                row_idx += 1
        else:
            # Cannot open this config if 0 compatible students
            rows.append(row_idx)
            cols.append(yi)
            vals.append(1.0)
            lbs.append(0.0)
            ubs.append(0.0)
            row_idx += 1

    # 4) Tutor max classes: sum_{k in tutor t, cfg} y_{k,cfg} <= max_classes[t]
    for t in tutors:
        tid = t["id"]
        t_y = [yi for (k, lvl, mode), yi in y_index.items() if ts_pairs[k][0] == tid]
        if t_y:
            for yi in t_y:
                rows.append(row_idx)
                cols.append(yi)
                vals.append(1.0)
            lbs.append(0.0)
            ubs.append(float(t["max_classes"]))
            row_idx += 1

    A = coo_matrix((vals, (rows, cols)), shape=(row_idx, total_vars)).tocsc()
    constraints = LinearConstraint(A, lbs, ubs)
    integrality = np.ones(total_vars)
    bounds = Bounds(np.zeros(total_vars), np.ones(total_vars))

    res = milp(
        c=c_obj,
        integrality=integrality,
        bounds=bounds,
        constraints=constraints,
        options={"time_limit": 2.5, "mip_rel_gap": 0.005},
    )
    if res.x is None:
        raise RuntimeError(f"MILP failed: {res.message}")

    sol = np.round(res.x).astype(int)
    matched = 0
    fit_scores = []
    student_outcomes = {}
    for i, s in enumerate(students):
        if sol[u_offset + i] == 0:
            matched += 1
            sc = 100
            for k in range(len(ts_pairs)):
                if (i, k) in x_index and sol[x_index[(i, k)]] == 1:
                    sc = x_vars[x_index[(i, k)]][5]
                    break
            fit_scores.append(sc)
            student_outcomes[s["id"]] = {"matched": True, "score": sc, "rework_loops": 0}
        else:
            student_outcomes[s["id"]] = {"matched": False, "score": 0, "rework_loops": 0}

    classes_opened = int(np.sum(sol[y_offset:]))
    return {
        "n_students": n_s,
        "matched": matched,
        "match_rate": matched / n_s * 100.0,
        "avg_fit_matched": float(np.mean(fit_scores)) if fit_scores else 0.0,
        "avg_fit_all": float(sum(fit_scores) / n_s),
        "unmatched": n_s - matched,
        "classes_opened": classes_opened,
        "student_outcomes": student_outcomes,
    }


def simulate_coupled_queue(rng, students, outcomes, mode="AS_IS", n_cskh=2, n_managers=1):
    """
    SimPy Discrete-Event Simulation (L4) directly coupled with the matching outcomes!
    Tracks:
      - Resource Queue Waiting Time (W_q_resource: waiting for CSKH/Manager availability)
      - Stage Durations (CSKH intake, Matching & Tutor Confirmation, Trial Class Setup)
      - End-to-End Cycle Time / Lead Time (W_total)
      - Resource utilization (rho_cskh, rho_manager) and Little's Law verification (L = lambda * W)
      - SLA compliance (% completed within 16 working hours = 2 working days)
    """
    env = simpy.Environment()
    cskh_res = simpy.Resource(env, capacity=n_cskh)
    mgr_res = simpy.Resource(env, capacity=n_managers)

    total_cycle_hrs = []
    pure_resource_queue_hrs = []
    stage_waits = {"cskh": [], "matching": [], "trial": []}
    cskh_busy_time = [0.0]
    mgr_busy_time = [0.0]

    def student_process(s):
        arrival_hr = s["arrival_day"] * 8.0
        yield env.timeout(arrival_hr)
        t_enter = env.now
        res_q_wait = 0.0
        out = outcomes[s["id"]]

        # Stage 1: CHUA_LIEN_HE -> CSKH intake & parent consultation
        t_s1 = env.now
        t_req = env.now
        with cskh_res.request() as req:
            yield req
            res_q_wait += (env.now - t_req)
            svc_t = float(rng.uniform(0.45, 1.15)) if mode == "AS_IS" else float(rng.uniform(0.55, 1.25))
            cskh_busy_time[0] += svc_t
            yield env.timeout(svc_t)

        # Parent callback delay if unreachable on first try
        if rng.random() < (0.30 if mode == "AS_IS" else 0.20):
            yield env.timeout(float(rng.uniform(2.0, 5.5)))
        stage_waits["cskh"].append(env.now - t_s1)

        # Stage 2: CHO_LOP -> Matching & Tutor Confirmation (coupled with actual rework_loops!)
        t_s2 = env.now
        if mode == "AS_IS":
            loops = 1 + int(out["rework_loops"])
            for l_idx in range(loops):
                t_req = env.now
                with mgr_res.request() as req:
                    yield req
                    res_q_wait += (env.now - t_req)
                    svc_m = float(rng.uniform(0.85, 1.75))
                    mgr_busy_time[0] += svc_m
                    yield env.timeout(svc_m)
                # Asynchronous wait for tutor reply on Zalo/phone
                yield env.timeout(float(rng.uniform(2.5, 7.5)))

                if l_idx < loops - 1:
                    # Rework handoff back to CSKH to re-negotiate slot with parent
                    t_req = env.now
                    with cskh_res.request() as req:
                        yield req
                        res_q_wait += (env.now - t_req)
                        svc_re = float(rng.uniform(0.35, 0.75))
                        cskh_busy_time[0] += svc_re
                        yield env.timeout(svc_re)
                    # Wait for parent to discuss with student & reply
                    yield env.timeout(float(rng.uniform(2.5, 6.5)))

            # If GROUP mode in AS-IS, waiting for group quorum (3..5 students) adds buffer
            if s["mode"] == "GROUP":
                yield env.timeout(float(rng.uniform(2.0, 6.0)))
        else:
            # TO-BE: Rolling batch window wait (1.0 - 3.5 working hrs) + MILP instant solve
            yield env.timeout(float(rng.uniform(1.0, 3.5)))
            t_req = env.now
            with mgr_res.request() as req:
                yield req
                res_q_wait += (env.now - t_req)
                svc_m = float(rng.uniform(0.20, 0.45))
                mgr_busy_time[0] += svc_m
                yield env.timeout(svc_m)
            # Pre-filtered tutor 1-tap confirmation
            yield env.timeout(float(rng.uniform(1.0, 3.5)))
            # 8% rare sudden tutor conflict -> fallback to 2nd MILP suggestion
            if rng.random() < 0.08:
                t_req = env.now
                with mgr_res.request() as req:
                    yield req
                    res_q_wait += (env.now - t_req)
                    svc_m2 = float(rng.uniform(0.15, 0.35))
                    mgr_busy_time[0] += svc_m2
                    yield env.timeout(svc_m2)
                yield env.timeout(float(rng.uniform(1.0, 2.5)))

        stage_waits["matching"].append(env.now - t_s2)

        # Stage 3: CHO_HOC_THU -> Trial Session & Enrollment Confirmation
        t_s3 = env.now
        if out["matched"]:
            if mode == "AS_IS":
                yield env.timeout(float(rng.uniform(4.0, 10.0)))
            else:
                yield env.timeout(float(rng.uniform(2.0, 5.5)))
        else:
            # Unmatched students receive final CLOSED_LOST notification after search exhausts
            yield env.timeout(float(rng.uniform(1.0, 3.0)))
        stage_waits["trial"].append(env.now - t_s3)

        total_cycle_hrs.append(env.now - t_enter)
        pure_resource_queue_hrs.append(res_q_wait)

    for s in students:
        env.process(student_process(s))
    env.run()

    arr = np.array(total_cycle_hrs)
    horizon_hrs = 30.0 * 8.0  # 240 working hours/month
    lambda_hr = len(students) / horizon_hrs
    mean_w = float(np.mean(arr))
    little_L = lambda_hr * mean_w  # Average number of active student cases in pipeline (WIP)

    return {
        "mean_wait_hrs": mean_w,
        "p90_wait_hrs": float(np.percentile(arr, 90)),
        "mean_wait_days": mean_w / 8.0,
        "p90_wait_days": float(np.percentile(arr, 90)) / 8.0,
        "pure_res_queue_hrs": float(np.mean(pure_resource_queue_hrs)),
        "sla_16h_rate": float(np.mean(arr <= 16.0) * 100.0),  # % completed within 2 working days (16h)
        "cskh_stage_hrs": float(np.mean(stage_waits["cskh"])),
        "matching_stage_hrs": float(np.mean(stage_waits["matching"])),
        "trial_stage_hrs": float(np.mean(stage_waits["trial"])),
        "rho_cskh": float(cskh_busy_time[0] / (horizon_hrs * n_cskh) * 100.0),
        "rho_mgr": float(mgr_busy_time[0] / (horizon_hrs * n_managers) * 100.0),
        "little_L_wip": float(little_L),
    }


def run_experiment(n_reps=20, n_students=60, n_tutors=10, max_prefs=3, seed=42):
    rng = np.random.default_rng(seed)
    as_is_match, to_be_match = [], []
    as_is_fit_m, to_be_fit_m = [], []
    as_is_fit_all, to_be_fit_all = [], []
    as_is_wait, to_be_wait = [], []
    as_is_p90, to_be_p90 = [], []
    as_is_sla, to_be_sla = [], []
    as_is_rho_mgr, to_be_rho_mgr = [], []
    as_is_rho_cskh, to_be_rho_cskh = [], []
    as_is_wip, to_be_wip = [], []
    as_is_stages, to_be_stages = [], []
    closed_lost_totals = {"SCHEDULE_MISMATCH": 0, "CENTER_CANNOT_SERVE": 0}

    for _ in range(n_reps):
        students, tutors = generate_cohort(rng, n_students=n_students, n_tutors=n_tutors, max_prefs=max_prefs)
        res_as = solve_as_is_greedy(students, tutors)
        res_to = solve_to_be_milp(students, tutors)

        q_as = simulate_coupled_queue(rng, students, res_as["student_outcomes"], mode="AS_IS")
        q_to = simulate_coupled_queue(rng, students, res_to["student_outcomes"], mode="TO_BE")

        as_is_match.append(res_as["match_rate"])
        to_be_match.append(res_to["match_rate"])
        as_is_fit_m.append(res_as["avg_fit_matched"])
        to_be_fit_m.append(res_to["avg_fit_matched"])
        as_is_fit_all.append(res_as["avg_fit_all"])
        to_be_fit_all.append(res_to["avg_fit_all"])
        as_is_wait.append(q_as["mean_wait_hrs"])
        to_be_wait.append(q_to["mean_wait_hrs"])
        as_is_p90.append(q_as["p90_wait_hrs"])
        to_be_p90.append(q_to["p90_wait_hrs"])
        as_is_sla.append(q_as["sla_16h_rate"])
        to_be_sla.append(q_to["sla_16h_rate"])
        as_is_rho_mgr.append(q_as["rho_mgr"])
        to_be_rho_mgr.append(q_to["rho_mgr"])
        as_is_rho_cskh.append(q_as["rho_cskh"])
        to_be_rho_cskh.append(q_to["rho_cskh"])
        as_is_wip.append(q_as["little_L_wip"])
        to_be_wip.append(q_to["little_L_wip"])
        as_is_stages.append((q_as["cskh_stage_hrs"], q_as["matching_stage_hrs"], q_as["trial_stage_hrs"]))
        to_be_stages.append((q_to["cskh_stage_hrs"], q_to["matching_stage_hrs"], q_to["trial_stage_hrs"]))
        closed_lost_totals["SCHEDULE_MISMATCH"] += res_as["closed_lost"]["SCHEDULE_MISMATCH"]
        closed_lost_totals["CENTER_CANNOT_SERVE"] += res_as["closed_lost"]["CENTER_CANNOT_SERVE"]

    return {
        "n_reps": n_reps,
        "n_students": n_students,
        "n_tutors": n_tutors,
        "as_is": {
            "match_rate_mean": float(np.mean(as_is_match)),
            "match_rate_std": float(np.std(as_is_match)),
            "fit_matched_mean": float(np.mean(as_is_fit_m)),
            "fit_all_mean": float(np.mean(as_is_fit_all)),
            "wait_hrs_mean": float(np.mean(as_is_wait)),
            "wait_days_mean": float(np.mean(as_is_wait)) / 8.0,
            "p90_hrs_mean": float(np.mean(as_is_p90)),
            "p90_days_mean": float(np.mean(as_is_p90)) / 8.0,
            "sla_16h_mean": float(np.mean(as_is_sla)),
            "rho_mgr_mean": float(np.mean(as_is_rho_mgr)),
            "rho_cskh_mean": float(np.mean(as_is_rho_cskh)),
            "little_L_wip": float(np.mean(as_is_wip)),
            "stage_cskh_hrs": float(np.mean([x[0] for x in as_is_stages])),
            "stage_match_hrs": float(np.mean([x[1] for x in as_is_stages])),
            "stage_trial_hrs": float(np.mean([x[2] for x in as_is_stages])),
            "closed_lost_avg": {k: v / n_reps for k, v in closed_lost_totals.items()},
        },
        "to_be": {
            "match_rate_mean": float(np.mean(to_be_match)),
            "match_rate_std": float(np.std(to_be_match)),
            "fit_matched_mean": float(np.mean(to_be_fit_m)),
            "fit_all_mean": float(np.mean(to_be_fit_all)),
            "wait_hrs_mean": float(np.mean(to_be_wait)),
            "wait_days_mean": float(np.mean(to_be_wait)) / 8.0,
            "p90_hrs_mean": float(np.mean(to_be_p90)),
            "p90_days_mean": float(np.mean(to_be_p90)) / 8.0,
            "sla_16h_mean": float(np.mean(to_be_sla)),
            "rho_mgr_mean": float(np.mean(to_be_rho_mgr)),
            "rho_cskh_mean": float(np.mean(to_be_rho_cskh)),
            "little_L_wip": float(np.mean(to_be_wip)),
            "stage_cskh_hrs": float(np.mean([x[0] for x in to_be_stages])),
            "stage_match_hrs": float(np.mean([x[1] for x in to_be_stages])),
            "stage_trial_hrs": float(np.mean([x[2] for x in to_be_stages])),
        },
    }


def run_pareto_frontier(n_reps=12, n_students=60, n_tutors=10, seed=42):
    """
    Slide L5 P21-25: Multi-objective Pareto Frontier analysis:
    Conflicting objectives between Provider (Minimize opened tutor class slots / cost)
    and Beneficiary (Maximize Match Rate % and Overall Schedule Fit Score).
    Sweeps class opening cost weight gamma in {0.05, 180, 380, 650, 950}.
    """
    gammas = [10.0, 1065.0, 1085.0, 1105.0]
    pareto_pts = []
    for g_val in gammas:
        rng = np.random.default_rng(seed)
        mr_list, fit_all_list, cls_list = [], [], []
        for _ in range(n_reps):
            students, tutors = generate_cohort(rng, n_students=n_students, n_tutors=n_tutors, max_prefs=3)
            res = solve_to_be_milp(students, tutors, penalty_unmatched=1000.0, fit_weight=1.0, class_cost=g_val)
            mr_list.append(res["match_rate"])
            fit_all_list.append(res["avg_fit_all"])
            cls_list.append(res["classes_opened"])
        pareto_pts.append({
            "gamma_cost": g_val,
            "match_rate": float(np.mean(mr_list)),
            "fit_all": float(np.mean(fit_all_list)),
            "classes_opened": float(np.mean(cls_list)),
        })
    return pareto_pts


def main():
    print("Running strict coupled baseline simulation (20 replications, N=60, M=10)...", flush=True)
    base = run_experiment(n_reps=20, n_students=60, n_tutors=10, max_prefs=3, seed=42)

    demand_levels = [45, 60, 75, 90]
    sens_demand = []
    for n_s in demand_levels:
        r = run_experiment(n_reps=12, n_students=n_s, n_tutors=10, max_prefs=3, seed=100 + n_s)
        sens_demand.append((n_s, r))

    tutor_levels = [6, 8, 10, 12]
    sens_tutors = []
    for n_t in tutor_levels:
        r = run_experiment(n_reps=12, n_students=60, n_tutors=n_t, max_prefs=3, seed=200 + n_t)
        sens_tutors.append((n_t, r))

    pref_levels = [1, 2, 3]
    sens_prefs = []
    for mp in pref_levels:
        r = run_experiment(n_reps=12, n_students=60, n_tutors=10, max_prefs=mp, seed=300)
        sens_prefs.append((mp, r))

    pareto_pts = run_pareto_frontier(n_reps=12, n_students=60, n_tutors=10, seed=42)

    summary = {
        "baseline": base,
        "sensitivity_demand": [(n, r["as_is"], r["to_be"]) for n, r in sens_demand],
        "sensitivity_tutors": [(n, r["as_is"], r["to_be"]) for n, r in sens_tutors],
        "sensitivity_prefs": [(n, r["as_is"], r["to_be"]) for n, r in sens_prefs],
        "pareto_frontier": pareto_pts,
    }
    json_path = os.path.join(OUT_DIR, "simulation_results.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # --- Figure 1: Main KPI Comparison ---
    fig, axes = plt.subplots(1, 3, figsize=(13.8, 4.4), dpi=220)
    colors = ["#CBD5E1", "#2563EB"]

    vals1 = [base["as_is"]["match_rate_mean"], base["to_be"]["match_rate_mean"]]
    bars1 = axes[0].bar(["AS-IS\n(Xếp tay FCFS)", "TO-BE\n(ILP + Duyệt)"], vals1, color=colors, width=0.52, edgecolor="#1E293B")
    axes[0].set_ylim(0, 112)
    axes[0].set_ylabel("Tỷ lệ (%)")
    axes[0].set_title("KPI 1: Tỷ lệ ghép thành công (%)", fontweight="bold", fontsize=10.5)
    for b, v in zip(bars1, vals1):
        axes[0].text(b.get_x() + b.get_width()/2, v + 2.2, f"{v:.1f}%", ha="center", fontweight="bold")

    x2 = np.arange(2)
    w2 = 0.34
    f_m = [base["as_is"]["fit_matched_mean"], base["to_be"]["fit_matched_mean"]]
    f_a = [base["as_is"]["fit_all_mean"], base["to_be"]["fit_all_mean"]]
    bm1 = axes[1].bar(x2 - w2/2, f_m, width=w2, label="Trên tập ghép được", color="#94A3B8", edgecolor="#1E293B")
    bm2 = axes[1].bar(x2 + w2/2, f_a, width=w2, label="Toàn bộ HV đăng ký", color="#2563EB", edgecolor="#1E293B")
    axes[1].set_xticks(x2)
    axes[1].set_xticklabels(["AS-IS\n(Xếp tay FCFS)", "TO-BE\n(ILP + Duyệt)"])
    axes[1].set_ylim(0, 116)
    axes[1].set_ylabel("Điểm phù hợp (Thang 100)")
    axes[1].set_title("KPI 2: Độ phù hợp lịch trung bình", fontweight="bold", fontsize=10.5)
    axes[1].legend(frameon=False, fontsize=8.2, loc="upper left")
    for b, v in list(zip(bm1, f_m)) + list(zip(bm2, f_a)):
        axes[1].text(b.get_x() + b.get_width()/2, v + 1.8, f"{v:.1f}", ha="center", fontsize=8.5, fontweight="bold")

    x3 = np.arange(2)
    w3 = 0.34
    means = [base["as_is"]["wait_hrs_mean"], base["to_be"]["wait_hrs_mean"]]
    p90s = [base["as_is"]["p90_hrs_mean"], base["to_be"]["p90_hrs_mean"]]
    b_m = axes[2].bar(x3 - w3/2, means, width=w3, label="Trung bình (Mean)", color="#3B82F6", edgecolor="#1E293B")
    b_p = axes[2].bar(x3 + w3/2, p90s, width=w3, label="Phân vị P90", color="#F59E0B", edgecolor="#1E293B")
    axes[2].set_xticks(x3)
    axes[2].set_xticklabels(["AS-IS\n(Xếp tay FCFS)", "TO-BE\n(ILP + Duyệt)"])
    axes[2].set_ylabel("Giờ làm việc (8h = 1 ngày)")
    axes[2].set_title("KPI 3: Thời gian chờ học viên (Giờ)", fontweight="bold", fontsize=10.5)
    axes[2].set_ylim(0, max(p90s) * 1.24)
    axes[2].legend(frameon=False, fontsize=8.5)
    for b, v in list(zip(b_m, means)) + list(zip(b_p, p90s)):
        axes[2].text(b.get_x() + b.get_width()/2, v + 0.6, f"{v:.1f}h", ha="center", fontsize=8.5, fontweight="bold")

    fig.suptitle("So sánh hiệu năng AS-IS và TO-BE trên 3 chỉ số KPI (20 lần chạy, Ràng buộc Group 3–5 HV)", fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig1_as_is_vs_to_be_kpi.png"), bbox_inches="tight")
    plt.close()

    # --- Figure 2: Stage-by-Stage Waiting Time Breakdown ---
    fig, ax = plt.subplots(figsize=(8.4, 4.2), dpi=220)
    stages_lbl = ["1. CSKH tiếp nhận\n(CHUA_LIEN_HE)", "2. Dò lịch, Gom nhóm & Chốt GS\n(CHO_LOP / Rework)", "3. Chờ xếp học thử\n(CHO_HOC_THU)"]
    as_vals = [base["as_is"]["stage_cskh_hrs"], base["as_is"]["stage_match_hrs"], base["as_is"]["stage_trial_hrs"]]
    to_vals = [base["to_be"]["stage_cskh_hrs"], base["to_be"]["stage_match_hrs"], base["to_be"]["stage_trial_hrs"]]
    x = np.arange(len(stages_lbl))
    w = 0.35
    b1 = ax.bar(x - w/2, as_vals, width=w, label="AS-IS (Thủ công nhiều vòng)", color="#94A3B8", edgecolor="#1E293B")
    b2 = ax.bar(x + w/2, to_vals, width=w, label="TO-BE (Thu thập 3 slot + ILP gợi ý)", color="#2563EB", edgecolor="#1E293B")
    ax.set_xticks(x)
    ax.set_xticklabels(stages_lbl)
    ax.set_ylabel("Thời gian trung bình (giờ làm việc)")
    ax.set_title("Phân rã thời gian chu trình (Cycle Time) theo từng chặng trong StudentJourney", fontweight="bold")
    ax.set_ylim(0, max(as_vals) * 1.25)
    ax.legend(frameon=False)
    for b, v in list(zip(b1, as_vals)) + list(zip(b2, to_vals)):
        ax.text(b.get_x() + b.get_width()/2, v + 0.3, f"{v:.1f}h", ha="center", fontweight="bold", fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig2_waiting_time_breakdown.png"), bbox_inches="tight")
    plt.close()

    # --- Figure 3: Sensitivity Analysis ---
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.2), dpi=220)

    d_x = [x[0] for x in sens_demand]
    axes[0].plot(d_x, [x[1]["as_is"]["match_rate_mean"] for x in sens_demand], "o--", color="#64748B", label="AS-IS (Xếp tay)")
    axes[0].plot(d_x, [x[1]["to_be"]["match_rate_mean"] for x in sens_demand], "s-", color="#2563EB", label="TO-BE (ILP)")
    axes[0].set_title("Độ nhạy 1: Nhu cầu học viên tăng", fontweight="bold", fontsize=10)
    axes[0].set_xlabel("Số học viên / tháng")
    axes[0].set_ylabel("Tỷ lệ ghép thành công (%)")
    axes[0].set_ylim(40, 105)
    axes[0].grid(alpha=0.3)
    axes[0].legend(frameon=False)

    t_x = [x[0] for x in sens_tutors]
    axes[1].plot(t_x, [x[1]["as_is"]["match_rate_mean"] for x in sens_tutors], "o--", color="#64748B", label="AS-IS (Xếp tay)")
    axes[1].plot(t_x, [x[1]["to_be"]["match_rate_mean"] for x in sens_tutors], "s-", color="#2563EB", label="TO-BE (ILP)")
    axes[1].set_title("Độ nhạy 2: Biến động số lượng gia sư", fontweight="bold", fontsize=10)
    axes[1].set_xlabel("Số gia sư hoạt động")
    axes[1].set_ylabel("Tỷ lệ ghép thành công (%)")
    axes[1].set_ylim(40, 105)
    axes[1].grid(alpha=0.3)
    axes[1].legend(frameon=False)

    p_x = [x[0] for x in sens_prefs]
    axes[2].plot(p_x, [x[1]["as_is"]["match_rate_mean"] for x in sens_prefs], "o--", color="#64748B", label="AS-IS (Xếp tay)")
    axes[2].plot(p_x, [x[1]["to_be"]["match_rate_mean"] for x in sens_prefs], "s-", color="#2563EB", label="TO-BE (ILP)")
    axes[2].set_xticks(p_x)
    axes[2].set_title("Độ nhạy 3: Số khung giờ rảnh thu thập", fontweight="bold", fontsize=10)
    axes[2].set_xlabel("Số khung giờ tối đa thu thập / HV")
    axes[2].set_ylabel("Tỷ lệ ghép thành công (%)")
    axes[2].set_ylim(40, 105)
    axes[2].grid(alpha=0.3)
    axes[2].legend(frameon=False)

    fig.suptitle("Phân tích độ nhạy (Sensitivity Analysis): AS-IS vs TO-BE", fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig3_sensitivity_analysis.png"), bbox_inches="tight")
    plt.close()

    # --- Figure 4: Multi-objective Pareto Trade-off & Dominance (Slide L5 P21-25) ---
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 4.4), dpi=220)

    # Panel A: Provider Cost (Classes Opened) vs Beneficiary Match Rate (%)
    p_cls = [pt["classes_opened"] for pt in pareto_pts]
    p_mr = [pt["match_rate"] for pt in pareto_pts]
    axes[0].plot(p_cls, p_mr, "s-", color="#2563EB", lw=2.0, markersize=7, label="Đường biên Pareto TO-BE (Quét chi phí mở lớp γ)")
    for idx, pt in enumerate(pareto_pts):
        lbl = f"γ={pt['gamma_cost']:g}\n({pt['classes_opened']:.1f} ca, {pt['match_rate']:.1f}%)"
        dy = -24 if idx == 1 else 7
        dx = -42 if idx in (0, 1) else 6
        axes[0].annotate(lbl, (pt["classes_opened"], pt["match_rate"]),
                         textcoords="offset points", xytext=(dx, dy), fontsize=7.6, fontweight="bold", color="#1E3A8A")
    axes[0].set_xlabel("Mục tiêu Nhà cung cấp: Số lớp/ca gia sư phải mở (Càng ít càng tiết kiệm)")
    axes[0].set_ylabel("Mục tiêu Người học: Tỷ lệ ghép thành công (%)")
    axes[0].set_title("A. Đường biên Pareto: Chi phí số ca mở vs Tỷ lệ ghép", fontweight="bold", fontsize=10)
    axes[0].set_ylim(50, 104)
    axes[0].set_xlim(min(p_cls) - 3, max(p_cls) + 5)
    axes[0].grid(alpha=0.3)
    axes[0].legend(frameon=False, loc="lower right", fontsize=8.5)

    # Panel B: Pareto Dominance in Service Quality Space (Match Rate % vs System-wide Schedule Fit)
    as_mr = base["as_is"]["match_rate_mean"]
    as_fa = base["as_is"]["fit_all_mean"]
    tb_pts = [(mp, r["to_be"]["match_rate_mean"], r["to_be"]["fit_all_mean"]) for mp, r in sens_prefs]
    axes[1].scatter([as_mr], [as_fa], color="#DC2626", s=100, zorder=5, label="Phương án AS-IS (Bị trội hoàn toàn)")
    axes[1].annotate(f"AS-IS ({as_mr:.1f}%, {as_fa:.1f}đ)\n[Bị trội ở cả 2 mục tiêu]",
                     (as_mr, as_fa), textcoords="offset points", xytext=(8, -6),
                     fontsize=8.5, fontweight="bold", color="#B91C1C")
    axes[1].plot([x[1] for x in tb_pts], [x[2] for x in tb_pts], "s-", color="#16A34A", lw=2.0, markersize=7,
                 label="Phương án TO-BE (1 -> 2 -> 3 slot)")
    for mp, mr_v, fa_v in tb_pts:
        axes[1].annotate(f"TO-BE ({mp} slot)\n({mr_v:.1f}%, {fa_v:.1f}đ)",
                         (mr_v, fa_v), textcoords="offset points", xytext=(-48, -22 if mp == 2 else 6),
                         fontsize=8, fontweight="bold", color="#166534")
    axes[1].set_xlim(52, 102)
    axes[1].set_ylim(50, 98)
    axes[1].set_xlabel("Mục tiêu 1: Tỷ lệ ghép thành công (%) — Càng cao càng tốt")
    axes[1].set_ylabel("Mục tiêu 2: Điểm phù hợp lịch toàn hệ thống — Càng cao càng tốt")
    axes[1].set_title("B. Kiểm định Trội Pareto (Bài L5 — Trang 22): AS-IS vs TO-BE", fontweight="bold", fontsize=10)
    axes[1].grid(alpha=0.3)
    axes[1].legend(frameon=False, loc="upper left", fontsize=8.5)

    fig.suptitle("Phân tích Tối ưu hóa Đa mục tiêu & Kiểm định Trội Pareto (Slide L5 Trang 21–25)", fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig4_pareto_tradeoff.png"), bbox_inches="tight")
    plt.close()

    print("Done! Baseline summary:", flush=True)
    print(json.dumps(base, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    import sys
    if "--pareto-only" in sys.argv:
        json_path = os.path.join(OUT_DIR, "simulation_results.json")
        with open(json_path, encoding="utf-8") as f:
            summary = json.load(f)
        base = summary["baseline"]
        sens_prefs_raw = summary["sensitivity_prefs"]
        pareto_pts = run_pareto_frontier(n_reps=12, n_students=60, n_tutors=10, seed=42)
        summary["pareto_frontier"] = pareto_pts
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        fig, axes = plt.subplots(1, 2, figsize=(13.2, 4.4), dpi=220)
        p_cls = [pt["classes_opened"] for pt in pareto_pts]
        p_mr = [pt["match_rate"] for pt in pareto_pts]
        axes[0].plot(p_cls, p_mr, "s-", color="#2563EB", lw=2.0, markersize=7, label="Đường biên Pareto TO-BE (Quét chi phí mở lớp γ)")
        offsets = [(-45, 8), (8, -14), (-105, -6), (8, 6)]
        for idx, pt in enumerate(pareto_pts):
            lbl = f"γ={pt['gamma_cost']:g} ({pt['classes_opened']:.1f} ca, {pt['match_rate']:.1f}%)"
            dx, dy = offsets[idx] if idx < len(offsets) else (6, 6)
            axes[0].annotate(lbl, (pt["classes_opened"], pt["match_rate"]),
                             textcoords="offset points", xytext=(dx, dy), fontsize=7.6, fontweight="bold", color="#1E3A8A")
        axes[0].set_xlabel("Mục tiêu Nhà cung cấp: Số lớp/ca gia sư phải mở (Càng ít càng tiết kiệm)")
        axes[0].set_ylabel("Mục tiêu Người học: Tỷ lệ ghép thành công (%)")
        axes[0].set_title("A. Đường biên Pareto: Chi phí số ca mở vs Tỷ lệ ghép", fontweight="bold", fontsize=10)
        axes[0].set_ylim(46, 104)
        axes[0].set_xlim(min(p_cls) - 3, max(p_cls) + 9)
        axes[0].grid(alpha=0.3)
        axes[0].legend(frameon=False, loc="lower right", fontsize=8.5)
        as_mr = base["as_is"]["match_rate_mean"]
        as_fa = base["as_is"]["fit_all_mean"]
        tb_pts = [(mp, r_tb["match_rate_mean"], r_tb["fit_all_mean"]) for mp, r_as, r_tb in sens_prefs_raw]
        axes[1].scatter([as_mr], [as_fa], color="#DC2626", s=100, zorder=5, label="Phương án AS-IS (Bị trội hoàn toàn)")
        axes[1].annotate(f"AS-IS ({as_mr:.1f}%, {as_fa:.1f}đ)\n[Bị trội ở cả 2 mục tiêu]",
                         (as_mr, as_fa), textcoords="offset points", xytext=(8, -6),
                         fontsize=8.5, fontweight="bold", color="#B91C1C")
        axes[1].plot([x[1] for x in tb_pts], [x[2] for x in tb_pts], "s-", color="#16A34A", lw=2.0, markersize=7,
                     label="Phương án TO-BE (1 -> 2 -> 3 slot)")
        for mp, mr_v, fa_v in tb_pts:
            axes[1].annotate(f"TO-BE ({mp} slot)\n({mr_v:.1f}%, {fa_v:.1f}đ)",
                             (mr_v, fa_v), textcoords="offset points", xytext=(-48, -24 if mp == 2 else 6),
                             fontsize=8, fontweight="bold", color="#166534")
        axes[1].set_xlim(52, 102)
        axes[1].set_ylim(50, 98)
        axes[1].set_xlabel("Mục tiêu 1: Tỷ lệ ghép thành công (%) — Càng cao càng tốt")
        axes[1].set_ylabel("Mục tiêu 2: Điểm phù hợp lịch toàn hệ thống")
        axes[1].set_title("B. Kiểm định Trội Pareto (Bài L5 — Trang 22): AS-IS vs TO-BE", fontweight="bold", fontsize=10)
        axes[1].grid(alpha=0.3)
        axes[1].legend(frameon=False, loc="upper left", fontsize=8.5)
        fig.suptitle("Phân tích Tối ưu hóa Đa mục tiêu & Kiểm định Trội Pareto (Slide L5 Trang 21–25)", fontweight="bold", y=1.02)
        plt.tight_layout()
        plt.savefig(os.path.join(OUT_DIR, "fig4_pareto_tradeoff.png"), bbox_inches="tight")
        plt.close()
        print("Pareto updated:", json.dumps(pareto_pts, indent=2))
    else:
        main()
