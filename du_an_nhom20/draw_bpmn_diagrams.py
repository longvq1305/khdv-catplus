"""
Render high-resolution visual BPMN 2.0 Swimlane Diagrams (AS-IS and TO-BE)
matching catplus_matching_as_is.bpmn and catplus_matching_to_be.bpmn
with zero overlapping labels or crossed boxes.
"""

import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, Rectangle

plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Segoe UI"]
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def draw_pool_lane(ax, x, y, w, h, label, bg="#F8FAFC", ec="#334155", header_bg="#E2E8F0", lw=1.4):
    rect = Rectangle((x, y), w, h, facecolor=bg, edgecolor=ec, linewidth=lw, zorder=1)
    ax.add_patch(rect)
    hdr_w = 0.036
    hdr = Rectangle((x, y), hdr_w, h, facecolor=header_bg, edgecolor=ec, linewidth=lw, zorder=2)
    ax.add_patch(hdr)
    ax.text(x + hdr_w / 2, y + h / 2, label, ha="center", va="center",
            rotation=90, fontsize=7.8, fontweight="bold", color="#0F172A", zorder=3)


def draw_task(ax, cx, cy, w, h, text, fc="#FFFFFF", ec="#1D4ED8"):
    box = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="round,pad=0.005,rounding_size=0.011",
        facecolor=fc, edgecolor=ec, linewidth=1.35, zorder=4
    )
    ax.add_patch(box)
    ax.text(cx, cy, text, ha="center", va="center", fontsize=7.1,
            color="#0F172A", fontweight="bold", linespacing=1.2, zorder=5)


def draw_event(ax, cx, cy, r, kind="start", label="", label_pos="bottom"):
    if kind == "start":
        c = Circle((cx, cy), r, facecolor="#DCFCE7", edgecolor="#15803D", linewidth=1.5, zorder=5)
        ax.add_patch(c)
    elif kind in ("catch", "timer"):
        c1 = Circle((cx, cy), r, facecolor="#FEF3C7", edgecolor="#D97706", linewidth=1.3, zorder=6)
        c2 = Circle((cx, cy), r * 0.76, facecolor="#FEF3C7", edgecolor="#D97706", linewidth=1.0, zorder=6)
        ax.add_patch(c1)
        ax.add_patch(c2)
        if kind == "timer":
            ax.plot([cx, cx], [cy, cy + r * 0.45], color="#B45309", lw=1.2, zorder=7)
            ax.plot([cx, cx + r * 0.35], [cy, cy], color="#B45309", lw=1.2, zorder=7)
        else:
            ax.text(cx, cy, "✉", ha="center", va="center", fontsize=7.2, color="#B45309", zorder=7)
    elif kind == "end_ok":
        c = Circle((cx, cy), r, facecolor="#BBF7D0", edgecolor="#166534", linewidth=2.5, zorder=5)
        ax.add_patch(c)
    elif kind == "end_fail":
        c = Circle((cx, cy), r, facecolor="#FECACA", edgecolor="#991B1B", linewidth=2.5, zorder=5)
        ax.add_patch(c)

    if label:
        if label_pos == "bottom":
            dy = -r - 0.021
        elif label_pos == "top":
            dy = r + 0.020
        else:
            dy = -r - 0.021
        ax.text(cx, cy + dy, label, ha="center", va="center", fontsize=6.6,
                color="#1E293B", fontweight="bold", linespacing=1.12, zorder=7)


def draw_gateway(ax, cx, cy, r, label="", label_pos="top"):
    pts = [(cx, cy + r), (cx + r * 0.75, cy), (cx, cy - r), (cx - r * 0.75, cy)]
    poly = Polygon(pts, closed=True, facecolor="#FEF9C3", edgecolor="#CA8A04", linewidth=1.4, zorder=5)
    ax.add_patch(poly)
    ax.text(cx, cy, "×", ha="center", va="center", fontsize=10.5, fontweight="bold", color="#854D0E", zorder=6)
    if label:
        dy = r + 0.019 if label_pos == "top" else -r - 0.019
        ax.text(cx, cy + dy, label, ha="center", va="center", fontsize=6.6,
                color="#713F12", fontweight="bold", zorder=7)


