"""
Script tham khao (Read-Only & An danh hoa) de trich xuat du lieu that tu DB CatPlus.
Chay bang Django shell hoac Django management command tren moi truong server/local
ma KHONG lay ten, email, SDT cua hoc vien hay phu huynh.

Cach dung (vi du voi service academic):
  python manage.py shell < export_academic_stats.py
"""

import csv
import hashlib

def anon_id(uuid_val):
    if uuid_val is None:
        return ""
    return hashlib.sha256(str(uuid_val).encode()).hexdigest()[:10]


def export_academic_csv(output_dir="./exported_data"):
    import os
    from academic_app.models import Student, Class, ClassScheduleRule, Enrollment, TrialSession

    os.makedirs(output_dir, exist_ok=True)

    # 1. Xuat trang thai tuyen sinh & thoi gian cho (an danh)
    with open(os.path.join(output_dir, "students_intake.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["student_hash", "birth_year", "intake_outcome", "closed_lost_reason", "created_at", "enrolled_at", "closed_lost_at"])
        for s in Student.objects.all():
            w.writerow([
                anon_id(s.id), s.birth_year or "", s.intake_outcome,
                s.closed_lost_reason or "", s.created_at.isoformat(),
                s.enrolled_at.isoformat() if s.enrolled_at else "",
                s.closed_lost_at.isoformat() if s.closed_lost_at else "",
            ])

    # 2. Xuat cau truc lop & khung gio day thuc te cua gia su
    with open(os.path.join(output_dir, "class_schedule_rules.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["class_hash", "tutor_hash", "class_type", "education_level", "max_students", "status", "weekday", "start_time", "duration_minutes"])
        for r in ClassScheduleRule.objects.select_related("class_obj").all():
            c = r.class_obj
            w.writerow([
                anon_id(c.id), anon_id(c.tutor_identity_user_id),
                c.class_type, c.education_level or "", c.max_students, c.status,
                r.weekday, r.start_time.isoformat(), r.duration_minutes,
            ])

    # 3. Xuat lich su hoc thu (TrialSession)
    with open(os.path.join(output_dir, "trial_sessions.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["trial_hash", "tutor_hash", "mode", "status", "delivery_mode", "created_at", "scheduled_start_at", "completed_at", "cancelled_at"])
        for t in TrialSession.objects.all():
            w.writerow([
                anon_id(t.id), anon_id(t.tutor_identity_user_id),
                t.mode, t.status, t.delivery_mode or "",
                t.created_at.isoformat(),
                t.scheduled_start_at.isoformat() if t.scheduled_start_at else "",
                t.completed_at.isoformat() if t.completed_at else "",
                t.cancelled_at.isoformat() if t.cancelled_at else "",
            ])


def export_customer_ops_csv(output_dir="./exported_data"):
    import os
    from customer_ops.models import StudentJourney, StudentJourneyEvent

    os.makedirs(output_dir, exist_ok=True)

    # Xuat log chuyen trang thai trong hanh trinh khach hang
    with open(os.path.join(output_dir, "journey_events.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["student_hash", "cskh_hash", "current_stage", "event_type", "from_stage", "to_stage", "occurred_at"])
        for ev in StudentJourneyEvent.objects.select_related("journey").order_by("occurred_at"):
            j = ev.journey
            w.writerow([
                anon_id(j.academic_student_id),
                anon_id(j.assigned_customer_care_identity_user_id),
                j.lifecycle_stage, ev.event_type,
                ev.from_stage or "", ev.to_stage or "",
                ev.occurred_at.isoformat(),
            ])
