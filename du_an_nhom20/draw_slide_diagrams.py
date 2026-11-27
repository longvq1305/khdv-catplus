"""
Projector-optimized diagrams for normal classroom projectors:
  - Exact frame aspect ratios so PowerPoint never shrinks them horizontally
  - Large bold fonts (11.5pt - 14pt), minimal keywords (2-5 words per box)
  - High-contrast thick borders (2.2pt - 2.6pt) in Green - Amber - Orange
"""

import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, Rectangle

plt.rcParams["font.sans-serif"] = ["Arial", "Segoe UI", "DejaVu Sans"]
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def _box(ax, x, y, w, h, title, body, fc, ec, tc, lw=2.3, t_fs=12.5, b_fs=11.0):
    b = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.010,rounding_size=0.022",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3
    )
    ax.add_patch(b)
    ax.text(x + w / 2, y + h - 0.030, title, ha="center", va="top",
            fontsize=t_fs, fontweight="bold", color=tc, zorder=4)
    ax.text(x + w / 2, y + h - 0.088, body, ha="center", va="top",
            fontsize=b_fs, fontweight="bold", color="#14261E", linespacing=1.42, zorder=4)


def _arr(ax, x1, y1, x2, y2, label="", color="#15803D", ls="-", lx=0.0, ly=0.0, fs=10.5):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=2.4, linestyle=ls),
        zorder=5
    )
    if label:
        mx, my = (x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly
        ax.text(mx, my, label, ha="center", va="center", fontsize=fs,
                color=color, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.20", fc="#FFFFFF", ec="none", alpha=0.96),
                zorder=6)


def render_slide_resource_map():
    # Aspect ratio 8.15 : 5.25 -> figsize=(10.6, 6.8)
    fig, ax = plt.subplots(figsize=(10.6, 6.8), dpi=240)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    boundary = FancyBboxPatch(
        (0.015, 0.13), 0.97, 0.84,
        boxstyle="round,pad=0.01,rounding_size=0.022",
        facecolor="#F8FBF9", edgecolor="#0F3D2E", linewidth=2.6, linestyle="--", zorder=1
    )
    ax.add_patch(boundary)
    ax.text(0.035, 0.955, "RANH GIỚI HỆ THỐNG CATPLUS",
            ha="left", va="top", fontsize=11.5, fontweight="bold", color="#0F3D2E", zorder=2)
    ax.text(0.965, 0.955, "Ngoài biên: Zalo/ĐT, Mạng, Thi HSG",
            ha="right", va="top", fontsize=10.2, style="italic", fontweight="bold", color="#52665D", zorder=2)

    # 1. Học viên & Phụ huynh
    _box(ax, 0.035, 0.46, 0.265, 0.42,
         "HỌC VIÊN & PHỤ HUYNH",
         "• 1–3 khung giờ rảnh\n• Cấp THCS / THPT\n• Lớp 1–1 / Nhóm 3–5\n• Rủi ro: Chờ lâu bỏ đi",
         fc="#FFFBEB", ec="#D97706", tc="#B45309")

    # 2. CSKH
    _box(ax, 0.365, 0.66, 0.27, 0.23,
         "CSKH (2 người)",
         "• Tư vấn & lấy khung giờ\n• Báo lịch chốt lớp",
         fc="#FEFCE8", ec="#D97706", tc="#92400E")

    # 3. Quản lý học vụ
    _box(ax, 0.365, 0.38, 0.27, 0.21,
         "QUẢN LÝ (1 người)",
         "• Điều phối nhóm 3–5 em\n• Duyệt lịch cuối cùng",
         fc="#ECFDF5", ec="#15803D", tc="#0F3D2E")

    # 4. Nền tảng CatPlus
    _box(ax, 0.365, 0.155, 0.27, 0.16,
         "PHẦN MỀM + MILP",
         "• Lưu hồ sơ & quy tắc lớp\n• Gợi ý tối ưu 2 đợt/ngày",
         fc="#FFF7ED", ec="#EA580C", tc="#C2410C", t_fs=11.8, b_fs=10.4)

    # 5. Gia sư
    _box(ax, 0.70, 0.46, 0.265, 0.42,
         "GIA SƯ (10 người)",
         "• Chuyên môn lập trình\n• Trống 5–7 ca / tuần\n• Tối đa 3–5 lớp\n• Rủi ro: Bận đột xuất",
         fc="#ECFDF5", ec="#15803D", tc="#14532D")

    # 6. Đồng tạo giá trị
    _box(ax, 0.035, 0.155, 0.265, 0.23,
         "ĐỒNG TẠO GIÁ TRỊ",
         "• Tích hợp lịch trò – thầy\n• Vào lớp nhanh, đúng ca",
         fc="#D1FAE5", ec="#0F3D2E", tc="#0F3D2E", t_fs=11.8, b_fs=10.5)

    # Arrows
    _arr(ax, 0.30, 0.79, 0.365, 0.79, "Báo giờ", color="#B45309", ly=0.042)
    _arr(ax, 0.365, 0.71, 0.30, 0.71, "Chốt lớp", color="#15803D", ly=-0.042)
    _arr(ax, 0.43, 0.66, 0.43, 0.59, "Giao ca", color="#0F3D2E", lx=-0.058)
    _arr(ax, 0.55, 0.59, 0.55, 0.66, "Đổi / Duyệt", color="#EA580C", ls="--", lx=0.066)
    _arr(ax, 0.45, 0.38, 0.45, 0.315, "Dữ liệu", color="#C2410C", lx=-0.055)
    _arr(ax, 0.55, 0.315, 0.55, 0.38, "Gợi ý", color="#15803D", ls=":", lx=0.052)
    _arr(ax, 0.635, 0.54, 0.70, 0.70, "Giao lớp", color="#15803D", lx=0.025, ly=0.052)
    _arr(ax, 0.70, 0.56, 0.635, 0.44, "Xác nhận", color="#EA580C", ls="--", lx=0.038, ly=-0.045)
    _arr(ax, 0.168, 0.46, 0.168, 0.385, "Học tập", color="#0F3D2E", lx=0.062)

    # Legend
    leg = FancyBboxPatch(
        (0.015, 0.015), 0.97, 0.09,
        boxstyle="round,pad=0.008,rounding_size=0.015",
        facecolor="#FFFFFF", edgecolor="#94A3B8", linewidth=1.6, zorder=2
    )
    ax.add_patch(leg)
    ax.plot([0.04, 0.09], [0.06, 0.06], color="#15803D", lw=2.8)
    ax.text(0.10, 0.06, "Luồng chính", va="center", fontsize=10.5, fontweight="bold", color="#14261E")

    ax.plot([0.33, 0.38], [0.06, 0.06], color="#EA580C", lw=2.8, linestyle="--")
    ax.text(0.39, 0.06, "Phản hồi / Đổi lịch", va="center", fontsize=10.5, fontweight="bold", color="#14261E")

    ax.plot([0.67, 0.72], [0.06, 0.06], color="#15803D", lw=2.8, linestyle=":")
    ax.text(0.73, 0.06, "Gợi ý MILP (TO-BE)", va="center", fontsize=10.5, fontweight="bold", color="#14261E")

    plt.tight_layout(pad=0.15)
    out = os.path.join(OUT_DIR, "slide_fig_resource_map.png")
    plt.savefig(out, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close()
    print("Saved", out)


def _lane(ax, x, y, w, h, label, bg, hdr_bg):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=bg, edgecolor="#94A3B8", linewidth=1.6, zorder=1))
    hw = 0.048
    ax.add_patch(Rectangle((x, y), hw, h, facecolor=hdr_bg, edgecolor="#94A3B8", linewidth=1.6, zorder=2))
    ax.text(x + hw / 2, y + h / 2, label, ha="center", va="center",
            rotation=90, fontsize=10.2, fontweight="bold", color="#0F3D2E", zorder=3)