def draw_flow(ax, x1, y1, x2, y2, label="", msg=False, color=None, rad=0.0, lx=0.0, ly=0.0):
    if color is None:
        color = "#0369A1" if msg else "#1E293B"
    ls = "--" if msg else "-"
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.2, linestyle=ls,
                        connectionstyle=f"arc3,rad={rad}"),
        zorder=4 if not msg else 6
    )
    if label:
        mx, my = (x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly
        ax.text(mx, my, label, ha="center", va="center", fontsize=6.4,
                color=color, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.9),
                zorder=8)


def draw_annotation(ax, x, y, w, h, text, target_x, target_y, ec="#DC2626"):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.004,rounding_size=0.008",
        facecolor="#FEF2F2", edgecolor=ec, linewidth=1.1, linestyle=":", zorder=7
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=6.4, color="#991B1B" if ec == "#DC2626" else "#1E3A8A",
            fontweight="bold", linespacing=1.15, zorder=8)
    ax.plot([x + w / 2, target_x], [y, target_y], color=ec, linestyle=":", linewidth=1.0, zorder=6)


def render_as_is():
    fig, ax = plt.subplots(figsize=(15.5, 9.2), dpi=220)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.984, "SƠ ĐỒ QUY TRÌNH BPMN 2.0 HIỆN TẠI (AS-IS): TIẾP NHẬN, GHÉP GIA SƯ & XẾP LỊCH HỌC CATPLUS",
            ha="center", va="top", fontsize=11.5, fontweight="bold", color="#0F172A")
    ax.text(0.5, 0.955, "Process Instance: 1 yêu cầu đăng ký học viên mới (Tệp chuẩn BPMN: catplus_matching_as_is.bpmn)",
            ha="center", va="top", fontsize=8.5, color="#475569")

    draw_pool_lane(ax, 0.02, 0.78, 0.96, 0.145, "POOL 1:\nPHỤ HUYNH & HV", bg="#FFFBEB", header_bg="#FDE68A")
    draw_pool_lane(ax, 0.02, 0.57, 0.96, 0.175, "LANE CSKH\n(Pool CatPlus)", bg="#F0F9FF", header_bg="#BAE6FD")
    draw_pool_lane(ax, 0.02, 0.39, 0.96, 0.18, "LANE QUẢN LÝ\n(Pool CatPlus)", bg="#EFF6FF", header_bg="#BFDBFE")
    draw_pool_lane(ax, 0.02, 0.23, 0.96, 0.16, "LANE HỆ THỐNG\n(Pool CatPlus)", bg="#F5F3FF", header_bg="#DDD6FE")
    draw_pool_lane(ax, 0.02, 0.05, 0.96, 0.15, "POOL 3:\nGIA SƯ", bg="#F0FDF4", header_bg="#BBF7D0")

    # POOL 1
    draw_event(ax, 0.085, 0.855, 0.016, "start", "Nhu cầu học")
    draw_task(ax, 0.18, 0.855, 0.105, 0.062, "Gửi thông tin\nđăng ký học", fc="#FEF3C7", ec="#D97706")
    draw_event(ax, 0.28, 0.855, 0.015, "catch", "Nhận gọi")
    draw_task(ax, 0.38, 0.855, 0.115, 0.062, "Cung cấp mục tiêu\n& 1 slot ưu tiên", fc="#FEF3C7", ec="#D97706")
    draw_event(ax, 0.565, 0.855, 0.015, "catch", "Báo lệch lịch")
    draw_task(ax, 0.675, 0.855, 0.115, 0.062, "Đề xuất lịch khác\nhoặc hủy chờ", fc="#FEF3C7", ec="#D97706")
    draw_event(ax, 0.835, 0.855, 0.015, "catch", "Nhận lịch chốt")
    draw_event(ax, 0.93, 0.855, 0.016, "end_ok", "Bắt đầu học")

    draw_flow(ax, 0.101, 0.855, 0.127, 0.855)
    draw_flow(ax, 0.233, 0.855, 0.265, 0.855)
    draw_flow(ax, 0.295, 0.855, 0.322, 0.855)
    draw_flow(ax, 0.438, 0.855, 0.550, 0.855)
    draw_flow(ax, 0.580, 0.855, 0.617, 0.855)
    draw_flow(ax, 0.733, 0.855, 0.820, 0.855)
    draw_flow(ax, 0.850, 0.855, 0.914, 0.855)

    # POOL 2
    draw_event(ax, 0.105, 0.66, 0.015, "catch", "Hồ sơ mới\n(CHUA_LIEN_HE)")
    draw_task(ax, 0.175, 0.305, 0.12, 0.062, "Tạo Student (PENDING)\n& StudentJourney", fc="#EDE9FE", ec="#6D28D9")

    draw_task(ax, 0.32, 0.66, 0.125, 0.064, "Tư vấn & hỏi\n1 khung giờ ưu tiên", fc="#E0F2FE", ec="#0284C4")
    draw_event(ax, 0.27, 0.625, 0.012, "timer", "Quá 24h", label_pos="bottom")

    draw_task(ax, 0.34, 0.475, 0.13, 0.064, "Dò lịch thủ công (FCFS)\n& nhắn hỏi Gia sư", fc="#DBEAFE", ec="#1D4ED8")
    draw_event(ax, 0.46, 0.475, 0.015, "catch", "Chờ GS trả lời")
    draw_event(ax, 0.475, 0.445, 0.011, "timer", "8h", label_pos="bottom")
    draw_gateway(ax, 0.555, 0.475, 0.022, "Khớp GS & đủ nhóm?")
    draw_gateway(ax, 0.645, 0.475, 0.022, ">= 2 vòng?", label_pos="bottom")

    draw_task(ax, 0.645, 0.66, 0.12, 0.064, "Gọi lại phụ huynh\nxin khung giờ khác", fc="#FEE2E2", ec="#DC2626")
    draw_gateway(ax, 0.75, 0.66, 0.021, "Đổi giờ?")

    draw_task(ax, 0.76, 0.485, 0.115, 0.06, "Tạo TrialSession /\nClass trên hệ thống", fc="#DCFCE7", ec="#15803D")
    draw_task(ax, 0.73, 0.305, 0.12, 0.062, "Cập nhật ENROLLED\n(DA_THAM_GIA)", fc="#DCFCE7", ec="#15803D")
    draw_task(ax, 0.845, 0.66, 0.11, 0.062, "Xác nhận lịch học\nvới phụ huynh", fc="#DCFCE7", ec="#15803D")
    draw_event(ax, 0.938, 0.66, 0.016, "end_ok", "Nhập học\nthành công")

    draw_task(ax, 0.865, 0.305, 0.11, 0.062, "Ghi CLOSED_LOST\n(Lệch lịch/Thiếu GS)", fc="#FEE2E2", ec="#B91C1C")
    draw_event(ax, 0.95, 0.305, 0.015, "end_fail", "CLOSED_LOST")

    # Sequence flows inside Pool 2
    draw_flow(ax, 0.105, 0.644, 0.13, 0.336)
    draw_flow(ax, 0.235, 0.336, 0.265, 0.635)
    draw_flow(ax, 0.32, 0.628, 0.32, 0.507, "Handoff 1", lx=-0.032)
    draw_flow(ax, 0.405, 0.475, 0.445, 0.475)
    draw_flow(ax, 0.475, 0.475, 0.533, 0.475)
    draw_flow(ax, 0.577, 0.475, 0.623, 0.475, "Không", ly=0.014)
    draw_flow(ax, 0.555, 0.497, 0.702, 0.497, "Có (Khớp)", ly=0.014, color="#15803D")
    draw_flow(ax, 0.645, 0.497, 0.645, 0.628, "Chưa (<2)", lx=-0.032)
    draw_flow(ax, 0.667, 0.475, 0.83, 0.336, "Quá 2 vòng", color="#B91C1C", lx=0.025, ly=-0.018)
    draw_flow(ax, 0.705, 0.66, 0.729, 0.66)
    # Rework arc goes above Task_Mgr cleanly without crossing annotation
    draw_flow(ax, 0.75, 0.681, 0.36, 0.507, "Có giờ mới (Rework)", rad=-0.16, color="#B91C1C", lx=-0.075, ly=-0.048)
    draw_flow(ax, 0.771, 0.66, 0.865, 0.336, "Hủy chờ", color="#B91C1C", lx=0.028, ly=0.03)
    # Timeout 24h goes cleanly along lower lane boundary
    draw_flow(ax, 0.27, 0.612, 0.82, 0.27, "Timeout 24h", rad=0.22, color="#B91C1C", lx=-0.08, ly=-0.055)
    draw_flow(ax, 0.475, 0.433, 0.635, 0.458, "Timeout 8h", rad=0.14, color="#B45309", ly=-0.018)
    draw_flow(ax, 0.76, 0.455, 0.73, 0.336)
    draw_flow(ax, 0.76, 0.336, 0.825, 0.628)
    draw_flow(ax, 0.90, 0.66, 0.922, 0.66)
    draw_flow(ax, 0.92, 0.305, 0.935, 0.305)

    # POOL 3
    draw_event(ax, 0.34, 0.125, 0.015, "catch", "Nhận tin hỏi lịch")
    draw_task(ax, 0.46, 0.125, 0.125, 0.062, "Kiểm tra lịch rảnh\n& phản hồi (Zalo)", fc="#DCFCE7", ec="#15803D")
    draw_event(ax, 0.58, 0.125, 0.015, "end_ok", "Đã phản hồi")
    draw_flow(ax, 0.355, 0.125, 0.397, 0.125)
    draw_flow(ax, 0.523, 0.125, 0.565, 0.125)

    # Message Flows
    draw_flow(ax, 0.15, 0.824, 0.105, 0.676, "Đăng ký", msg=True, lx=-0.024)
    draw_flow(ax, 0.295, 0.692, 0.28, 0.838, "Gọi tư vấn", msg=True, lx=-0.026)
    draw_flow(ax, 0.38, 0.824, 0.34, 0.692, "Báo 1 slot", msg=True, lx=0.026)
    draw_flow(ax, 0.34, 0.443, 0.34, 0.141, "Nhắn hỏi GS", msg=True, lx=-0.034)
    draw_flow(ax, 0.46, 0.156, 0.46, 0.459, "GS trả lời", msg=True, lx=0.028)
    draw_flow(ax, 0.625, 0.692, 0.565, 0.838, "Xin giờ khác", msg=True, lx=-0.026)
    draw_flow(ax, 0.675, 0.824, 0.665, 0.692, "Slot mới/Hủy", msg=True, lx=0.034)
    draw_flow(ax, 0.845, 0.692, 0.835, 0.838, "Báo lịch chốt", msg=True, lx=0.034)

    # Annotations placed in clear whitespace
    draw_annotation(ax, 0.07, 0.465, 0.18, 0.082,
                    "[Bottleneck & Handoff]\nDò tay FCFS từng ca; nhóm\nGroup < 3 HV bị kẹt ở CHO_LOP",
                    0.275, 0.475)
    draw_annotation(ax, 0.42, 0.642, 0.155, 0.072,
                    "[Waiting & Rework]\nChờ GS trả lời Zalo (2–8h)\n& hỏi lại phụ huynh (~45%)",
                    0.46, 0.491)

    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, "fig_bpmn_as_is.png")
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_path}")


