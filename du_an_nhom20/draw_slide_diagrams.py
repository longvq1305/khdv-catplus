"""
Generate high-legibility, projector-optimized diagrams for the 10-minute slide deck
using the unified Forest Green - Warm Yellow/Amber - Vibrant Orange palette.
Outputs:
  - slide_fig_resource_map.png
  - slide_fig_bpmn_as_is.png
  - slide_fig_bpmn_to_be.png
"""

import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, Rectangle

plt.rcParams["font.sans-serif"] = ["Arial", "Segoe UI", "DejaVu Sans"]
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def draw_card(ax, x, y, w, h, title, body, fc, ec, title_color, lw=1.8, title_fs=10.5, body_fs=9.0):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.010,rounding_size=0.020",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h - 0.024, title, ha="center", va="top",
            fontsize=title_fs, fontweight="bold", color=title_color, zorder=4)
    ax.text(x + w / 2, y + h - 0.068, body, ha="center", va="top",
            fontsize=body_fs, color="#14261E", linespacing=1.38, zorder=4)


def draw_arrow(ax, x1, y1, x2, y2, label="", color="#15803D", ls="-", rad=0.0, lx=0.0, ly=0.0, fs=8.3):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.7, linestyle=ls,
                        connectionstyle=f"arc3,rad={rad}"),
        zorder=5
    )
    if label:
        mx, my = (x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly
        ax.text(mx, my, label, ha="center", va="center", fontsize=fs,
                color=color, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.18", fc="#FFFFFF", ec="none", alpha=0.95),
                zorder=6)


def render_slide_resource_map():
    fig, ax = plt.subplots(figsize=(10.5, 6.2), dpi=260)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # System Boundary
    boundary = FancyBboxPatch(
        (0.02, 0.14), 0.96, 0.82,
        boxstyle="round,pad=0.01,rounding_size=0.022",
        facecolor="#F9FBF9", edgecolor="#0F3D2E", linewidth=2.2, linestyle="--", zorder=1
    )
    ax.add_patch(boundary)
    ax.text(0.04, 0.945, "RANH GIỚI HỆ THỐNG GHÉP ĐÔI & XẾP LỊCH CATPLUS",
            ha="left", va="top", fontsize=9.8, fontweight="bold", color="#0F3D2E", zorder=2)
    ax.text(0.96, 0.945, "Ngoài biên: Zalo/ĐT, Hạ tầng mạng, Kỳ thi HSG",
            ha="right", va="top", fontsize=8.6, style="italic", color="#52665D", zorder=2)

    # 1. Học viên & Phụ huynh
    draw_card(
        ax, 0.045, 0.48, 0.255, 0.39,
        "HỌC VIÊN & PHỤ HUYNH",
        "Đóng góp:\n"
        "• Khung giờ rảnh (1–3 ca)\n"
        "• Cấp học THCS / THPT\n"
        "• Hình thức 1–1 hoặc Nhóm\n\n"
        "Rủi ro: Bỏ cuộc nếu chờ lâu",
        fc="#FFFBEB", ec="#F59E0B", title_color="#B45309"
    )

    # 2. CSKH
    draw_card(
        ax, 0.37, 0.66, 0.26, 0.23,
        "CSKH (2 nhân sự)",
        "• Kỹ năng tư vấn & khai thác lịch\n"
        "• Theo dõi hành trình học viên\n"
        "• Báo lịch chốt & chăm sóc",
        fc="#FEFCE8", ec="#D97706", title_color="#92400E"
    )

    # 3. Quản lý học vụ
    draw_card(
        ax, 0.37, 0.38, 0.26, 0.21,
        "QUẢN LÝ HỌC VỤ (1 nhân sự)",
        "• Tri thức phân loại & ghép nhóm\n"
        "• Điều phối lớp 1–1 / Nhóm 3–5\n"
        "• Phê duyệt phương án cuối cùng",
        fc="#ECFDF5", ec="#15803D", title_color="#0F3D2E"
    )

    # 4. Nền tảng CatPlus
    draw_card(
        ax, 0.37, 0.165, 0.26, 0.165,
        "NỀN TẢNG & QUY TẮC LỚP",
        "• Hồ sơ HV, lịch lớp, quy tắc 3–5 HV\n"
        "• [TO-BE] Module MILP gợi ý 2 đợt/ngày",
        fc="#FFF7ED", ec="#EA580C", title_color="#C2410C", title_fs=10.0, body_fs=8.7
    )

    # 5. Gia sư
    draw_card(
        ax, 0.70, 0.48, 0.255, 0.39,
        "GIA SƯ (10 giảng viên)",
        "Đóng góp:\n"
        "• Chuyên môn lập trình & sư phạm\n"
        "• Quỹ 5–7 ca trống / tuần\n"
        "• Trần nhận dạy 3–5 lớp\n\n"
        "Rủi ro: Bận đột xuất (~8%)",
        fc="#ECFDF5", ec="#15803D", title_color="#14532D"
    )

    # Co-creation summary box
    draw_card(
        ax, 0.045, 0.165, 0.255, 0.24,
        "ĐỒNG TẠO GIÁ TRỊ",
        "• Toán hạng: Hồ sơ, ca trống\n"
        "• Toán tử: Kỹ năng + MILP\n"
        "• Kết quả: Vào lớp nhanh, đúng ca",
        fc="#ECFDF5", ec="#0F3D2E", title_color="#0F3D2E", title_fs=10.0, body_fs=8.7
    )

    # Clean non-overlapping flows
    draw_arrow(ax, 0.30, 0.79, 0.37, 0.79, "1–3 khung giờ", color="#B45309", ly=0.038)
    draw_arrow(ax, 0.37, 0.71, 0.30, 0.71, "Chốt lịch học", color="#15803D", ly=-0.038)
    draw_arrow(ax, 0.43, 0.66, 0.43, 0.59, "Chuyển hồ sơ", color="#0F3D2E", lx=-0.062)
    draw_arrow(ax, 0.54, 0.59, 0.54, 0.66, "Đổi giờ / Duyệt", color="#EA580C", ls="--", lx=0.056)
    draw_arrow(ax, 0.45, 0.38, 0.45, 0.33, "Dữ liệu", color="#C2410C", lx=-0.052)
    draw_arrow(ax, 0.55, 0.33, 0.55, 0.38, "Gợi ý MILP", color="#15803D", ls=":", lx=0.062)
    draw_arrow(ax, 0.63, 0.55, 0.70, 0.72, "Đề xuất lớp", color="#15803D", lx=0.032, ly=0.052)
    draw_arrow(ax, 0.70, 0.58, 0.63, 0.45, "Xác nhận / Bận", color="#EA580C", ls="--", lx=0.036, ly=-0.045)
    draw_arrow(ax, 0.172, 0.48, 0.172, 0.405, "Tham gia", color="#0F3D2E", lx=0.055)

    # Bottom Legend
    leg = FancyBboxPatch(
        (0.02, 0.02), 0.96, 0.09,
        boxstyle="round,pad=0.008,rounding_size=0.015",
        facecolor="#FFFFFF", edgecolor="#DAE2DE", linewidth=1.3, zorder=2
    )
    ax.add_patch(leg)
    ax.plot([0.04, 0.085], [0.065, 0.065], color="#15803D", lw=2.2)
    ax.text(0.095, 0.065, "Luồng phối hợp chính", va="center", fontsize=8.5, fontweight="bold", color="#14261E")

    ax.plot([0.30, 0.345], [0.065, 0.065], color="#EA580C", lw=2.2, linestyle="--")
    ax.text(0.355, 0.065, "Phản hồi lệch lịch / Làm lại", va="center", fontsize=8.5, fontweight="bold", color="#14261E")

    ax.plot([0.60, 0.645], [0.065, 0.065], color="#15803D", lw=2.2, linestyle=":")
    ax.text(0.655, 0.065, "Gợi ý tối ưu hóa (TO-BE)", va="center", fontsize=8.5, fontweight="bold", color="#14261E")

    ax.plot([0.84, 0.875], [0.065, 0.065], color="#0F3D2E", lw=2.2, linestyle="--")
    ax.text(0.885, 0.065, "Biên hệ thống", va="center", fontsize=8.5, fontweight="bold", color="#14261E")

    plt.tight_layout(pad=0.2)
    out = os.path.join(OUT_DIR, "slide_fig_resource_map.png")
    plt.savefig(out, bbox_inches="tight", transparent=False, facecolor="#FFFFFF")
    plt.close()
    print("Saved", out)


def _lane(ax, x, y, w, h, label, bg, hdr_bg, ec="#CBD5E1"):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=bg, edgecolor=ec, linewidth=1.4, zorder=1))
    hw = 0.042
    ax.add_patch(Rectangle((x, y), hw, h, facecolor=hdr_bg, edgecolor=ec, linewidth=1.4, zorder=2))
    ax.text(x + hw / 2, y + h / 2, label, ha="center", va="center",
            rotation=90, fontsize=8.5, fontweight="bold", color="#0F3D2E", zorder=3)