def _task(ax, cx, cy, w, h, text, fc="#FFFFFF", ec="#15803D", fs=10.2):
    box = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="round,pad=0.005,rounding_size=0.014",
        facecolor=fc, edgecolor=ec, linewidth=2.1, zorder=4
    )
    ax.add_patch(box)
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs,
            color="#14261E", fontweight="bold", linespacing=1.22, zorder=5)


def _ev(ax, cx, cy, r, kind="start", label="", pos="bottom"):
    if kind == "start":
        ax.add_patch(Circle((cx, cy), r, facecolor="#D1FAE5", edgecolor="#15803D", linewidth=2.2, zorder=5))
    elif kind in ("catch", "timer"):
        ax.add_patch(Circle((cx, cy), r, facecolor="#FFFBEB", edgecolor="#D97706", linewidth=1.8, zorder=6))
        ax.add_patch(Circle((cx, cy), r * 0.72, facecolor="#FFFBEB", edgecolor="#D97706", linewidth=1.3, zorder=6))
        if kind == "timer":
            ax.plot([cx, cx], [cy, cy + r * 0.45], color="#B45309", lw=1.6, zorder=7)
            ax.plot([cx, cx + r * 0.35], [cy, cy], color="#B45309", lw=1.6, zorder=7)
        else:
            ew, eh = r * 0.76, r * 0.50
            ax.add_patch(Rectangle((cx - ew / 2, cy - eh / 2), ew, eh, facecolor="none", edgecolor="#B45309", lw=1.4, zorder=7))
            ax.plot([cx - ew / 2, cx, cx + ew / 2], [cy + eh / 2, cy - eh * 0.1, cy + eh / 2], color="#B45309", lw=1.3, zorder=7)
    elif kind == "end_ok":
        ax.add_patch(Circle((cx, cy), r, facecolor="#A7F3D0", edgecolor="#0F3D2E", linewidth=3.0, zorder=5))
    elif kind == "end_fail":
        ax.add_patch(Circle((cx, cy), r, facecolor="#FED7AA", edgecolor="#C2410C", linewidth=3.0, zorder=5))

    if label:
        dy = -r - 0.028 if pos == "bottom" else r + 0.026
        ax.text(cx, cy + dy, label, ha="center", va="center", fontsize=9.2,
                color="#14261E", fontweight="bold", zorder=7)