def render_to_be():
    fig, ax = plt.subplots(figsize=(15.5, 8.8), dpi=220)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.984, "SƠ ĐỒ QUY TRÌNH BPMN 2.0 CẢI TIẾN (TO-BE): HUMAN-IN-THE-LOOP + GỢI Ý TỐI ƯU MILP",
            ha="center", va="top", fontsize=11.5, fontweight="bold", color="#0F172A")
    ax.text(0.5, 0.955, "Cơ chế cải tiến: Chuẩn hóa thu thập 1–3 slot rảnh + MILP gom cụm lớp & gợi ý + Quản lý duyệt 1 vòng (catplus_matching_to_be.bpmn)",
            ha="center", va="top", fontsize=8.5, color="#475569")

    draw_pool_lane(ax, 0.02, 0.78, 0.96, 0.145, "POOL 1:\nPHỤ HUYNH & HV", bg="#FFFBEB", header_bg="#FDE68A")
    draw_pool_lane(ax, 0.02, 0.57, 0.96, 0.175, "LANE CSKH\n(Pool CatPlus)", bg="#F0F9FF", header_bg="#BAE6FD")
    draw_pool_lane(ax, 0.02, 0.39, 0.96, 0.18, "LANE QUẢN LÝ\n(Pool CatPlus)", bg="#EFF6FF", header_bg="#BFDBFE")
    draw_pool_lane(ax, 0.02, 0.23, 0.96, 0.16, "LANE HỆ THỐNG\n+ MODULE MILP", bg="#F5F3FF", header_bg="#DDD6FE")
    draw_pool_lane(ax, 0.02, 0.05, 0.96, 0.15, "POOL 3:\nGIA SƯ", bg="#F0FDF4", header_bg="#BBF7D0")

    # Pool 1
    draw_event(ax, 0.09, 0.855, 0.016, "start", "Nhu cầu học")
    draw_task(ax, 0.20, 0.855, 0.115, 0.062, "Gửi thông tin\nđăng ký học", fc="#FEF3C7", ec="#D97706")
    draw_event(ax, 0.32, 0.855, 0.015, "catch", "Nhận gọi")
    draw_task(ax, 0.44, 0.855, 0.14, 0.062, "Cung cấp bộ 1–3 khung\ngiờ rảnh theo ưu tiên", fc="#FEF3C7", ec="#D97706")
    draw_event(ax, 0.85, 0.855, 0.015, "catch", "Nhận lịch chốt\n(1 vòng)")
    draw_event(ax, 0.94, 0.855, 0.016, "end_ok", "Bắt đầu học")

    draw_flow(ax, 0.106, 0.855, 0.142, 0.855)
    draw_flow(ax, 0.258, 0.855, 0.305, 0.855)
    draw_flow(ax, 0.335, 0.855, 0.37, 0.855)
    draw_flow(ax, 0.51, 0.855, 0.835, 0.855)
    draw_flow(ax, 0.865, 0.855, 0.924, 0.855)

    # Pool 2
    draw_event(ax, 0.12, 0.66, 0.015, "catch", "Hồ sơ mới")
    draw_task(ax, 0.19, 0.305, 0.12, 0.062, "Ghi nhận Student\n& StudentJourney", fc="#EDE9FE", ec="#6D28D9")
    draw_task(ax, 0.36, 0.66, 0.14, 0.064, "Tư vấn & nhập chuẩn\nhóa 1–3 slot ưu tiên", fc="#E0F2FE", ec="#0284C4")
    draw_task(ax, 0.36, 0.305, 0.15, 0.064, "Chạy MILP gợi ý Top cặp\nghép cặp & gom nhóm 3–5", fc="#DDD6FE", ec="#5B21B6")
    draw_gateway(ax, 0.495, 0.475, 0.022, "Có nghiệm khả thi?")

    # Put CLOSED_LOST to the left-middle of system lane (x=0.53) so tutor message flows at x=0.64 & 0.74 don't cross it!
    draw_task(ax, 0.53, 0.305, 0.115, 0.062, "Ghi CLOSED_LOST\n(Vượt trần công suất)", fc="#FEE2E2", ec="#B91C1C")
    draw_event(ax, 0.618, 0.305, 0.014, "end_fail", "Đóng hồ sơ")

    draw_task(ax, 0.635, 0.475, 0.13, 0.064, "Quản lý duyệt gợi ý\n& gửi xác nhận GS", fc="#DBEAFE", ec="#1D4ED8")
    draw_event(ax, 0.74, 0.475, 0.015, "catch", "GS xác nhận")
    draw_gateway(ax, 0.815, 0.475, 0.021, "GS đồng ý?", label_pos="bottom")
    draw_task(ax, 0.73, 0.542, 0.115, 0.038, "Chọn PA dự phòng #2", fc="#FEF3C7", ec="#D97706")

    draw_task(ax, 0.855, 0.305, 0.125, 0.062, "Tạo Class/Trial &\ncập nhật ENROLLED", fc="#DCFCE7", ec="#15803D")
    draw_task(ax, 0.855, 0.66, 0.12, 0.062, "Thông báo lịch chốt\ncho phụ huynh", fc="#DCFCE7", ec="#15803D")
    draw_event(ax, 0.945, 0.66, 0.016, "end_ok", "Nhập học\nthành công")

    draw_flow(ax, 0.12, 0.644, 0.145, 0.336)
    draw_flow(ax, 0.25, 0.336, 0.305, 0.63)
    draw_flow(ax, 0.36, 0.628, 0.36, 0.337, "Dữ liệu 3 slot", lx=-0.036)
    draw_flow(ax, 0.435, 0.305, 0.495, 0.453, "Top gợi ý", lx=-0.025, ly=0.015)
    draw_flow(ax, 0.517, 0.475, 0.57, 0.475, "Có", ly=0.012, color="#15803D")
    draw_flow(ax, 0.495, 0.453, 0.515, 0.336, "Không", color="#B91C1C", lx=0.022)
    draw_flow(ax, 0.588, 0.305, 0.604, 0.305)
    draw_flow(ax, 0.70, 0.475, 0.725, 0.475)
    draw_flow(ax, 0.755, 0.475, 0.794, 0.475)
    draw_flow(ax, 0.815, 0.496, 0.788, 0.542, "Bận (8%)", color="#B45309", lx=0.028)
    draw_flow(ax, 0.672, 0.542, 0.635, 0.507, color="#B45309")
    draw_flow(ax, 0.836, 0.475, 0.855, 0.336, "Đồng ý", color="#15803D", lx=0.025)
    draw_flow(ax, 0.855, 0.336, 0.855, 0.629)
    draw_flow(ax, 0.915, 0.66, 0.929, 0.66)

    # Pool 3 (positioned at x=0.635 and x=0.74 so vertical message flows drop through clear space!)
    draw_event(ax, 0.635, 0.125, 0.015, "catch", "Nhận đề xuất\nđã lọc lịch rảnh")
    draw_task(ax, 0.74, 0.125, 0.12, 0.062, "Xác nhận nhận lớp\n(1 chạm)", fc="#DCFCE7", ec="#15803D")
    draw_event(ax, 0.85, 0.125, 0.015, "end_ok", "Chốt lịch dạy")
    draw_flow(ax, 0.65, 0.125, 0.68, 0.125)
    draw_flow(ax, 0.80, 0.125, 0.835, 0.125)

    # Message Flows (passing cleanly at x=0.635 and x=0.74 between x=0.62 and x=0.79!)
    draw_flow(ax, 0.17, 0.824, 0.12, 0.676, "Đăng ký", msg=True, lx=-0.025)
    draw_flow(ax, 0.335, 0.692, 0.32, 0.838, "Gọi tư vấn", msg=True, lx=-0.025)
    draw_flow(ax, 0.44, 0.824, 0.395, 0.692, "Bộ 1–3 slot", msg=True, lx=0.03)
    draw_flow(ax, 0.635, 0.443, 0.635, 0.141, "Đề xuất khớp sẵn", msg=True, lx=0.042, ly=-0.04)
    draw_flow(ax, 0.74, 0.156, 0.74, 0.459, "Xác nhận", msg=True, lx=0.028, ly=-0.04)
    draw_flow(ax, 0.855, 0.692, 0.85, 0.838, "Báo lịch chốt", msg=True, lx=0.032)

    # Annotations
    draw_annotation(ax, 0.07, 0.46, 0.21, 0.082,
                    "[Automate & Simplify - L3B/L5]\nMILP tự động gom nhóm 3–5 HV &\nbảo toàn gia sư cho ca lịch hẹp",
                    0.32, 0.336, ec="#15803D")
    draw_annotation(ax, 0.49, 0.635, 0.21, 0.078,
                    "[Design Recovery - L3B]\nLoại bỏ vòng lặp hỏi lại phụ huynh;\nQuản lý vẫn giữ quyền duyệt cuối",
                    0.635, 0.507, ec="#1D4ED8")

    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, "fig_bpmn_to_be.png")
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_path}")


if __name__ == "__main__":
    render_as_is()
    render_to_be()