def _task(ax, cx, cy, w, h, text, fc="#FFFFFF", ec="#15803D", fs=8.1):
    box = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="round,pad=0.005,rounding_size=0.012",
        facecolor=fc, edgecolor=ec, linewidth=1.6, zorder=4
    )
    ax.add_patch(box)
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs,
            color="#14261E", fontweight="bold", linespacing=1.22, zorder=5)


def _event(ax, cx, cy, r, kind="start", label="", pos="bottom"):
    if kind == "start":
        ax.add_patch(Circle((cx, cy), r, facecolor="#ECFDF5", edgecolor="#15803D", linewidth=1.8, zorder=5))
    elif kind in ("catch", "timer"):
        ax.add_patch(Circle((cx, cy), r, facecolor="#FFFBEB", edgecolor="#D97706", linewidth=1.5, zorder=6))
        ax.add_patch(Circle((cx, cy), r * 0.74, facecolor="#FFFBEB", edgecolor="#D97706", linewidth=1.1, zorder=6))
        if kind == "timer":
            ax.plot([cx, cx], [cy, cy + r * 0.45], color="#B45309", lw=1.4, zorder=7)
            ax.plot([cx, cx + r * 0.35], [cy, cy], color="#B45309", lw=1.4, zorder=7)
        else:
            ew, eh = r * 0.76, r * 0.50
            ax.add_patch(Rectangle((cx - ew / 2, cy - eh / 2), ew, eh, facecolor="none", edgecolor="#B45309", lw=1.2, zorder=7))
            ax.plot([cx - ew / 2, cx, cx + ew / 2], [cy + eh / 2, cy - eh * 0.1, cy + eh / 2], color="#B45309", lw=1.1, zorder=7)
    elif kind == "end_ok":
        ax.add_patch(Circle((cx, cy), r, facecolor="#D1FAE5", edgecolor="#0F3D2E", linewidth=2.6, zorder=5))
    elif kind == "end_fail":
        ax.add_patch(Circle((cx, cy), r, facecolor="#FFEDD5", edgecolor="#C2410C", linewidth=2.6, zorder=5))

    if label:
        dy = -r - 0.023 if pos == "bottom" else r + 0.022
        ax.text(cx, cy + dy, label, ha="center", va="center", fontsize=7.4,
                color="#14261E", fontweight="bold", linespacing=1.15, zorder=7)


