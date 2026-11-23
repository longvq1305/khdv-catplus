"""
Generate a crisp, rubric-compliant Resource Map (Bản đồ nguồn lực & đồng tạo giá trị)
for CatPlus Tutor-Student Matching & Scheduling Service System.
Meets all 5 criteria in INT3501 Rubric Section 6:
  (i) System boundary
  (ii) 3-5 resource types (Human/Pedagogical, Schedule/Time, Digital/Data, Institutional/Rules)
  (iii) Who contributes / uses resources
  (iv) Interactions & information/value flows
  (v) Benefits, costs, or risks for each side + Legend (Chú giải ký hiệu)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Segoe UI"]
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def draw_box(ax, x, y, w, h, title, body, fc="#EFF6FF", ec="#1D4ED8", lw=1.5, title_color="#1E3A8A"):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h - 0.022, title, ha="center", va="top",
            fontsize=8.7, fontweight="bold", color=title_color, zorder=4)
    ax.text(x + w / 2, y + h - 0.055, body, ha="center", va="top",
            fontsize=7.6, color="#1E293B", linespacing=1.35, zorder=4)


def draw_arrow(ax, x1, y1, x2, y2, label="", color="#334155", style="-|>", ls="-", rad=0.0, lx_off=0, ly_off=0):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle=style, color=color, lw=1.3, linestyle=ls,
                        connectionstyle=f"arc3,rad={rad}"),
        zorder=5
    )
    if label:
        mx, my = (x1 + x2) / 2 + lx_off, (y1 + y2) / 2 + ly_off
        ax.text(mx, my, label, ha="center", va="center", fontsize=7.2,
                color=color, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.85),
                zorder=6)


def main():
    fig, ax = plt.subplots(figsize=(14, 8.5), dpi=220)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Title
    ax.text(0.5, 0.985, "BẢN ĐỒ NGUỒN LỰC & ĐỒNG TẠO GIÁ TRỊ (RESOURCE MAP) — HỆ THỐNG DỊCH VỤ CATPLUS",
            ha="center", va="top", fontsize=11.8, fontweight="bold", color="#0F172A")
    ax.text(0.5, 0.953, "Phạm vi: Tiếp nhận, ghép đôi gia sư – học viên và xếp lịch học (Human-in-the-loop)",
            ha="center", va="top", fontsize=9, color="#475569")

    # System Boundary (i)
    boundary = FancyBboxPatch(
        (0.03, 0.14), 0.94, 0.76,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor="#F8FAFC", edgecolor="#0F172A", linewidth=2.0, linestyle="--", zorder=1
    )
    ax.add_patch(boundary)
    ax.text(0.045, 0.892, "RANH GIỚI HỆ THỐNG DỊCH VỤ CATPLUS (TRONG BIÊN PHÂN TÍCH)",
            ha="left", va="top", fontsize=8.3, fontweight="bold", color="#0F172A", zorder=2)

    # External Environment Box (Outside boundary bottom-right/top-right note)
    ax.text(0.955, 0.892, "Ngoài biên: Hạ tầng mạng, Zalo/ĐT, Kỳ thi HSG, Thị trường gia sư",
            ha="right", va="top", fontsize=7.6, style="italic", color="#64748B", zorder=2)

    # Actors & Contributed Resources (ii, iii, v)
    # 1. Học viên & Phụ huynh (Left)
    draw_box(
        ax, 0.055, 0.56, 0.24, 0.28,
        "1. HỌC VIÊN & PHỤ HUYNH (Người thụ hưởng)",
        "Nguồn lực đóng góp:\n"
        "• Thời gian & khung giờ rảnh cá nhân (Slot)\n"
        "• Trình độ đầu vào, mục tiêu thi đấu (THCS/THPT)\n"
        "• Thông tin phản hồi & học phí\n"
        "Lợi ích: Được ghép đúng gia sư, ít chờ đợi\n"
        "Chi phí/Rủi ro: Mất thời gian chờ; bỏ cuộc nếu lệch lịch",
        fc="#FEF3C7", ec="#D97706", title_color="#92400E"
    )

    # 2. CSKH (Top Center)
    draw_box(
        ax, 0.38, 0.65, 0.25, 0.20,
        "2. CHĂM SÓC KHÁCH HÀNG (CSKH)",
        "Nguồn lực đóng góp:\n"
        "• Kỹ năng giao tiếp, tư vấn & thuyết phục\n"
        "• Thời gian xử lý & theo dõi StudentJourney\n"
        "Lợi ích: Chốt đơn nhanh, giảm tải gọi lại\n"
        "Chi phí/Rủi ro: Quá tải khi phải hỏi lại nhiều vòng",
        fc="#E0F2FE", ec="#0284C4", title_color="#075985"
    )

    # 3. Quản lý học vụ (Center)
    draw_box(
        ax, 0.38, 0.39, 0.25, 0.20,
        "3. QUẢN LÝ HỌC VỤ (Điều phối chính)",
        "Nguồn lực đóng góp:\n"
        "• Tri thức phân loại năng lực & ghép lớp\n"
        "• Quyền điều phối lớp (1-1 / Nhóm 3-5) & duyệt lịch\n"
        "Lợi ích: Tối ưu tỷ lệ lấp đầy & giữ chân HV\n"
        "Chi phí/Rủi ro: Nút cổ chai (bottleneck) khi dò tay",
        fc="#DBEAFE", ec="#1D4ED8", title_color="#1E3A8A"
    )

    # 4. Nền tảng CatPlus (Bottom Center)
    draw_box(
        ax, 0.38, 0.165, 0.25, 0.175,
        "4. NỀN TẢNG CATPLUS (Dữ liệu & Quy tắc)",
        "Nguồn lực (Operand & Thiết chế):\n"
        "• DB StudentJourney, ClassScheduleRule, TrialSession\n"
        "• Quy tắc lớp (1-1 vs Nhóm 3-5), chính sách học thử\n"
        "• [TO-BE]: Module tối ưu hóa ILP gợi ý lịch\n"
        "Rủi ro: Dữ liệu lịch gia sư chưa cập nhật real-time",
        fc="#EDE9FE", ec="#6D28D9", title_color="#4C1D95"
    )

    # 5. Gia sư (Right)
    draw_box(
        ax, 0.705, 0.56, 0.24, 0.28,
        "5. GIA SƯ (Nhà cung ứng chuyên môn)",
        "Nguồn lực đóng góp:\n"
        "• Tri thức thuật toán & kỹ năng sư phạm (Operant)\n"
        "• Quỹ thời gian giảng dạy & số lớp tối đa (Capacity)\n"
        "Lợi ích: Thu nhập ổn định, lịch dạy hợp lý\n"
        "Chi phí/Rủi ro: Từ chối ca đột xuất; quá tải cục bộ",
        fc="#DCFCE7", ec="#15803D", title_color="#14532D"
    )

    # 6. Value Co-creation Hub (Bottom Left & Bottom Right)
    draw_box(
        ax, 0.055, 0.20, 0.24, 0.23,
        "CƠ CHẾ ĐỒNG TẠO GIÁ TRỊ",
        "1. Tích hợp nguồn lực: Lịch rảnh HV\n"
        "   + Năng lực CSKH/QL + Quỹ giờ Gia sư\n"
        "2. Output kỹ thuật: Lịch học thử (Trial)\n"
        "   & Lớp học (Class/Enrollment) được khớp\n"
        "3. Outcome dịch vụ: HV vào học đúng\n"
        "   trình độ, đúng lịch, thời gian chờ ngắn\n"
        "4. Value-in-context: Tiến bộ lập trình",
        fc="#FFF1F2", ec="#BE123C", title_color="#881337"
    )

    # Interaction & Flow Arrows (iv)
    # Customer <-> CSKH
    draw_arrow(ax, 0.295, 0.75, 0.38, 0.77, "Nhu cầu + Slot rảnh\n(Thông tin đầu vào)", color="#0369A1", ly_off=0.03)
    draw_arrow(ax, 0.38, 0.71, 0.295, 0.69, "Tư vấn & Chốt lịch", color="#0F766E", ly_off=-0.028)

    # CSKH <-> Manager
    draw_arrow(ax, 0.44, 0.65, 0.44, 0.59, "Chuyển ca (Handoff)", color="#1D4ED8", lx_off=-0.068)
    draw_arrow(ax, 0.54, 0.59, 0.54, 0.65, "Báo lệch/chốt", color="#B91C1C", ls="--", lx_off=0.048, ly_off=-0.005)

    # Manager <-> System
    draw_arrow(ax, 0.46, 0.39, 0.46, 0.34, "Tra cứu / Cập nhật", color="#5B21B6", lx_off=-0.068)
    draw_arrow(ax, 0.55, 0.34, 0.55, 0.39, "Dữ liệu / Gợi ý ILP", color="#6D28D9", ls=":", lx_off=0.068)

    # Manager <-> Tutor
    draw_arrow(ax, 0.63, 0.53, 0.705, 0.66, "Đề xuất lớp & lịch", color="#15803D", lx_off=0.015, ly_off=0.048)
    draw_arrow(ax, 0.705, 0.60, 0.63, 0.47, "Xác nhận / Từ chối", color="#B91C1C", ls="--", lx_off=0.025, ly_off=-0.032)

    # Value realization arrow
    draw_arrow(ax, 0.175, 0.56, 0.175, 0.43, "Tham gia đồng tạo\ngiá trị (Co-creation)", color="#BE123C", lx_off=0.085)
    draw_arrow(ax, 0.38, 0.25, 0.295, 0.27, "Cung ứng hạ tầng số", color="#6D28D9", ls=":", ly_off=0.028)

    # Legend (Chú giải ký hiệu) at bottom (y=0.02..0.11)
    legend_box = FancyBboxPatch(
        (0.03, 0.02), 0.94, 0.095,
        boxstyle="round,pad=0.008,rounding_size=0.012",
        facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1.2, zorder=2
    )
    ax.add_patch(legend_box)
    ax.text(0.045, 0.098, "CHÚ GIẢI KÝ HIỆU (LEGEND):", fontsize=8.2, fontweight="bold", color="#0F172A")

    # Legend items
    ax.plot([0.05, 0.09], [0.062, 0.062], color="#0369A1", lw=1.8)
    ax.text(0.098, 0.062, "Luồng thông tin & giao tiếp chính (Thông tin / Đề xuất)", va="center", fontsize=7.6)

    ax.plot([0.05, 0.09], [0.035, 0.035], color="#B91C1C", lw=1.8, linestyle="--")
    ax.text(0.098, 0.035, "Luồng phản hồi ngoại lệ / Từ chối lịch (Rework / Handoff ngược)", va="center", fontsize=7.6)

    ax.plot([0.48, 0.52], [0.062, 0.062], color="#6D28D9", lw=1.8, linestyle=":")
    ax.text(0.528, 0.062, "Luồng dữ liệu số & hỗ trợ quyết định (Platform / ILP TO-BE)", va="center", fontsize=7.6)

    ax.plot([0.48, 0.52], [0.035, 0.035], color="#0F172A", lw=1.8, linestyle="--")
    ax.text(0.528, 0.035, "Đường bao nét đứt lớn: Ranh giới hệ thống phân tích", va="center", fontsize=7.6)

    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, "fig0_resource_map.png")
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