def _gw(ax, cx, cy, r, label="", pos="top"):
    pts = [(cx, cy + r), (cx + r * 0.76, cy), (cx, cy - r), (cx - r * 0.76, cy)]
    ax.add_patch(Polygon(pts, closed=True, facecolor="#FEF08A", edgecolor="#D97706", linewidth=2.0, zorder=5))
    ax.text(cx, cy, "×", ha="center", va="center", fontsize=13, fontweight="bold", color="#92400E", zorder=6)
    if label:
        dy = r + 0.025 if pos == "top" else -r - 0.025
        ax.text(cx, cy + dy, label, ha="center", va="center", fontsize=9.2,
                color="#92400E", fontweight="bold", zorder=7)


def _fl(ax, x1, y1, x2, y2, label="", msg=False, color=None, rad=0.0, lx=0.0, ly=0.0):
    if color is None:
        color = "#D97706" if msg else "#14261E"
    ls = "--" if msg else "-"
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.9, linestyle=ls,
                        connectionstyle=f"arc3,rad={rad}"),
        zorder=4 if not msg else 6
    )
    if label:
        mx, my = (x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly
        ax.text(mx, my, label, ha="center", va="center", fontsize=9.0,
                color=color, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.15", fc="#FFFFFF", ec="none", alpha=0.95),
                zorder=8)


def render_slide_bpmn_as_is():
    # Exact frame ratio 11.9 : 4.55 -> figsize=(15.6, 5.95) so ZERO horizontal shrinking!
    fig, ax = plt.subplots(figsize=(15.6, 5.95), dpi=240)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    _lane(ax, 0.008, 0.80, 0.984, 0.18, "PHỤ HUYNH", "#FFFBEB", "#FDE68A")
    _lane(ax, 0.008, 0.59, 0.984, 0.19, "CSKH", "#FEFCE8", "#FEF08A")
    _lane(ax, 0.008, 0.38, 0.984, 0.21, "QUẢN LÝ", "#FFF7ED", "#FED7AA")
    _lane(ax, 0.008, 0.20, 0.984, 0.18, "HỆ THỐNG", "#F8FAFC", "#CBD5E1")
    _lane(ax, 0.008, 0.02, 0.984, 0.16, "GIA SƯ", "#ECFDF5", "#A7F3D0")

    # Pool 1
    _ev(ax, 0.085, 0.885, 0.018, "start", "Đăng ký")
    _task(ax, 0.19, 0.885, 0.115, 0.088, "Gửi đăng ký", "#FFFFFF", "#D97706")
    _ev(ax, 0.30, 0.885, 0.017, "catch", "Nghe gọi", pos="top")
    _task(ax, 0.42, 0.885, 0.135, 0.088, "Báo 1 ca rảnh", "#FFFFFF", "#D97706")
    _ev(ax, 0.585, 0.885, 0.017, "catch", "Lệch lịch", pos="top")
    _task(ax, 0.705, 0.885, 0.13, 0.088, "Đổi giờ / Hủy", "#FFF7ED", "#EA580C")
    _ev(ax, 0.845, 0.885, 0.017, "catch", "Nhận lịch", pos="top")
    _ev(ax, 0.94, 0.885, 0.018, "end_ok", "Vào học")

    for x1, x2 in [(0.103, 0.132), (0.248, 0.283), (0.317, 0.352), (0.488, 0.568),
                   (0.602, 0.640), (0.770, 0.828), (0.862, 0.922)]:
        _fl(ax, x1, 0.885, x2, 0.885)

    # Pool 2
    _ev(ax, 0.11, 0.685, 0.017, "catch", "Hồ sơ mới", pos="top")
    _task(ax, 0.17, 0.29, 0.13, 0.088, "Lưu hồ sơ chờ", "#FFFFFF", "#475569")
    _task(ax, 0.335, 0.685, 0.145, 0.090, "Hỏi 1 khung giờ", "#FFFFFF", "#D97706")

    _task(ax, 0.335, 0.485, 0.155, 0.092, "Dò lịch tay &\nnhắn hỏi Zalo", "#FFF7ED", "#EA580C")
    _ev(ax, 0.465, 0.485, 0.017, "catch", "Chờ Zalo", pos="top")
    _ev(ax, 0.482, 0.448, 0.013, "timer", "")
    _gw(ax, 0.56, 0.485, 0.028, "Đủ 3–5 em?", pos="top")
    _gw(ax, 0.66, 0.485, 0.027, "≥ 2 vòng?", pos="bottom")

    _task(ax, 0.66, 0.685, 0.14, 0.090, "Gọi xin đổi giờ", "#FFF7ED", "#EA580C")
    _task(ax, 0.775, 0.495, 0.125, 0.086, "Mở lớp học", "#ECFDF5", "#15803D")
    _task(ax, 0.73, 0.29, 0.13, 0.086, "Đã tham gia", "#ECFDF5", "#15803D")
    _task(ax, 0.855, 0.685, 0.115, 0.086, "Báo lịch chốt", "#ECFDF5", "#15803D")
    _ev(ax, 0.948, 0.685, 0.018, "end_ok", "Thành công")

    _task(ax, 0.875, 0.29, 0.115, 0.086, "Rớt lớp\n(39,6%)", "#FFF7ED", "#C2410C")
    _ev(ax, 0.958, 0.29, 0.017, "end_fail", "")

    # Flows Pool 2
    _fl(ax, 0.11, 0.667, 0.145, 0.334)
    _fl(ax, 0.20, 0.334, 0.275, 0.640)
    _fl(ax, 0.335, 0.640, 0.335, 0.531, "Handoff", lx=0.042, color="#C2410C")
    _fl(ax, 0.413, 0.485, 0.448, 0.485)
    _fl(ax, 0.482, 0.485, 0.532, 0.485)
    _fl(ax, 0.588, 0.485, 0.633, 0.485, "Không", ly=0.020, color="#C2410C")
    _fl(ax, 0.56, 0.513, 0.712, 0.513, "Đủ", lx=0.035, ly=0.018, color="#15803D")
    _fl(ax, 0.66, 0.512, 0.66, 0.640, "< 2", lx=-0.026, color="#EA580C")
    _fl(ax, 0.687, 0.485, 0.835, 0.333, "≥ 2 vòng", color="#C2410C", lx=0.025, ly=-0.022)
    _fl(ax, 0.59, 0.685, 0.365, 0.531, "Làm lại (Rework)", rad=0.18, color="#EA580C", lx=-0.02, ly=0.052)
    _fl(ax, 0.482, 0.435, 0.648, 0.468, "Quá 8h", rad=0.18, color="#B45309", ly=-0.032)
    _fl(ax, 0.775, 0.452, 0.73, 0.333, color="#15803D")
    _fl(ax, 0.76, 0.333, 0.835, 0.642, color="#15803D")
    _fl(ax, 0.913, 0.685, 0.930, 0.685, color="#15803D")
    _fl(ax, 0.933, 0.29, 0.941, 0.29, color="#C2410C")

    # Pool 3
    _ev(ax, 0.335, 0.10, 0.017, "catch", "Tin Zalo")
    _task(ax, 0.465, 0.10, 0.145, 0.086, "Xem lịch &\ntrả lời Zalo", "#FFFFFF", "#15803D")
    _ev(ax, 0.595, 0.10, 0.017, "end_ok", "Đã báo")
    _fl(ax, 0.352, 0.10, 0.392, 0.10)
    _fl(ax, 0.538, 0.10, 0.578, 0.10)

    # Message flows
    _fl(ax, 0.16, 0.841, 0.11, 0.703, msg=True)
    _fl(ax, 0.31, 0.730, 0.30, 0.867, msg=True)
    _fl(ax, 0.41, 0.841, 0.36, 0.730, "1 ca", msg=True, lx=0.030)
    _fl(ax, 0.335, 0.439, 0.335, 0.118, "Hỏi Zalo", msg=True, lx=-0.038)
    _fl(ax, 0.465, 0.143, 0.465, 0.467, "Trả lời", msg=True, lx=-0.038)
    _fl(ax, 0.64, 0.730, 0.585, 0.867, msg=True)
    _fl(ax, 0.705, 0.841, 0.685, 0.730, msg=True)
    _fl(ax, 0.855, 0.728, 0.845, 0.867, msg=True)

    # Bold high-contrast callout badge in open left area
    badge = FancyBboxPatch(
        (0.065, 0.43), 0.175, 0.115,
        boxstyle="round,pad=0.006,rounding_size=0.014",
        facecolor="#EA580C", edgecolor="#9A3412", linewidth=1.8, zorder=8
    )
    ax.add_patch(badge)
    ax.text(0.152, 0.487, "ĐIỂM NGHẼN CHÍNH\nNhóm lẻ 1–2 em bị kẹt;\nchờ Zalo 15,66 giờ",
            ha="center", va="center", fontsize=9.3, fontweight="bold", color="#FFFFFF", linespacing=1.22, zorder=9)

    plt.tight_layout(pad=0.12)
    out = os.path.join(OUT_DIR, "slide_fig_bpmn_as_is.png")
    plt.savefig(out, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close()
    print("Saved", out)


def render_slide_bpmn_to_be():
    # Exact frame ratio 11.9 : 3.85 -> figsize=(15.6, 5.05) so ZERO horizontal shrinking!
    fig, ax = plt.subplots(figsize=(15.6, 5.05), dpi=240)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    _lane(ax, 0.008, 0.79, 0.984, 0.19, "PHỤ HUYNH", "#FFFBEB", "#FDE68A")
    _lane(ax, 0.008, 0.58, 0.984, 0.19, "CSKH", "#FEFCE8", "#FEF08A")
    _lane(ax, 0.008, 0.38, 0.984, 0.20, "QUẢN LÝ", "#ECFDF5", "#A7F3D0")
    _lane(ax, 0.008, 0.19, 0.984, 0.19, "MILP", "#D1FAE5", "#6EE7B7")
    _lane(ax, 0.008, 0.02, 0.984, 0.15, "GIA SƯ", "#F8FAFC", "#CBD5E1")

    # Pool 1
    _ev(ax, 0.085, 0.88, 0.019, "start", "Đăng ký")
    _task(ax, 0.20, 0.88, 0.12, 0.096, "Gửi đăng ký", "#FFFFFF", "#D97706", fs=10.8)
    _ev(ax, 0.32, 0.88, 0.018, "catch", "Nghe gọi", pos="top")
    _task(ax, 0.475, 0.88, 0.17, 0.096, "Báo 1–3 khung giờ\ntheo ưu tiên", "#FFFBEB", "#D97706", fs=10.6)
    _ev(ax, 0.835, 0.88, 0.018, "catch", "Chốt 1 vòng", pos="top")
    _ev(ax, 0.94, 0.88, 0.019, "end_ok", "Vào học")

    for x1, x2 in [(0.104, 0.140), (0.260, 0.302), (0.338, 0.390), (0.560, 0.817), (0.853, 0.921)]:
        _fl(ax, x1, 0.88, x2, 0.88)

    # Pool 2
    _ev(ax, 0.115, 0.675, 0.018, "catch", "Hồ sơ mới")
    _task(ax, 0.35, 0.675, 0.165, 0.098, "Nhập chuẩn\n1–3 khung giờ", "#FFFBEB", "#D97706", fs=10.8)
    _task(ax, 0.475, 0.285, 0.195, 0.104, "Chạy MILP (11h30 & 17h30)\nGom nhóm 3–5 em", "#A7F3D0", "#0F3D2E", fs=10.6)
    _task(ax, 0.665, 0.48, 0.175, 0.098, "Duyệt bảng gợi ý\n1 vòng (+dự phòng)", "#ECFDF5", "#15803D", fs=10.6)
    _task(ax, 0.835, 0.675, 0.135, 0.096, "Báo lịch chốt", "#ECFDF5", "#15803D", fs=10.8)
    _ev(ax, 0.945, 0.675, 0.019, "end_ok", "92,7% đỗ")

    # Pool 3
    _task(ax, 0.23, 0.095, 0.185, 0.092, "Điền sẵn ca trống\nđầu tuần", "#FFFFFF", "#15803D", fs=10.4)
    _ev(ax, 0.665, 0.095, 0.018, "catch", "Nhận lớp")
    _ev(ax, 0.79, 0.095, 0.018, "end_ok", "Xác nhận")
    _fl(ax, 0.683, 0.095, 0.772, 0.095, color="#15803D")

    # Flows
    _fl(ax, 0.133, 0.675, 0.267, 0.675)
    _fl(ax, 0.395, 0.626, 0.445, 0.337, "Gom đợt", lx=0.048, color="#0F3D2E")
    _fl(ax, 0.573, 0.285, 0.625, 0.431, "Đề xuất", lx=0.045, color="#15803D")
    _fl(ax, 0.753, 0.48, 0.805, 0.627, "Duyệt", lx=0.038, color="#15803D")
    _fl(ax, 0.903, 0.675, 0.926, 0.675, color="#15803D")

    # Message flows
    _fl(ax, 0.17, 0.832, 0.115, 0.693, msg=True)
    _fl(ax, 0.32, 0.724, 0.32, 0.861, msg=True)
    _fl(ax, 0.475, 0.832, 0.40, 0.724, "1–3 ca", msg=True, lx=0.042)
    _fl(ax, 0.28, 0.141, 0.39, 0.235, "Ca trống", msg=True, lx=-0.048, color="#15803D")
    _fl(ax, 0.665, 0.431, 0.665, 0.114, "Giao lớp", msg=True, lx=0.040, color="#15803D")
    _fl(ax, 0.835, 0.723, 0.835, 0.861, msg=True, color="#15803D")

    badge = FancyBboxPatch(
        (0.08, 0.41), 0.22, 0.13,
        boxstyle="round,pad=0.006,rounding_size=0.014",
        facecolor="#0F3D2E", edgecolor="#0F3D2E", linewidth=1.8, zorder=8
    )
    ax.add_patch(badge)
    ax.text(0.19, 0.475, "XÓA BỎ VÒNG LẶP ZALO\nĐồng bộ lịch đầu tuần +\nMILP gom cụm 3–5 em",
            ha="center", va="center", fontsize=9.8, fontweight="bold", color="#FBBF24", linespacing=1.24, zorder=9)

    plt.tight_layout(pad=0.12)
    out = os.path.join(OUT_DIR, "slide_fig_bpmn_to_be.png")
    plt.savefig(out, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close()
    print("Saved", out)


if __name__ == "__main__":
    render_slide_resource_map()
    render_slide_bpmn_as_is()
    render_slide_bpmn_to_be()