def _gw(ax, cx, cy, r, label="", pos="top"):
    pts = [(cx, cy + r), (cx + r * 0.76, cy), (cx, cy - r), (cx - r * 0.76, cy)]
    ax.add_patch(Polygon(pts, closed=True, facecolor="#FEF3C7", edgecolor="#D97706", linewidth=1.6, zorder=5))
    ax.text(cx, cy, "×", ha="center", va="center", fontsize=11.5, fontweight="bold", color="#92400E", zorder=6)
    if label:
        dy = r + 0.021 if pos == "top" else -r - 0.021
        ax.text(cx, cy + dy, label, ha="center", va="center", fontsize=7.4,
                color="#92400E", fontweight="bold", zorder=7)


def _flow(ax, x1, y1, x2, y2, label="", msg=False, color=None, rad=0.0, lx=0.0, ly=0.0):
    if color is None:
        color = "#D97706" if msg else "#14261E"
    ls = "--" if msg else "-"
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.45, linestyle=ls,
                        connectionstyle=f"arc3,rad={rad}"),
        zorder=4 if not msg else 6
    )
    if label:
        mx, my = (x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly
        ax.text(mx, my, label, ha="center", va="center", fontsize=7.2,
                color=color, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.14", fc="#FFFFFF", ec="none", alpha=0.94),
                zorder=8)


def _callout(ax, x, y, w, h, text, tx, ty, fc="#FFF7ED", ec="#EA580C", tc="#C2410C"):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.005,rounding_size=0.010",
        facecolor=fc, edgecolor=ec, linewidth=1.5, linestyle="-", zorder=8
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=7.5, color=tc, fontweight="bold", linespacing=1.18, zorder=9)
    ax.plot([x + w / 2, tx], [y + h if ty > y + h else y, ty], color=ec, linestyle=":", linewidth=1.4, zorder=7)


def render_slide_bpmn_as_is():
    fig, ax = plt.subplots(figsize=(15.0, 7.1), dpi=260)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    _lane(ax, 0.01, 0.80, 0.98, 0.17, "PHỤ HUYNH\n& HỌC VIÊN", "#FFFBEB", "#FDE68A")
    _lane(ax, 0.01, 0.59, 0.98, 0.18, "CSKH\n(CatPlus)", "#FEFCE8", "#FEF08A")
    _lane(ax, 0.01, 0.39, 0.98, 0.20, "QUẢN LÝ\nHỌC VỤ", "#FFF7ED", "#FED7AA")
    _lane(ax, 0.01, 0.22, 0.98, 0.17, "HỆ THỐNG\nPHẦN MỀM", "#F7F9F8", "#DAE2DE")
    _lane(ax, 0.01, 0.03, 0.98, 0.16, "GIA SƯ", "#ECFDF5", "#A7F3D0")

    # Pool 1
    _event(ax, 0.08, 0.88, 0.016, "start", "Đăng ký")
    _task(ax, 0.175, 0.88, 0.105, 0.070, "Gửi thông tin\nđăng ký học", "#FFFFFF", "#F59E0B")
    _event(ax, 0.275, 0.88, 0.015, "catch", "Nhận gọi", pos="top")
    _task(ax, 0.38, 0.88, 0.12, 0.070, "Báo mục tiêu &\n1 khung giờ đầu", "#FFFFFF", "#F59E0B")
    _event(ax, 0.565, 0.88, 0.015, "catch", "Báo lệch lịch", pos="top")
    _task(ax, 0.68, 0.88, 0.12, 0.070, "Chọn giờ khác\nhoặc hủy chờ", "#FFF7ED", "#EA580C")
    _event(ax, 0.84, 0.88, 0.015, "catch", "Nhận lịch", pos="top")
    _event(ax, 0.935, 0.88, 0.016, "end_ok", "Vào học")

    for x1, x2 in [(0.096, 0.122), (0.228, 0.260), (0.290, 0.320), (0.440, 0.550),
                   (0.580, 0.620), (0.740, 0.825), (0.855, 0.919)]:
        _flow(ax, x1, 0.88, x2, 0.88)

    # Pool 2
    _event(ax, 0.10, 0.68, 0.015, "catch", "Hồ sơ mới", pos="top")
    _task(ax, 0.16, 0.305, 0.12, 0.070, "Tạo hồ sơ chờ\ntrên hệ thống", "#FFFFFF", "#52665D")
    _task(ax, 0.31, 0.68, 0.13, 0.072, "Tư vấn & chỉ hỏi\n1 khung giờ đầu", "#FFFFFF", "#D97706")
    _event(ax, 0.258, 0.644, 0.012, "timer", "")
    _event(ax, 0.21, 0.625, 0.013, "end_fail", "Quá 24h")

    _task(ax, 0.32, 0.485, 0.135, 0.072, "Dò lịch tay FCFS\n& nhắn hỏi Gia sư", "#FFF7ED", "#EA580C")
    _event(ax, 0.445, 0.485, 0.015, "catch", "Chờ Zalo", pos="top")
    _event(ax, 0.460, 0.452, 0.011, "timer", "")
    _gw(ax, 0.545, 0.485, 0.024, "Đủ nhóm 3–5?", pos="top")
    _gw(ax, 0.645, 0.485, 0.023, "Quá 2 vòng?", pos="bottom")

    _task(ax, 0.645, 0.68, 0.125, 0.072, "Gọi lại phụ huynh\nxin đổi giờ khác", "#FFF7ED", "#EA580C")
    _gw(ax, 0.755, 0.68, 0.022, "Đổi giờ?")

    _task(ax, 0.765, 0.50, 0.115, 0.068, "Tạo lớp học thử\n/ chính thức", "#ECFDF5", "#15803D")
    _task(ax, 0.725, 0.305, 0.12, 0.070, "Cập nhật\nĐã tham gia", "#ECFDF5", "#15803D")
    _task(ax, 0.855, 0.68, 0.11, 0.070, "Báo lịch chốt\nphụ huynh", "#ECFDF5", "#15803D")
    _event(ax, 0.945, 0.68, 0.016, "end_ok", "Nhập học")

    _task(ax, 0.87, 0.305, 0.11, 0.070, "Đóng hồ sơ\n(Rớt lớp)", "#FFF7ED", "#C2410C")
    _event(ax, 0.955, 0.305, 0.015, "end_fail", "Thất bại")

    # Flows Pool 2 (zero crossing lines!)
    _flow(ax, 0.10, 0.664, 0.135, 0.340)
    _flow(ax, 0.19, 0.340, 0.255, 0.648)
    _flow(ax, 0.246, 0.640, 0.223, 0.628, color="#C2410C")
    _flow(ax, 0.315, 0.644, 0.315, 0.521, "Handoff", lx=0.036, color="#C2410C")
    _flow(ax, 0.388, 0.485, 0.430, 0.485)
    _flow(ax, 0.460, 0.485, 0.521, 0.485)
    _flow(ax, 0.569, 0.485, 0.622, 0.485, "Không", ly=0.016, color="#C2410C")
    _flow(ax, 0.545, 0.509, 0.707, 0.509, "Khớp lịch", lx=0.032, ly=0.015, color="#15803D")
    _flow(ax, 0.645, 0.508, 0.645, 0.644, "< 2 vòng", lx=-0.034, color="#EA580C")
    _flow(ax, 0.668, 0.485, 0.83, 0.340, "≥ 2 vòng", color="#C2410C", lx=0.025, ly=-0.02)
    _flow(ax, 0.708, 0.68, 0.733, 0.68)
    # Clean Rework arc above Pool 2 middle lane without hitting gateway text
    _flow(ax, 0.755, 0.702, 0.35, 0.521, "Lặp lại dò lịch (Rework)", rad=0.22, color="#EA580C", lx=-0.03, ly=0.068)
    _flow(ax, 0.777, 0.68, 0.87, 0.340, "Hủy", color="#C2410C", lx=0.028, ly=0.03)
    _flow(ax, 0.460, 0.440, 0.635, 0.468, "Quá 8h", rad=0.18, color="#B45309", ly=-0.026)
    _flow(ax, 0.765, 0.466, 0.725, 0.340, color="#15803D")
    _flow(ax, 0.755, 0.340, 0.835, 0.645, color="#15803D")
    _flow(ax, 0.910, 0.68, 0.929, 0.68, color="#15803D")
    _flow(ax, 0.925, 0.305, 0.940, 0.305, color="#C2410C")

    # Pool 3
    _event(ax, 0.32, 0.11, 0.015, "catch", "Tin nhắn hỏi")
    _task(ax, 0.445, 0.11, 0.135, 0.070, "Xem lịch cá nhân\n& trả lời qua Zalo", "#FFFFFF", "#15803D")
    _event(ax, 0.57, 0.11, 0.015, "end_ok", "Đã báo")
    _flow(ax, 0.335, 0.11, 0.377, 0.11)
    _flow(ax, 0.513, 0.11, 0.555, 0.11)

    # Message flows
    _flow(ax, 0.145, 0.845, 0.10, 0.696, "Đăng ký", msg=True, lx=-0.028)
    _flow(ax, 0.285, 0.716, 0.275, 0.864, "Gọi tư vấn", msg=True, lx=-0.030)
    _flow(ax, 0.38, 0.845, 0.335, 0.716, "1 khung giờ", msg=True, lx=0.035)
    _flow(ax, 0.32, 0.449, 0.32, 0.126, "Hỏi Zalo", msg=True, lx=-0.032)
    _flow(ax, 0.445, 0.145, 0.445, 0.469, "Báo rảnh/bận", msg=True, lx=-0.046)
    _flow(ax, 0.625, 0.716, 0.565, 0.864, "Xin đổi giờ", msg=True, lx=-0.030)
    _flow(ax, 0.68, 0.845, 0.668, 0.716, "Giờ mới/Hủy", msg=True, lx=0.038)
    _flow(ax, 0.855, 0.715, 0.84, 0.864, "Lịch chốt", msg=True, lx=0.034)

    # Diagnostic badges placed in clean open lane areas!
    _callout(ax, 0.065, 0.445, 0.175, 0.095,
             "ĐIỂM NGHẼN XẾP TAY\nXếp lẻ từng ca; nhóm < 3 em\nkhông đủ điều kiện mở lớp",
             0.252, 0.485)
    _callout(ax, 0.48, 0.255, 0.175, 0.095,
             "CHỜ ĐỢI & LÀM LẠI\nChờ Zalo gia sư 2,5–7,5h;\ngọi hỏi đổi lịch nhiều vòng",
             0.46, 0.470)

    plt.tight_layout(pad=0.15)
    out = os.path.join(OUT_DIR, "slide_fig_bpmn_as_is.png")
    plt.savefig(out, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close()
    print("Saved", out)


def render_slide_bpmn_to_be():
    fig, ax = plt.subplots(figsize=(15.0, 5.5), dpi=260)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    _lane(ax, 0.01, 0.79, 0.98, 0.18, "PHỤ HUYNH\n& HỌC VIÊN", "#FFFBEB", "#FDE68A")
    _lane(ax, 0.01, 0.58, 0.98, 0.19, "CSKH", "#FEFCE8", "#FEF08A")
    _lane(ax, 0.01, 0.38, 0.98, 0.20, "QUẢN LÝ\nHỌC VỤ", "#ECFDF5", "#A7F3D0")
    _lane(ax, 0.01, 0.19, 0.98, 0.19, "HỆ THỐNG\n+ MILP", "#ECFDF5", "#6EE7B7")
    _lane(ax, 0.01, 0.02, 0.98, 0.15, "GIA SƯ", "#F7F9F8", "#DAE2DE")

    # Pool 1
    _event(ax, 0.08, 0.875, 0.017, "start", "Đăng ký")
    _task(ax, 0.195, 0.875, 0.115, 0.082, "Gửi thông tin\nđăng ký học", "#FFFFFF", "#F59E0B")
    _event(ax, 0.315, 0.875, 0.016, "catch", "Nhận gọi", pos="top")
    _task(ax, 0.465, 0.875, 0.16, 0.082, "Cung cấp 1–3 khung giờ\nrảnh theo thứ tự ưu tiên", "#FFFBEB", "#D97706")
    _event(ax, 0.835, 0.875, 0.016, "catch", "Nhận lịch (1 vòng)", pos="top")
    _event(ax, 0.94, 0.875, 0.017, "end_ok", "Vào học")

    for x1, x2 in [(0.097, 0.137), (0.253, 0.299), (0.331, 0.385), (0.545, 0.819), (0.851, 0.923)]:
        _flow(ax, x1, 0.875, x2, 0.875)

    # Pool 2
    _event(ax, 0.11, 0.675, 0.016, "catch", "Hồ sơ mới")
    _task(ax, 0.345, 0.675, 0.155, 0.084, "Tư vấn & nhập chuẩn\n1–3 khung giờ ưu tiên", "#FFFBEB", "#D97706")
    _task(ax, 0.465, 0.285, 0.18, 0.088, "Chạy MILP 2 đợt/ngày:\nGom nhóm 3–5 & gợi ý", "#D1FAE5", "#0F3D2E")
    _task(ax, 0.65, 0.48, 0.16, 0.084, "Quản lý xem bảng gợi ý\n& duyệt 1 vòng (+dự phòng)", "#ECFDF5", "#15803D")
    _task(ax, 0.835, 0.675, 0.13, 0.082, "Báo lịch chốt\ncho phụ huynh", "#ECFDF5", "#15803D")
    _event(ax, 0.945, 0.675, 0.017, "end_ok", "Nhập học\n92,7%")

    # Pool 3
    _task(ax, 0.23, 0.095, 0.175, 0.078, "Cập nhật bảng ca trống\ncố định hằng tuần", "#FFFFFF", "#15803D")
    _event(ax, 0.65, 0.095, 0.016, "catch", "Nhận lịch dạy")
    _event(ax, 0.77, 0.095, 0.016, "end_ok", "Xác nhận")
    _flow(ax, 0.666, 0.095, 0.754, 0.095, color="#15803D")

    # Flows
    _flow(ax, 0.126, 0.675, 0.267, 0.675)
    _flow(ax, 0.39, 0.633, 0.435, 0.329, "Đưa vào đợt chạy", lx=0.056, color="#0F3D2E")
    _flow(ax, 0.555, 0.285, 0.61, 0.438, "Đề xuất tối ưu", lx=0.052, color="#15803D")
    _flow(ax, 0.73, 0.48, 0.80, 0.634, "Đã duyệt", lx=0.042, color="#15803D")
    _flow(ax, 0.90, 0.675, 0.928, 0.675, color="#15803D")

    # Message flows
    _flow(ax, 0.165, 0.834, 0.11, 0.691, "Đăng ký", msg=True, lx=-0.025)
    _flow(ax, 0.315, 0.717, 0.315, 0.858, "Gọi tư vấn", msg=True, lx=-0.034)
    _flow(ax, 0.465, 0.834, 0.395, 0.717, "1–3 khung giờ", msg=True, lx=0.045)
    _flow(ax, 0.275, 0.134, 0.385, 0.241, "Đồng bộ ca trống", msg=True, lx=-0.055, color="#15803D")
    _flow(ax, 0.65, 0.438, 0.65, 0.112, "Giao lớp", msg=True, lx=0.036, color="#15803D")
    _flow(ax, 0.835, 0.716, 0.835, 0.858, "Báo lịch chốt", msg=True, lx=0.044, color="#15803D")

    _callout(ax, 0.08, 0.42, 0.22, 0.11,
             "XÓA BỎ VÒNG LẶP HỎI LẠI\nLịch trống đồng bộ đầu tuần +\nMILP gom cụm nhóm 3–5 học viên",
             0.375, 0.295, fc="#ECFDF5", ec="#15803D", tc="#0F3D2E")

    plt.tight_layout(pad=0.15)
    out = os.path.join(OUT_DIR, "slide_fig_bpmn_to_be.png")
    plt.savefig(out, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close()
    print("Saved", out)


if __name__ == "__main__":
    render_slide_resource_map()
    render_slide_bpmn_as_is()
    render_slide_bpmn_to_be()
