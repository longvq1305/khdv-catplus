"""
Build a 12-slide native PowerPoint (.pptx) presentation for a 10-minute defense
of Group 20's INT3501 Service Science project (CatPlus Tutor-Student Matching & Scheduling).

Design system:
  - Widescreen 16:9 (13.333" x 7.5")
  - Palette: Forest Green (#0F3D2E / #15803D), Warm Amber-Yellow (#F59E0B / #FBBF24),
    Vibrant Orange (#EA580C / #C2410C) on crisp White (#FFFFFF) content slides
    with Dark Forest Cover & Closing slides ("sandwich" structure).
  - Strictly zero AI clichés: no speaker script boxes, no timing notes, no academic
    bracket citations, no meta-commentary, no title underlines, no edge stripes.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from pptx.chart.data import CategoryChartData

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
PPTX_PATH = os.path.join(OUT_DIR, "Slide_Thuyet_Trinh_Nhom20_CatPlus.pptx")

# --- COLOR PALETTE (Yellow - Orange - Green) ---
FOREST_DARK     = RGBColor(15, 61, 46)     # #0F3D2E (Dark anchor background & deep titles)
FOREST_ELEVATED = RGBColor(24, 84, 64)     # #185440 (Card fill on dark slides)
FOREST_BORDER   = RGBColor(45, 118, 92)    # #2D765C

GREEN_PRIMARY   = RGBColor(21, 128, 61)    # #15803D (TO-BE / Success green)
GREEN_SOFT_BG   = RGBColor(236, 253, 245)  # #ECFDF5
GREEN_BORDER    = RGBColor(167, 243, 208)  # #A7F3D0

YELLOW_BRIGHT   = RGBColor(251, 191, 36)   # #FBBF24 (Bright gold on dark backgrounds)
AMBER_PRIMARY   = RGBColor(245, 158, 11)   # #F59E0B (Amber chart & badge fill)
AMBER_TEXT      = RGBColor(180, 83, 9)     # #B45309 (High-contrast amber text on light bg)
YELLOW_SOFT_BG  = RGBColor(255, 251, 235)  # #FFFBEB
YELLOW_BORDER   = RGBColor(253, 230, 138)  # #FDE68A

ORANGE_PRIMARY  = RGBColor(234, 88, 12)    # #EA580C (AS-IS / Bottleneck orange)
ORANGE_TEXT     = RGBColor(194, 65, 12)    # #C2410C (High-contrast orange text)
ORANGE_SOFT_BG  = RGBColor(255, 247, 237)  # #FFF7ED
ORANGE_BORDER   = RGBColor(254, 215, 170)  # #FED7AA

INK_DARK        = RGBColor(20, 38, 30)     # #14261E (Main body text)
INK_MUTED       = RGBColor(82, 102, 93)    # #52665D (Secondary text)
SURFACE_NEUTRAL = RGBColor(246, 249, 247)  # #F6F9F7
BORDER_NEUTRAL  = RGBColor(216, 226, 220)  # #D8E2DC
WHITE           = RGBColor(255, 255, 255)
MINT_TEXT       = RGBColor(209, 250, 229)  # #D1FAE5

FONT_MAIN = "Arial"
TOTAL_SLIDES = 12


def set_bg(slide, color):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg


def add_box(slide, x, y, w, h, fill_rgb, border_rgb=None, border_pt=1.0, rounded=True):
    shp_type = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    shp = slide.shapes.add_shape(shp_type, Inches(x), Inches(y), Inches(w), Inches(h))
    if rounded and len(shp.adjustments) > 0:
        shp.adjustments[0] = 0.045
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill_rgb
    if border_rgb is not None:
        shp.line.color.rgb = border_rgb
        shp.line.width = Pt(border_pt)
    else:
        shp.line.fill.background()
    return shp


def add_circle_badge(slide, x, y, d, text, fill_rgb, text_rgb=WHITE, fs=12):
    oval = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    oval.fill.solid()
    oval.fill.fore_color.rgb = fill_rgb
    oval.line.fill.background()
    tf = oval.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = text
    r.font.name = FONT_MAIN
    r.font.size = Pt(fs)
    r.font.bold = True
    r.font.color.rgb = text_rgb
    return oval


def add_pill(slide, x, y, w, h, text, fill_rgb, text_rgb, border_rgb=None, fs=10.0):
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    if len(pill.adjustments) > 0:
        pill.adjustments[0] = 0.5
    pill.fill.solid()
    pill.fill.fore_color.rgb = fill_rgb
    if border_rgb is not None:
        pill.line.color.rgb = border_rgb
        pill.line.width = Pt(1.0)
    else:
        pill.line.fill.background()
    tf = pill.text_frame
    tf.word_wrap = False
    tf.margin_left = Inches(0.12)
    tf.margin_right = Inches(0.12)
    tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = text
    r.font.name = FONT_MAIN
    r.font.size = Pt(fs)
    r.font.bold = True
    r.font.color.rgb = text_rgb
    return pill


def add_text(slide, x, y, w, h, text, fs=14, bold=False, color=INK_DARK,
             align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP, line_spacing=1.2):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = valign
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = line_spacing
    r = p.add_run()
    r.text = text
    r.font.name = FONT_MAIN
    r.font.size = Pt(fs)
    r.font.bold = bold
    r.font.color.rgb = color
    return tb


def add_bullets(slide, x, y, w, h, items, fs=13.0, color=INK_DARK, space_after=6, bullet_char="• "):
    """Add crisp multi-paragraph items with bold lead-in before colon if present."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for idx, item in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(space_after)
        p.line_spacing = 1.22
        if ":" in item:
            head, tail = item.split(":", 1)
            r1 = p.add_run()
            r1.text = f"{bullet_char}{head}:"
            r1.font.name = FONT_MAIN
            r1.font.size = Pt(fs)
            r1.font.bold = True
            r1.font.color.rgb = color

            r2 = p.add_run()
            r2.text = tail
            r2.font.name = FONT_MAIN
            r2.font.size = Pt(fs)
            r2.font.bold = False
            r2.font.color.rgb = color
        else:
            r = p.add_run()
            r.text = f"{bullet_char}{item}"
            r.font.name = FONT_MAIN
            r.font.size = Pt(fs)
            r.font.color.rgb = color
    return tb


def add_slide_header(slide, slide_num, tag_text, tag_theme, title_text, subtitle_text=""):
    """Consistent header motif: rounded category pill + slide counter + bold Action Title (zero underline bars!)."""
    set_bg(slide, WHITE)
    if tag_theme == "orange":
        bg_c, tx_c, bd_c = ORANGE_SOFT_BG, ORANGE_TEXT, ORANGE_BORDER
    elif tag_theme == "yellow":
        bg_c, tx_c, bd_c = YELLOW_SOFT_BG, AMBER_TEXT, YELLOW_BORDER
    else:
        bg_c, tx_c, bd_c = GREEN_SOFT_BG, GREEN_PRIMARY, GREEN_BORDER

    pill_w = max(2.1, len(tag_text) * 0.095 + 0.35)
    add_pill(slide, 0.65, 0.36, pill_w, 0.30, tag_text, bg_c, tx_c, bd_c, fs=9.5)

    # Subtle page indicator top right
    add_pill(slide, 11.85, 0.36, 0.83, 0.30, f"{slide_num} / {TOTAL_SLIDES}",
             SURFACE_NEUTRAL, INK_MUTED, BORDER_NEUTRAL, fs=9.5)

    # Action Title (single-line calibrated)
    add_text(slide, 0.65, 0.76, 12.03, 0.44, title_text,
             fs=21.0, bold=True, color=FOREST_DARK, line_spacing=1.10)

    if subtitle_text:
        add_text(slide, 0.65, 1.22, 12.03, 0.32, subtitle_text,
                 fs=12.2, bold=False, color=INK_MUTED, line_spacing=1.15)


def style_chart_common(chart, show_legend=False, legend_pos=XL_LEGEND_POSITION.TOP):
    chart.has_title = False
    chart.font.name = FONT_MAIN
    chart.font.size = Pt(10.5)
    chart.has_legend = show_legend
    if show_legend:
        chart.legend.position = legend_pos
        chart.legend.include_in_layout = False
        chart.legend.font.name = FONT_MAIN
        chart.legend.font.size = Pt(10)

    val_axis = chart.value_axis
    val_axis.minimum_scale = 0.0
    val_axis.has_major_gridlines = True
    val_axis.major_gridlines.format.line.color.rgb = BORDER_NEUTRAL
    val_axis.major_gridlines.format.line.width = Pt(0.75)
    val_axis.format.line.fill.background()
    val_axis.tick_labels.font.name = FONT_MAIN
    val_axis.tick_labels.font.size = Pt(9.5)
    val_axis.tick_labels.font.color.rgb = INK_MUTED

    cat_axis = chart.category_axis
    cat_axis.has_major_gridlines = False
    cat_axis.format.line.color.rgb = BORDER_NEUTRAL
    cat_axis.tick_labels.font.name = FONT_MAIN
    cat_axis.tick_labels.font.size = Pt(10.0)
    cat_axis.tick_labels.font.bold = True
    cat_axis.tick_labels.font.color.rgb = INK_DARK


# ==============================================================================
# SLIDE BUILDERS
# ==============================================================================

def build_slide_1_cover(prs, blank):
    s = prs.slides.add_slide(blank)
    set_bg(s, FOREST_DARK)

    # Subtle geometric circles top-right / bottom-right for modern visual depth
    c1 = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(10.2), Inches(-1.2), Inches(4.6), Inches(4.6))
    c1.fill.solid()
    c1.fill.fore_color.rgb = FOREST_ELEVATED
    c1.line.fill.background()

    c2 = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(11.3), Inches(5.3), Inches(3.2), Inches(3.2))
    c2.fill.solid()
    c2.fill.fore_color.rgb = FOREST_ELEVATED
    c2.line.fill.background()

    # Course badge
    add_pill(s, 0.80, 0.85, 4.95, 0.36,
             "KHOA HỌC DỊCH VỤ (INT3501) · ĐH CÔNG NGHỆ – ĐHQGHN",
             FOREST_ELEVATED, YELLOW_BRIGHT, FOREST_BORDER, fs=10.0)

    # Main Title
    add_text(s, 0.80, 1.55, 7.65, 2.35,
             "Tối ưu hóa quy trình ghép đôi\ngia sư – học viên và xếp lịch học\ntrên nền tảng CatPlus",
             fs=32, bold=True, color=WHITE, line_spacing=1.18)

    # Subtitle
    add_text(s, 0.80, 4.05, 7.45, 0.85,
             "Đối chứng phương án xếp lịch thủ công (AS-IS) và quy hoạch nguyên gom nhóm (MILP)\nkết hợp mô phỏng hàng đợi sự kiện rời rạc trên hệ thống đào tạo lập trình",
             fs=14, bold=False, color=MINT_TEXT, line_spacing=1.32)

    # Author card bottom-left
    add_box(s, 0.80, 5.45, 7.35, 1.25, FOREST_ELEVATED, FOREST_BORDER, border_pt=1.2)
    add_pill(s, 1.02, 5.65, 1.25, 0.30, "NHÓM 20", YELLOW_BRIGHT, FOREST_DARK, fs=10.0)
    add_text(s, 2.45, 5.64, 5.4, 0.34, "Sinh viên thực hiện:", fs=12.5, bold=True, color=YELLOW_BRIGHT)
    add_text(s, 1.02, 6.12, 6.9, 0.42,
             "Phoutthavong Xayavong (23021941)    ·    Vũ Quốc Long (23020105)",
             fs=14, bold=True, color=WHITE)

    # Right column: 3 Key Result Preview Cards (Green, Yellow, Orange accents)
    highlights = [
        ("92,7%", "Tỷ lệ ghép lớp thành công", "Tăng +32,3 điểm % so với xếp tay (60,4%)", YELLOW_BRIGHT),
        ("10,29 giờ", "Thời gian chờ trung bình", "Giảm 54,4% thời gian chờ (từ 22,56 giờ)", RGBColor(110, 231, 183)),
        ("99,3%", "Hoàn tất trong 2 ngày", "Tăng vọt từ mức 18,0% của quy trình cũ", RGBColor(253, 186, 116)),
    ]
    for idx, (val, ttl, sub, col) in enumerate(highlights):
        cy = 1.45 + idx * 1.82
        add_box(s, 8.75, cy, 3.80, 1.56, FOREST_ELEVATED, FOREST_BORDER, border_pt=1.2)
        add_text(s, 9.02, cy + 0.16, 3.3, 0.55, val, fs=28, bold=True, color=col)
        add_text(s, 9.02, cy + 0.74, 3.35, 0.32, ttl, fs=13.5, bold=True, color=WHITE)
        add_text(s, 9.02, cy + 1.08, 3.35, 0.38, sub, fs=11.0, bold=False, color=MINT_TEXT)


def build_slide_2_problem_scope(prs, blank):
    s = prs.slides.add_slide(blank)
    add_slide_header(
        s, 2, "01 · BÀI TOÁN & PHẠM VI", "orange",
        "Khâu xếp lịch thủ công đang làm nghẽn đầu vào học viên tại CatPlus",
        "Tư vấn đăng ký mới chỉ là nửa chặng đường; ghép đúng lịch giữa trò – thầy và đủ sĩ số nhóm mới tạo ra lớp học thực tế"
    )

    # Top row: 3 horizontal boundary stages connected by arrows
    stages = [
        ("ĐIỂM BẮT ĐẦU", "Học viên đăng ký mới",
         "• Học sinh THCS (55%) & THPT (45%)\n• Nhu cầu: N = 60 hồ sơ/tháng\n• Trạng thái đầu: Chưa liên hệ",
         YELLOW_SOFT_BG, YELLOW_BORDER, AMBER_TEXT),
        ("TRONG BIÊN PHÂN TÍCH (GIỮ CỐ ĐỊNH NGUỒN LỰC)", "Tư vấn khung giờ · Ghép gia sư · Gom nhóm",
         "• Hai hình thức: Kèm 1–1 (đúng 1 em) & Lớp nhóm (bắt buộc 3–5 em cùng cấp)\n• Nguồn lực cố định: 10 Gia sư · 2 CSKH · 1 Quản lý học vụ · 14 ca/tuần\n• Hiện trạng: Hỏi lịch qua ĐT/Zalo, dò tay tuần tự từng ca (FCFS)",
         GREEN_SOFT_BG, GREEN_BORDER, GREEN_PRIMARY),
        ("ĐIỂM KẾT THÚC & NGOÀI BIÊN", "Chốt lớp hoặc Đóng thất bại",
         "• Đầu ra: Nhập học hoặc Rớt lớp\n• Ngoài biên: Chấm bài lập trình tự động, biên soạn đề thi, đối soát học phí",
         ORANGE_SOFT_BG, ORANGE_BORDER, ORANGE_TEXT),
    ]
    xs = [0.65, 3.95, 9.45]
    ws = [2.95, 5.15, 3.23]
    for idx, (tag, ttl, body, bg, bd, tc) in enumerate(stages):
        add_box(s, xs[idx], 1.72, ws[idx], 2.22, bg, bd, border_pt=1.3)
        add_pill(s, xs[idx] + 0.18, 1.88, min(ws[idx] - 0.36, len(tag) * 0.088 + 0.3), 0.27, tag, WHITE, tc, bd, fs=8.8)
        add_text(s, xs[idx] + 0.18, 2.24, ws[idx] - 0.36, 0.32, ttl, fs=13.8, bold=True, color=FOREST_DARK)
        add_text(s, xs[idx] + 0.18, 2.60, ws[idx] - 0.36, 1.25, body, fs=11.0, color=INK_DARK, line_spacing=1.26)

    # Arrows between boundary boxes
    for ax_x in [3.65, 9.15]:
        arr = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(ax_x), Inches(2.68), Inches(0.25), Inches(0.26))
        arr.fill.solid()
        arr.fill.fore_color.rgb = AMBER_PRIMARY
        arr.line.fill.background()

    # Bottom row: 3 Core Research Questions & KPI Cards
    add_text(s, 0.65, 4.12, 12.0, 0.32,
             "BA CÂU HỎI PHÂN TÍCH GẮN VỚI BA CHỈ SỐ ĐO LƯỜNG TRỌNG TÂM",
             fs=11.5, bold=True, color=INK_MUTED)

    kpis = [
        ("Q1", "Tỷ lệ ghép thành công (%)",
         "Trên cùng 10 gia sư và ngưỡng nhóm 3–5 học viên, mô hình gom nhóm tăng thêm bao nhiêu % học viên vào lớp và cần hỏi tối thiểu mấy khung giờ?",
         GREEN_PRIMARY, GREEN_SOFT_BG, GREEN_BORDER),
        ("Q2", "Độ phù hợp lịch học (thang 100)",
         "Việc điều phối giờ học để gom đủ nhóm 3–5 em tạo ra sự đánh đổi như thế nào giữa điểm phù hợp cá nhân và điểm phù hợp toàn trung tâm?",
         AMBER_PRIMARY, YELLOW_SOFT_BG, YELLOW_BORDER),
        ("Q3", "Thời gian chờ & Độ bận nhân sự",
         "Quy trình cải tiến rút ngắn bao nhiêu giờ chờ trung bình, phân vị P90, tỷ lệ chốt trong 2 ngày (≤ 16h) và giải phóng bao nhiêu % tải cho Quản lý?",
         ORANGE_PRIMARY, ORANGE_SOFT_BG, ORANGE_BORDER),
    ]
    cw = 3.82
    gap = 0.28
    for idx, (num, ttl, desc, badge_c, bg_c, bd_c) in enumerate(kpis):
        cx = 0.65 + idx * (cw + gap)
        add_box(s, cx, 4.50, cw, 2.45, bg_c, bd_c, border_pt=1.3)
        add_circle_badge(s, cx + 0.22, 4.70, 0.44, num, badge_c, WHITE, fs=12)
        add_text(s, cx + 0.78, 4.74, cw - 0.98, 0.38, ttl, fs=14.5, bold=True, color=FOREST_DARK)
        add_text(s, cx + 0.22, 5.28, cw - 0.44, 1.50, desc, fs=12.2, color=INK_DARK, line_spacing=1.30)


def build_slide_3_work_system(prs, blank):
    s = prs.slides.add_slide(blank)
    add_slide_header(
        s, 3, "02 · HỆ THỐNG DỊCH VỤ", "yellow",
        "Mô hình Hệ thống làm việc chỉ ra 4 nút thắt cấu trúc gây rớt lớp nhóm",
        "Hiệu năng xếp lớp phụ thuộc vào sự ăn khớp giữa con người, thông tin lịch rảnh, quy tắc mở lớp và công cụ hỗ trợ"
    )

    # Left side (x=0.65..7.45): 9-component Work System architectural stack
    add_box(s, 0.65, 1.72, 6.80, 5.25, SURFACE_NEUTRAL, BORDER_NEUTRAL, border_pt=1.2)
    add_text(s, 0.90, 1.88, 6.30, 0.32, "9 THÀNH PHẦN HỆ THỐNG LÀM VIỆC (WORK SYSTEM) TẠI CATPLUS",
             fs=11.5, bold=True, color=FOREST_DARK)

    # Tier 1: Customers & Service Outputs
    add_box(s, 0.90, 2.30, 3.05, 1.22, YELLOW_SOFT_BG, YELLOW_BORDER, border_pt=1.2)
    add_text(s, 1.06, 2.40, 2.75, 0.28, "1. Khách hàng thụ hưởng", fs=12.5, bold=True, color=AMBER_TEXT)
    add_text(s, 1.06, 2.70, 2.75, 0.72, "Học sinh THCS/THPT & Phụ huynh cung cấp mục tiêu, khung giờ rảnh", fs=11.2, color=INK_DARK)

    add_box(s, 4.15, 2.30, 3.05, 1.22, GREEN_SOFT_BG, GREEN_BORDER, border_pt=1.2)
    add_text(s, 4.31, 2.40, 2.75, 0.28, "2. Sản phẩm & Dịch vụ", fs=12.5, bold=True, color=GREEN_PRIMARY)
    add_text(s, 4.31, 2.70, 2.75, 0.72, "Tư vấn lộ trình, buổi học thử & lớp chính thức (1–1 hoặc Nhóm 3–5 em)", fs=11.2, color=INK_DARK)

    # Tier 2: Core Operational Triad (Processes, Participants, Information, Technology)
    ops = [
        ("3. Quy trình hoạt động", "Tiếp nhận → Tư vấn → Dò lịch gia sư → Gom nhóm → Xác nhận lớp"),
        ("4. Người tham gia", "2 CSKH tư vấn, 1 Quản lý điều phối duyệt lớp, 10 Gia sư giảng dạy"),
        ("5. Thông tin điều phối", "Cấp học, hình thức lớp, khung giờ rảnh của trò & ca trống của thầy"),
        ("6. Công nghệ vận hành", "Phần mềm quản lý học vụ nội bộ, kênh liên lạc Zalo & điện thoại"),
    ]
    for idx, (t_lbl, t_desc) in enumerate(ops):
        col = idx % 2
        row = idx // 2
        bx = 0.90 + col * 3.25
        by = 3.68 + row * 1.02
        add_box(s, bx, by, 3.05, 0.90, WHITE, BORDER_NEUTRAL, border_pt=1.0)
        add_text(s, bx + 0.15, by + 0.10, 2.75, 0.26, t_lbl, fs=11.8, bold=True, color=FOREST_DARK)
        add_text(s, bx + 0.15, by + 0.38, 2.75, 0.46, t_desc, fs=10.6, color=INK_MUTED, line_spacing=1.18)

    # Tier 3: Foundation (Strategy, Environment, Infrastructure)
    fnds = [
        ("7. Chiến lược", "Tư vấn sát sao + tối ưu tải gia sư"),
        ("8. Môi trường", "Lịch học văn hóa dày tối & cuối tuần"),
        ("9. Hạ tầng", "Phòng học Meet/Zoom & máy chủ DB"),
    ]
    for idx, (f_lbl, f_desc) in enumerate(fnds):
        fx = 0.90 + idx * 2.13
        add_box(s, fx, 5.82, 2.04, 0.95, GREEN_SOFT_BG, GREEN_BORDER, border_pt=1.0)
        add_text(s, fx + 0.12, 5.92, 1.80, 0.25, f_lbl, fs=11.2, bold=True, color=FOREST_DARK)
        add_text(s, fx + 0.12, 6.20, 1.80, 0.50, f_desc, fs=10.2, color=INK_DARK, line_spacing=1.18)

    # Right side (x=7.72..12.68): 4 System Failure Cards
    add_text(s, 7.72, 1.72, 4.95, 0.32, "4 ĐIỂM LỖI HỆ THỐNG TRONG CÁCH LÀM HIỆN TẠI",
             fs=11.5, bold=True, color=ORANGE_TEXT)

    failures = [
        ("01", "Lỗi thông tin đầu vào",
         "CSKH chỉ hỏi 1 khung giờ ưa thích nhất; lịch trống của 10 gia sư nằm rời rạc trên tin nhắn Zalo."),
        ("02", "Lỗi hoạt động xếp lớp tuần tự",
         "Quản lý dò tay từng hồ sơ đến trước xếp trước làm học viên nhóm bị rải mỏng (1–2 em/ca, không đủ mở lớp)."),
        ("03", "Lỗi công nghệ hậu kiểm",
         "Phần mềm chỉ lưu kết quả sau khi con người tự xoay xở xong, thiếu thuật toán gom nhóm hỗ trợ quyết định."),
        ("04", "Lỗi thiết chế điều phối",
         "Chưa có nhịp gom đợt cố định trong ngày và thiếu phương án gia sư dự phòng khi phát sinh bận đột xuất."),
    ]
    for idx, (code, f_ttl, f_desc) in enumerate(failures):
        fy = 2.12 + idx * 1.24
        add_box(s, 7.72, fy, 4.96, 1.10, ORANGE_SOFT_BG, ORANGE_BORDER, border_pt=1.2)
        add_circle_badge(s, 7.90, fy + 0.18, 0.40, code, ORANGE_PRIMARY, WHITE, fs=11)
        add_text(s, 8.42, fy + 0.12, 4.10, 0.28, f_ttl, fs=13.0, bold=True, color=ORANGE_TEXT)
        add_text(s, 8.42, fy + 0.42, 4.10, 0.60, f_desc, fs=11.2, color=INK_DARK, line_spacing=1.22)


def build_slide_4_resource_map(prs, blank):
    s = prs.slides.add_slide(blank)
    add_slide_header(
        s, 4, "03 · BẢN ĐỒ NGUỒN LỰC", "yellow",
        "Tích hợp lịch rảnh khách hàng với năng lực điều phối để đồng tạo giá trị",
        "Lớp học chỉ hình thành khi thông tin khung giờ từ phía gia đình kết hợp đồng bộ với chuyên môn gia sư và quy tắc ghép nhóm"
    )

    # Left: High-resolution palette-matched Resource Map image
    img_path = os.path.join(OUT_DIR, "slide_fig_resource_map.png")
    add_box(s, 0.65, 1.70, 8.35, 5.30, WHITE, BORDER_NEUTRAL, border_pt=1.2)
    s.shapes.add_picture(img_path, Inches(0.75), Inches(1.80), width=Inches(8.15))

    # Right: 3-stage Value Co-Creation & Trade-off stack
    cards = [
        ("NGUỒN LỰC THAM GIA", GREEN_PRIMARY, GREEN_SOFT_BG, GREEN_BORDER,
         ["Toán hạng: Hồ sơ học viên, danh sách ca trống, khung 14 ca học/tuần.",
          "Toán tử: Kỹ năng tư vấn CSKH, kinh nghiệm điều phối của Quản lý, chuyên môn Gia sư và quy tắc MILP."]),
        ("CHUỖI CHUYỂN HÓA GIÁ TRỊ", AMBER_PRIMARY, YELLOW_SOFT_BG, YELLOW_BORDER,
         ["Đầu ra kỹ thuật: Mã lớp học thử / chính thức hợp lệ trên hệ thống.",
          "Kết quả dịch vụ: Học sinh vào đúng nhóm 3–5 em, đúng giờ, ít phải chờ.",
          "Giá trị thực tế: Tiến bộ tư duy lập trình & sự an tâm của phụ huynh."]),
        ("ĐÁNH ĐỔI GIỮA CÁC BÊN", ORANGE_PRIMARY, ORANGE_SOFT_BG, ORANGE_BORDER,
         ["Phụ huynh: Muốn học đúng giờ đẹp nhưng dễ rời bỏ nếu chờ quá 2 ngày.",
          "Trung tâm & Gia sư: Cần gom đủ 3–5 em/nhóm để tối ưu chi phí giảng dạy."]),
    ]
    for idx, (hdr, badge_c, bg_c, bd_c, bullets) in enumerate(cards):
        cy = 1.70 + idx * 1.80
        ch = 1.68
        add_box(s, 9.20, cy, 3.48, ch, bg_c, bd_c, border_pt=1.2)
        add_pill(s, 9.36, cy + 0.12, 2.45, 0.25, hdr, badge_c, WHITE, fs=8.6)
        add_bullets(s, 9.36, cy + 0.44, 3.16, ch - 0.50, bullets, fs=10.0, color=INK_DARK, space_after=3)


def build_slide_5_bpmn_as_is(prs, blank):
    s = prs.slides.add_slide(blank)
    add_slide_header(
        s, 5, "04 · QUY TRÌNH HIỆN TẠI (BPMN AS-IS)", "orange",
        "Quy trình AS-IS phát sinh nhiều bước chuyển giao và vòng lặp hỏi đổi lịch",
        "Đơn vị quy trình: 01 yêu cầu đăng ký mới đi qua 3 Pool độc lập (Phụ huynh & Học viên · Vận hành CatPlus · Gia sư)"
    )

    img_path = os.path.join(OUT_DIR, "slide_fig_bpmn_as_is.png")
    add_box(s, 0.65, 1.66, 12.03, 4.62, WHITE, BORDER_NEUTRAL, border_pt=1.2)
    # Constrain by height so all 3 pools fit cleanly inside the frame
    s.shapes.add_picture(img_path, Inches(1.98), Inches(1.72), height=Inches(4.48))

    # Bottom concise 4-pill diagnostic bar
    pills = [
        ("Chuyển giao (Handoff)", "CSKH chỉ lấy 1 khung giờ rồi đẩy hồ sơ sang Quản lý", YELLOW_SOFT_BG, YELLOW_BORDER, AMBER_TEXT),
        ("Chờ đợi (Waiting)", "Đợi gia sư phản hồi Zalo thủ công 2,5–7,5 giờ/vòng", ORANGE_SOFT_BG, ORANGE_BORDER, ORANGE_TEXT),
        ("Nghẽn nhóm (Bottleneck)", "Nhóm lẻ 1–2 học viên bị treo vì chưa đủ ngưỡng 3 người", ORANGE_SOFT_BG, ORANGE_BORDER, ORANGE_TEXT),
        ("Làm lại (Rework)", "Gọi lại phụ huynh xin đổi lịch tối đa 2 vòng trước khi rớt", YELLOW_SOFT_BG, YELLOW_BORDER, AMBER_TEXT),
    ]
    pw = 2.86
    gap = 0.19
    for idx, (pttl, psub, bg_c, bd_c, tx_c) in enumerate(pills):
        px = 0.65 + idx * (pw + gap)
        add_box(s, px, 6.42, pw, 0.76, bg_c, bd_c, border_pt=1.1)
        add_text(s, px + 0.14, 6.48, pw - 0.28, 0.24, pttl, fs=11.0, bold=True, color=tx_c)
        add_text(s, px + 0.14, 6.72, pw - 0.28, 0.40, psub, fs=9.8, color=INK_DARK, line_spacing=1.15)


def build_slide_6_diagnosis_metrics(prs, blank):
    s = prs.slides.add_slide(blank)
    add_slide_header(
        s, 6, "05 · CHẨN ĐOÁN ĐỊNH LƯỢNG", "orange",
        "Chặng dò lịch và làm lại chiếm 69,4% thời gian chờ, làm rớt 39,6% hồ sơ",
        "Kết quả đo trên 20 chu kỳ tháng mô phỏng tái lập (1.200 hồ sơ, N = 60 ca/tháng, quy ước 8 giờ làm việc/ngày)"
    )

    # Left card: Native Horizontal Bar Chart of Waiting Time Breakdown
    add_box(s, 0.65, 1.72, 6.85, 5.25, WHITE, BORDER_NEUTRAL, border_pt=1.2)
    add_text(s, 0.90, 1.88, 6.35, 0.34,
             "PHÂN RÃ THỜI GIAN CHU TRÌNH TRUNG BÌNH (TỔNG W = 22,56 GIỜ ≈ 2,82 NGÀY)",
             fs=11.5, bold=True, color=FOREST_DARK)

    chart_data = CategoryChartData()
    chart_data.categories = [
        "3. Chốt học thử & nhập học (22,0%)",
        "2. Dò lịch, hỏi Zalo & đổi giờ (69,4%)",
        "1. Tiếp nhận & gọi tư vấn đầu (8,6%)",
    ]
    chart_data.add_series("Giờ làm việc", (4.96, 15.66, 1.95))

    graphic_frame = s.shapes.add_chart(
        XL_CHART_TYPE.BAR_CLUSTERED,
        Inches(0.85), Inches(2.30), Inches(6.40), Inches(3.35),
        chart_data
    )
    chart = graphic_frame.chart
    style_chart_common(chart, show_legend=False)
    chart.value_axis.maximum_scale = 19.0

    plot = chart.plots[0]
    plot.gap_width = 85
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    dl.number_format = '0.00" giờ"'
    dl.font.name = FONT_MAIN
    dl.font.size = Pt(11)
    dl.font.bold = True
    dl.font.color.rgb = INK_DARK

    # Color individual bars: Green, Vibrant Orange (bottleneck!), Amber
    bar_colors = [GREEN_PRIMARY, ORANGE_PRIMARY, AMBER_PRIMARY]
    series = plot.series[0]
    for idx_pt, col_rgb in enumerate(bar_colors):
        pt = series.points[idx_pt]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = col_rgb

    # Diagnostic conclusion inside left card bottom
    add_box(s, 0.90, 5.82, 6.35, 0.92, ORANGE_SOFT_BG, ORANGE_BORDER, border_pt=1.0)
    add_text(s, 1.08, 5.92, 6.00, 0.72,
             "Bằng chứng loại trừ phỏng đoán cảm tính: CSKH gọi lần đầu chỉ mất 1,95 giờ (8,6%); điểm nghẽn thực sự nằm ở 15,66 giờ chờ phản hồi Zalo và lặp lại xin đổi giờ.",
             fs=11.3, bold=False, color=INK_DARK, line_spacing=1.25)

    # Right side: 2x2 Grid of Big Stat Callouts
    stats = [
        ("39,6%", "Hồ sơ rớt lớp mỗi tháng",
         "23,75 / 60 học viên bị rớt; trong đó 17,5 ca do lớp nhóm chỉ gom được 1–2 em.",
         ORANGE_PRIMARY, ORANGE_SOFT_BG, ORANGE_BORDER),
        ("18,0%", "Tỷ lệ đạt chuẩn ≤ 2 ngày",
         "Chỉ 18% hồ sơ chốt xong trong 16 giờ làm việc; phân vị P90 kéo dài tới 31,29 giờ.",
         ORANGE_PRIMARY, ORANGE_SOFT_BG, ORANGE_BORDER),
        ("49,7%", "Quỹ giờ Quản lý bị ngốn",
         "Gần một nửa ngày làm việc của Quản lý học vụ dùng để dò bảng lịch thủ công.",
         AMBER_TEXT, YELLOW_SOFT_BG, YELLOW_BORDER),
        ("5,64 ca", "Hồ sơ tồn đọng thường trực",
         "Theo Định luật Little (L = 0,25 × 22,56), luôn có ~6 hồ sơ nằm chờ xử lý.",
         GREEN_PRIMARY, GREEN_SOFT_BG, GREEN_BORDER),
    ]
    sw, sh = 2.38, 2.52
    for idx, (big_num, st_ttl, st_desc, num_c, bg_c, bd_c) in enumerate(stats):
        col = idx % 2
        row = idx // 2
        sx = 7.72 + col * (sw + 0.20)
        sy = 1.72 + row * (sh + 0.21)
        add_box(s, sx, sy, sw, sh, bg_c, bd_c, border_pt=1.2)
        add_text(s, sx + 0.18, sy + 0.20, sw - 0.36, 0.62, big_num, fs=30, bold=True, color=num_c)
        add_text(s, sx + 0.18, sy + 0.88, sw - 0.36, 0.42, st_ttl, fs=13.0, bold=True, color=FOREST_DARK, line_spacing=1.15)
        add_text(s, sx + 0.18, sy + 1.38, sw - 0.36, 1.00, st_desc, fs=11.0, color=INK_DARK, line_spacing=1.24)


def build_slide_7_milp_simpy_model(prs, blank):
    s = prs.slides.add_slide(blank)
    add_slide_header(
        s, 7, "06 · MÔ HÌNH TỐI ƯU & MÔ PHỎNG", "green",
        "Mô hình quy hoạch nguyên gom cụm lớp nhóm kết hợp mô phỏng hàng đợi",
        "Giải đồng thời bài toán gom đủ ngưỡng 3–5 học viên/nhóm bằng MILP và đo thời gian chờ động bằng SimPy"
    )

    # 3 Columns: Input Standardization -> MILP Formulation -> SimPy Queueing
    # Col 1: Inputs (Yellow)
    add_box(s, 0.65, 1.72, 3.60, 5.25, YELLOW_SOFT_BG, YELLOW_BORDER, border_pt=1.3)
    add_circle_badge(s, 0.85, 1.92, 0.42, "01", AMBER_PRIMARY, WHITE, fs=12)
    add_text(s, 1.38, 1.96, 2.70, 0.36, "Dữ liệu & Điểm hợp lịch", fs=14.5, bold=True, color=FOREST_DARK)
    add_bullets(s, 0.85, 2.52, 3.20, 4.25, [
        "Quy mô tháng: N = 60 học viên (40% kèm 1–1, 60% học nhóm) & M = 10 gia sư trên 14 khung giờ/tuần.",
        "Chuẩn hóa nguyện vọng: Mỗi học viên cung cấp tối đa 3 khung giờ khả dụng theo thứ tự ưu tiên.",
        "Thang điểm phù hợp (w): Ưu tiên 1 = 100 điểm, Ưu tiên 2 = 80 điểm, Ưu tiên 3 = 60 điểm (rớt = 0 điểm).",
        "Năng lực gia sư: Mỗi gia sư trống 5–7 ca/tuần, nhận dạy tối đa K_t từ 3 đến 5 lớp.",
    ], fs=11.8, color=INK_DARK, space_after=10)

    # Col 2: MILP Core (Green Highlight)
    add_box(s, 4.50, 1.72, 4.35, 5.25, GREEN_SOFT_BG, GREEN_PRIMARY, border_pt=1.6)
    add_circle_badge(s, 4.70, 1.92, 0.42, "02", GREEN_PRIMARY, WHITE, fs=12)
    add_text(s, 5.23, 1.96, 3.45, 0.36, "Quy hoạch nguyên hỗn hợp (MILP)", fs=14.5, bold=True, color=FOREST_DARK)

    # Clean visual formula cards inside Col 2
    add_box(s, 4.70, 2.50, 3.95, 1.12, WHITE, GREEN_BORDER, border_pt=1.1)
    add_text(s, 4.85, 2.58, 3.65, 0.25, "BIẾN QUYẾT ĐỊNH NHỊ PHÂN {0, 1}", fs=10.0, bold=True, color=GREEN_PRIMARY)
    add_text(s, 4.85, 2.86, 3.65, 0.68,
             "• x(i,k) = 1: Gán học viên i vào ca gia sư k\n"
             "• y(k,c) = 1: Mở lớp cấu hình c tại ca k  |  u(i) = 1: Lớp ảo (chưa ghép)",
             fs=11.0, color=INK_DARK, line_spacing=1.25)

    add_box(s, 4.70, 3.76, 3.95, 1.20, FOREST_DARK, FOREST_DARK, border_pt=1.0)
    add_text(s, 4.85, 3.86, 3.65, 0.25, "HÀM MỤC TIÊU TỔNG TRỌNG SỐ", fs=10.0, bold=True, color=YELLOW_BRIGHT)
    add_text(s, 4.85, 4.16, 3.65, 0.68,
             "min Z = ∑ P · u(i)  −  ∑ w(i,k) · x(i,k)  +  γ ∑ y(k,c)\n"
             "(Phạt rớt lớp P = 1.000 · Tối đa hợp lịch · Kiểm soát số ca mở γ)",
             fs=11.2, bold=True, color=WHITE, line_spacing=1.28)

    add_box(s, 4.70, 5.10, 3.95, 1.68, WHITE, GREEN_BORDER, border_pt=1.1)
    add_text(s, 4.85, 5.18, 3.65, 0.24, "RÀNG BUỘC SĨ SỐ & NĂNG LỰC CỨNG", fs=10.0, bold=True, color=ORANGE_TEXT)
    add_text(s, 4.85, 5.44, 3.65, 1.24,
             "• Mỗi học viên vào tối đa 1 lớp thật hoặc lớp ảo: ∑ x + u = 1\n"
             "• Lớp 1–1 đúng 1 em; Lớp nhóm bắt buộc: 3 · y ≤ ∑ x ≤ 5 · y\n"
             "• Không vượt trần số lớp K_t của từng gia sư (giải < 0,5 giây)",
             fs=10.3, color=INK_DARK, line_spacing=1.22)

    # Col 3: SimPy Queueing (Orange/Amber)
    add_box(s, 9.10, 1.72, 3.58, 5.25, ORANGE_SOFT_BG, ORANGE_BORDER, border_pt=1.3)
    add_circle_badge(s, 9.30, 1.92, 0.42, "03", ORANGE_PRIMARY, WHITE, fs=12)
    add_text(s, 9.83, 1.96, 2.70, 0.36, "Mô phỏng hàng đợi SimPy", fs=14.5, bold=True, color=FOREST_DARK)
    add_bullets(s, 9.30, 2.52, 3.18, 4.25, [
        "Vì sao cần SimPy: Quy trình có rẽ nhánh làm lại (Rework) và gom đợt nên không thể áp công thức hàng đợi tĩnh đơn lẻ.",
        "Dòng đến ngẫu nhiên: Hồ sơ đến theo quá trình Poisson (λ = 0,25 hồ sơ/giờ) qua 2 CSKH và 1 Quản lý.",
        "Nhịp gom đợt thực tế: Hệ thống chạy MILP 2 đợt/ngày (11h30 & 17h30), tính cả 8% xác suất gia sư bận đột xuất.",
        "Độ tin cậy thống kê: Chạy độc lập 20 chu kỳ tháng (seed = 42) để đo chính xác W, P90 và SLA ≤ 16h.",
    ], fs=11.6, color=INK_DARK, space_after=10)


def build_slide_8_bpmn_to_be(prs, blank):
    s = prs.slides.add_slide(blank)
    add_slide_header(
        s, 8, "07 · QUY TRÌNH CẢI TIẾN (TO-BE)", "green",
        "Chuẩn hóa thu thập 1–3 khung giờ và gợi ý MILP giúp chốt lớp trong 1 vòng",
        "Giữ nguyên quy mô nhân sự và vai trò tư vấn con người; công nghệ đảm nhận khâu tính toán gom nhóm phức tạp"
    )

    img_path = os.path.join(OUT_DIR, "slide_fig_bpmn_to_be.png")
    add_box(s, 0.65, 1.66, 12.03, 3.62, WHITE, BORDER_NEUTRAL, border_pt=1.2)
    # Constrain by height so all 3 pools fit cleanly inside the 3.62" frame
    s.shapes.add_picture(img_path, Inches(1.94), Inches(1.73), height=Inches(3.48))

    add_text(s, 0.65, 5.40, 12.0, 0.28,
             "BẢNG QUY TẮC XỬ LÝ NHANH CỦA QUẢN LÝ HỌC VỤ SAU MỖI ĐỢT CHẠY GỢI Ý (11H30 & 17H30)",
             fs=11.0, bold=True, color=FOREST_DARK)

    rules = [
        ("Khớp lớp 1–1 hoặc Nhóm 3–5 em",
         "Quản lý bấm duyệt trên màn hình; CSKH báo lịch chốt cho phụ huynh ngay trong vòng đầu.",
         GREEN_SOFT_BG, GREEN_BORDER, GREEN_PRIMARY),
        ("Gia sư chính bận đột xuất (~8%)",
         "Chọn ngay phương án gia sư dự phòng số 2 do hệ thống gợi ý sẵn, không cần gọi hỏi lại gia đình.",
         YELLOW_SOFT_BG, YELLOW_BORDER, AMBER_TEXT),
        ("Nhóm mới gom được 2 học viên",
         "Giữ chờ tối đa thêm 1 đợt chạy kế tiếp (nửa ngày); nếu chưa đủ 3 em thì tư vấn lộ trình 1–1.",
         YELLOW_SOFT_BG, YELLOW_BORDER, AMBER_TEXT),
        ("Hồ sơ rơi vào lớp ảo (lịch quá hẹp)",
         "Cảnh báo sớm ngay trong ngày đầu để CSKH chủ động thương lượng mở rộng khung giờ.",
         ORANGE_SOFT_BG, ORANGE_BORDER, ORANGE_TEXT),
    ]
    rw = 2.86
    gap = 0.19
    for idx, (r_ttl, r_desc, bg_c, bd_c, tx_c) in enumerate(rules):
        rx = 0.65 + idx * (rw + gap)
        add_box(s, rx, 5.74, rw, 1.36, bg_c, bd_c, border_pt=1.2)
        add_text(s, rx + 0.15, 5.84, rw - 0.30, 0.36, r_ttl, fs=11.5, bold=True, color=tx_c, line_spacing=1.15)
        add_text(s, rx + 0.15, 6.26, rw - 0.30, 0.76, r_desc, fs=10.4, color=INK_DARK, line_spacing=1.20)


def build_slide_9_comparison_results(prs, blank):
    s = prs.slides.add_slide(blank)
    add_slide_header(
        s, 9, "08 · ĐỐI CHỨNG HIỆU QUẢ", "green",
        "Phương án TO-BE nâng tỷ lệ ghép lên 92,7% và giảm 54,4% thời gian chờ",
        "Đối chứng công bằng trên cùng tập nhu cầu N = 60 học viên/tháng và đội ngũ M = 10 gia sư"
    )

    # Top row: 4 Hero Impact KPI Cards
    cards = [
        ("92,7%", "Tỷ lệ ghép thành công", "Tăng +32,3 điểm % (từ 60,4%)\nGiảm 81,5% số ca rớt lớp",
         GREEN_PRIMARY, GREEN_SOFT_BG, GREEN_BORDER),
        ("86,5 đ", "Độ hợp lịch toàn tập", "Tăng +28,0 điểm (từ 58,5 đ)\nNhóm vào lớp đạt 93,3 / 100",
         AMBER_TEXT, YELLOW_SOFT_BG, YELLOW_BORDER),
        ("10,29h", "Thời gian chờ TB", "Giảm 54,4% (từ 22,56 giờ)\nP90 giảm từ 31,29h còn 13,24h",
         GREEN_PRIMARY, GREEN_SOFT_BG, GREEN_BORDER),
        ("8,7%", "Độ bận Quản lý học vụ", "Giảm mạnh từ 49,7% quỹ giờ\nĐạt hạn ≤ 16h lên tới 99,3%",
         ORANGE_TEXT, ORANGE_SOFT_BG, ORANGE_BORDER),
    ]
    cw = 2.84
    gap = 0.22
    for idx, (val, ttl, sub, vc, bg_c, bd_c) in enumerate(cards):
        cx = 0.65 + idx * (cw + gap)
        add_box(s, cx, 1.68, cw, 1.62, bg_c, bd_c, border_pt=1.3)
        add_text(s, cx + 0.18, 1.78, cw - 0.36, 0.54, val, fs=27, bold=True, color=vc)
        add_text(s, cx + 0.18, 2.34, cw - 0.36, 0.30, ttl, fs=12.5, bold=True, color=FOREST_DARK)
        add_text(s, cx + 0.18, 2.66, cw - 0.36, 0.55, sub, fs=10.5, color=INK_DARK, line_spacing=1.20)

    # Bottom Left: Native Grouped Column Chart
    add_box(s, 0.65, 3.50, 6.15, 3.55, WHITE, BORDER_NEUTRAL, border_pt=1.2)
    add_text(s, 0.88, 3.64, 5.70, 0.28, "SO SÁNH BA CHỈ SỐ CHẤT LƯỢNG CỐT LÕI (THANG 0–100)",
             fs=11.0, bold=True, color=FOREST_DARK)

    c_data = CategoryChartData()
    c_data.categories = ["Tỷ lệ ghép lớp (%)", "Hợp lịch chung (điểm)", "Đạt hạn ≤ 2 ngày (%)"]
    c_data.add_series("AS-IS (Xếp tay)", (60.4, 58.5, 18.0))
    c_data.add_series("TO-BE (Hỏi 2 ca)", (87.8, 82.7, 98.8))
    c_data.add_series("TO-BE (Hỏi 3 ca)", (92.7, 86.5, 99.3))

    gf = s.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED,
        Inches(0.80), Inches(3.96), Inches(5.85), Inches(2.95),
        c_data
    )
    ch = gf.chart
    style_chart_common(ch, show_legend=True, legend_pos=XL_LEGEND_POSITION.TOP)
    ch.value_axis.maximum_scale = 115.0
    plot = ch.plots[0]
    plot.gap_width = 110
    plot.overlap = -12
    plot.has_data_labels = True
    plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    plot.data_labels.number_format = "0.0"
    plot.data_labels.font.name = FONT_MAIN
    plot.data_labels.font.size = Pt(9.0)
    plot.data_labels.font.bold = True

    series_cols = [ORANGE_PRIMARY, AMBER_PRIMARY, GREEN_PRIMARY]
    for s_idx, col_rgb in enumerate(series_cols):
        ser = plot.series[s_idx]
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = col_rgb

    # Bottom Right: Clean Native Comparison Table
    add_box(s, 7.00, 3.50, 5.68, 3.55, WHITE, BORDER_NEUTRAL, border_pt=1.2)
    add_text(s, 7.22, 3.64, 5.25, 0.28, "BẢNG ĐỐI CHỨNG ĐẦY ĐỦ CÁC PHƯƠNG ÁN",
             fs=11.0, bold=True, color=FOREST_DARK)

    rows_data = [
        ["Chỉ số đo lường", "AS-IS", "TO-BE (1 ca)", "TO-BE (3 ca)"],
        ["Tỷ lệ ghép lớp (%)", "60,4%", "58,3%", "92,7%"],
        ["Học viên rớt / tháng", "23,75 ca", "25,00 ca", "4,40 ca"],
        ["Hợp lịch nhóm đỗ", "96,8 đ", "100,0 đ", "93,3 đ"],
        ["Hợp lịch toàn tập", "58,5 đ", "58,3 đ", "86,5 đ"],
        ["Thời gian chờ TB (W)", "22,56 giờ", "9,69 giờ", "10,29 giờ"],
        ["Phân vị chờ P90", "31,29 giờ", "12,84 giờ", "13,24 giờ"],
        ["Hồ sơ tồn đọng (L)", "5,64 ca", "2,42 ca", "2,57 ca"],
    ]
    tbl_shp = s.shapes.add_table(len(rows_data), 4, Inches(7.18), Inches(4.00), Inches(5.32), Inches(2.88))
    tbl = tbl_shp.table
    col_ws = [Inches(2.12), Inches(1.02), Inches(1.08), Inches(1.10)]
    for c_i, w_val in enumerate(col_ws):
        tbl.columns[c_i].width = w_val

    for r_i, r_vals in enumerate(rows_data):
        for c_i, val in enumerate(r_vals):
            cell = tbl.cell(r_i, c_i)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            if r_i == 0:
                cell.fill.fore_color.rgb = FOREST_DARK
            elif c_i == 3:
                cell.fill.fore_color.rgb = GREEN_SOFT_BG
            elif r_i % 2 == 1:
                cell.fill.fore_color.rgb = SURFACE_NEUTRAL
            else:
                cell.fill.fore_color.rgb = WHITE

            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if c_i == 0 else PP_ALIGN.CENTER
            run = p.add_run()
            run.text = val
            run.font.name = FONT_MAIN
            run.font.size = Pt(9.8)
            run.font.bold = (r_i == 0 or c_i == 3)
            if r_i == 0:
                run.font.color.rgb = WHITE
            elif c_i == 3:
                run.font.color.rgb = GREEN_PRIMARY
            elif c_i == 1 and r_i in (1, 2, 5):
                run.font.color.rgb = ORANGE_TEXT
            else:
                run.font.color.rgb = INK_DARK


def build_slide_10_sensitivity_pareto(prs, blank):
    s = prs.slides.add_slide(blank)
    add_slide_header(
        s, 10, "09 · ĐỘ NHẠY & ĐÁNH ĐỔI ĐA MỤC TIÊU", "yellow",
        "Thu thập từ 2 khung giờ là tiên quyết; hiệu quả bền vững khi thiếu gia sư",
        "Kiểm định 11 kịch bản biến động nguồn lực và phân tích đường biên Pareto theo trọng số chi phí mở lớp γ"
    )

    # Left Card: Sensitivity Native Chart (Slots m & Tutor count M)
    add_box(s, 0.65, 1.72, 5.88, 5.25, WHITE, BORDER_NEUTRAL, border_pt=1.2)
    add_text(s, 0.88, 1.88, 5.40, 0.30,
             "ĐỘ NHẠY TỶ LỆ GHÉP THEO SỐ KHUNG GIỜ & SỐ GIA SƯ (%)",
             fs=11.2, bold=True, color=FOREST_DARK)

    s_data = CategoryChartData()
    s_data.categories = ["Hỏi 1 ca", "Hỏi 2 ca", "Hỏi 3 ca", "6 Gia sư", "10 Gia sư", "12 Gia sư"]
    s_data.add_series("AS-IS (Xếp tay)", (60.8, 60.8, 60.8, 50.1, 63.1, 62.2))
    s_data.add_series("TO-BE (MILP)", (58.3, 87.8, 92.1, 75.3, 93.9, 91.9))

    gf1 = s.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED,
        Inches(0.80), Inches(2.24), Inches(5.55), Inches(3.25),
        s_data
    )
    ch1 = gf1.chart
    style_chart_common(ch1, show_legend=True, legend_pos=XL_LEGEND_POSITION.TOP)
    ch1.value_axis.maximum_scale = 110.0
    p1 = ch1.plots[0]
    p1.gap_width = 95
    p1.overlap = -10
    p1.has_data_labels = True
    p1.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    p1.data_labels.number_format = "0.0"
    p1.data_labels.font.name = FONT_MAIN
    p1.data_labels.font.size = Pt(8.8)
    p1.data_labels.font.bold = True

    p1.series[0].format.fill.solid()
    p1.series[0].format.fill.fore_color.rgb = ORANGE_PRIMARY
    p1.series[1].format.fill.solid()
    p1.series[1].format.fill.fore_color.rgb = GREEN_PRIMARY

    add_box(s, 0.88, 5.62, 5.42, 1.16, GREEN_SOFT_BG, GREEN_BORDER, border_pt=1.0)
    add_bullets(s, 1.04, 5.72, 5.12, 1.00, [
        "Ngưỡng thông tin: Nếu chỉ hỏi 1 ca, MILP chỉ đạt 58,3%; hỏi từ 2 ca vọt ngay lên 87,8%.",
        "Chống chịu thiếu nhân sự: Với 6 gia sư, MILP đạt 75,3% — cao hơn xếp tay có tới 12 gia sư (62,2%).",
    ], fs=10.6, color=INK_DARK, space_after=4)

    # Right Card: Pareto Frontier & Operational Trade-offs
    add_box(s, 6.75, 1.72, 5.93, 5.25, WHITE, BORDER_NEUTRAL, border_pt=1.2)
    add_text(s, 6.98, 1.88, 5.45, 0.30,
             "ĐƯỜNG BIÊN PARETO KHI ĐIỀU CHỈNH TRỌNG SỐ CHI PHÍ MỞ CA (γ)",
             fs=11.2, bold=True, color=FOREST_DARK)

    p_rows = [
        ["Mức trọng số γ", "Số ca mở / tháng", "Tỷ lệ ghép", "Chính sách vận hành tương ứng"],
        ["γ = 10 (Đề xuất)", "33,3 ca", "91,3%", "Tối đa hóa nhận lớp ở mọi mức ưu tiên 1–3"],
        ["γ = 1.065", "32,2 ca", "89,4%", "Ngừng mở lớp lẻ 1–1 rơi vào ưu tiên 3"],
        ["γ = 1.085 (Cao điểm)", "29,7 ca", "85,3%", "Ưu tiên dồn nhóm 4–5 em, tiết kiệm 3,6 ca"],
        ["γ = 1.105", "8,9 ca", "50,7%", "Chỉ mở lớp nhóm đông, dừng hẳn lớp 1–1"],
    ]
    ptbl_s = s.shapes.add_table(len(p_rows), 4, Inches(6.95), Inches(2.26), Inches(5.52), Inches(2.22))
    ptbl = ptbl_s.table
    p_ws = [Inches(1.38), Inches(1.12), Inches(0.92), Inches(2.10)]
    for ci, wv in enumerate(p_ws):
        ptbl.columns[ci].width = wv

    for ri, rvals in enumerate(p_rows):
        for ci, val in enumerate(rvals):
            c = ptbl.cell(ri, ci)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            c.fill.solid()
            if ri == 0:
                c.fill.fore_color.rgb = FOREST_DARK
            elif ri == 1:
                c.fill.fore_color.rgb = GREEN_SOFT_BG
            elif ri == 3:
                c.fill.fore_color.rgb = YELLOW_SOFT_BG
            else:
                c.fill.fore_color.rgb = WHITE
            p = c.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if ci in (0, 3) else PP_ALIGN.CENTER
            rn = p.add_run()
            rn.text = val
            rn.font.name = FONT_MAIN
            rn.font.size = Pt(9.5)
            rn.font.bold = (ri in (0, 1))
            rn.font.color.rgb = WHITE if ri == 0 else (GREEN_PRIMARY if ri == 1 and ci < 3 else INK_DARK)

    # 3 Explicit Trade-offs box below Pareto table
    add_box(s, 6.95, 4.66, 5.52, 2.12, YELLOW_SOFT_BG, YELLOW_BORDER, border_pt=1.1)
    add_text(s, 7.12, 4.76, 5.20, 0.28, "BA ĐÁNH ĐỔI THỰC TẾ CẦN KIỂM SOÁT",
             fs=10.8, bold=True, color=AMBER_TEXT)
    add_bullets(s, 7.12, 5.08, 5.20, 1.62, [
        "Cuộc gọi đầu dài thêm 3–5 phút: Để hỏi kỹ 2–3 khung giờ, đổi lại cắt bỏ các cuộc gọi xin đổi lịch về sau.",
        "Độ trễ gom đợt nửa ngày: Chờ chạy đợt 11h30 / 17h30 nhưng tổng thời gian vẫn giảm hơn 54%.",
        "Giảm nhẹ 3,5 điểm ưu tiên cá nhân: Nhường ca hiếm để gom đủ nhóm 3–5 em, cứu thêm +32,3% học viên.",
    ], fs=10.4, color=INK_DARK, space_after=5)


def build_slide_11_roadmap_governance(prs, blank):
    s = prs.slides.add_slide(blank)
    add_slide_header(
        s, 11, "10 · LỘ TRÌNH & MINH BẠCH NGHIÊN CỨU", "green",
        "Lộ trình áp dụng 2 giai đoạn không tăng nhân sự và bộ chỉ số giám sát",
        "Triển khai trực tiếp trên nền tảng sẵn có của CatPlus kèm cơ chế kiểm chứng dữ liệu minh bạch"
    )

    # Left Column: 2-step Implementation Roadmap + 4 BSC KPIs
    add_box(s, 0.65, 1.72, 6.05, 2.55, GREEN_SOFT_BG, GREEN_BORDER, border_pt=1.3)
    add_text(s, 0.88, 1.86, 5.60, 0.30, "LỘ TRÌNH TRIỂN KHAI THỰC TẾ (KHÔNG TĂNG BIÊN CHẾ)",
             fs=11.5, bold=True, color=FOREST_DARK)

    add_circle_badge(s, 0.88, 2.28, 0.40, "B1", AMBER_PRIMARY, WHITE, fs=11)
    add_text(s, 1.40, 2.26, 5.10, 0.28, "Tuần 1–2: Chuẩn hóa thiết chế thông tin đầu vào", fs=12.5, bold=True, color=AMBER_TEXT)
    add_text(s, 1.40, 2.54, 5.10, 0.58, "Cập nhật biểu mẫu CSKH bắt buộc ghi nhận 2–3 khung giờ ưu tiên; áp dụng lịch đăng ký ca trống cố định đầu tuần cho 10 gia sư.", fs=10.8, color=INK_DARK)

    add_circle_badge(s, 0.88, 3.24, 0.40, "B2", GREEN_PRIMARY, WHITE, fs=11)
    add_text(s, 1.40, 3.22, 5.10, 0.28, "Từ tuần 3: Tích hợp nút gợi ý MILP chạy song song", fs=12.5, bold=True, color=GREEN_PRIMARY)
    add_text(s, 1.40, 3.50, 5.10, 0.62, "Nhúng mô-đun giải MILP lên hệ thống quản trị (chạy 11h30 & 17h30); đối chứng với quyết định duyệt thực tế 1 tháng trước khi vận hành chính thức.", fs=10.8, color=INK_DARK)

    # 4 Balanced Scorecard Perspectives (2x2 mini cards bottom-left)
    add_text(s, 0.65, 4.44, 6.05, 0.28, "BỘ CHỈ SỐ THEO DÕI BỐN GÓC NHÌN CÂN BẰNG",
             fs=11.2, bold=True, color=FOREST_DARK)
    bsc = [
        ("Hiệu quả nguồn lực", "Sĩ số TB lớp nhóm mở mới ≥ 3,8 em/lớp (hằng tháng)", YELLOW_SOFT_BG, YELLOW_BORDER, AMBER_TEXT),
        ("Khách hàng thụ hưởng", "Tỷ lệ ghép lớp, SLA ≤ 16h & điểm hợp lịch (hằng tuần)", GREEN_SOFT_BG, GREEN_BORDER, GREEN_PRIMARY),
        ("Quy trình nội bộ", "Tỷ lệ phải gọi đổi giờ & độ bận Quản lý (hằng tuần)", SURFACE_NEUTRAL, BORDER_NEUTRAL, FOREST_DARK),
        ("Học hỏi & Mở rộng", "Thống kê khung giờ có lớp ảo u = 1 để tuyển gia sư", ORANGE_SOFT_BG, ORANGE_BORDER, ORANGE_TEXT),
    ]
    bw, bh = 2.92, 1.02
    for idx, (b_ttl, b_sub, bg_c, bd_c, tx_c) in enumerate(bsc):
        col = idx % 2
        row = idx // 2
        bx = 0.65 + col * (bw + 0.21)
        by = 4.78 + row * (bh + 0.16)
        add_box(s, bx, by, bw, bh, bg_c, bd_c, border_pt=1.1)
        add_text(s, bx + 0.14, by + 0.12, bw - 0.28, 0.26, b_ttl, fs=11.5, bold=True, color=tx_c)
        add_text(s, bx + 0.14, by + 0.42, bw - 0.28, 0.50, b_sub, fs=10.2, color=INK_DARK, line_spacing=1.18)

    # Right Column: Limitations, Future Work & AI Transparency
    add_box(s, 6.95, 1.72, 5.73, 2.55, YELLOW_SOFT_BG, YELLOW_BORDER, border_pt=1.2)
    add_text(s, 7.18, 1.86, 5.25, 0.30, "GIỚI HẠN HIỆN TẠI & HƯỚNG PHÁT TRIỂN",
             fs=11.5, bold=True, color=AMBER_TEXT)
    add_bullets(s, 7.18, 2.24, 5.28, 1.92, [
        "Dữ liệu mô phỏng tái lập: Bộ số liệu hiện tại chạy trên hạt giống cố định (seed = 42); cần hiệu chỉnh lại trọng số khung giờ ngay khi nạp CSV lịch sử từ máy chủ CatPlus.",
        "Ghép xen lớp đang học: Mở rộng mô hình cho phép xếp học viên mới vào các nhóm hiện hữu còn chỗ trống (3–4 em) có cùng tiến độ bài học.",
        "Chính sách ca cao điểm: Dùng thống kê biến lớp ảo để khuyến khích gia sư mở thêm ca cuối tuần.",
    ], fs=10.8, color=INK_DARK, space_after=6)

    add_box(s, 6.95, 4.46, 5.73, 2.50, SURFACE_NEUTRAL, BORDER_NEUTRAL, border_pt=1.2)
    add_text(s, 7.18, 4.60, 5.25, 0.30, "KHAI BÁO MINH BẠCH SỬ DỤNG CÔNG CỤ AI",
             fs=11.5, bold=True, color=FOREST_DARK)
    add_bullets(s, 7.18, 4.98, 5.28, 1.88, [
        "Phạm vi hỗ trợ: Hỗ trợ sinh mã mô phỏng MILP/SimPy, kết xuất đồ họa sơ đồ và bố cục trình chiếu; tuyệt đối không dùng AI sinh dữ liệu giả mạo thực tế.",
        "Kiểm chứng của Nhóm 20: Tự thiết lập cấu trúc nghiệp vụ thật của CatPlus, kiểm tra độc lập từng bất đẳng thức toán học, rà soát 10 quy tắc BPMN 2.0 và chạy kiểm thử toàn bộ mã nguồn.",
    ], fs=10.8, color=INK_DARK, space_after=8)


def build_slide_12_conclusion(prs, blank):
    s = prs.slides.add_slide(blank)
    set_bg(s, FOREST_DARK)

    # Decorative subtle circle
    c1 = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(10.5), Inches(-1.0), Inches(4.2), Inches(4.2))
    c1.fill.solid()
    c1.fill.fore_color.rgb = FOREST_ELEVATED
    c1.line.fill.background()

    add_pill(s, 0.80, 0.60, 2.35, 0.34, "TỔNG KẾT ĐỀ TÀI",
             FOREST_ELEVATED, YELLOW_BRIGHT, FOREST_BORDER, fs=10.0)

    add_text(s, 0.80, 1.12, 11.7, 0.96,
             "Chuẩn hóa đầu vào đồng tạo giá trị kết hợp tối ưu hóa\ngiúp bứt phá hiệu năng trên cùng đội ngũ nhân sự hiện có",
             fs=22, bold=True, color=WHITE, line_spacing=1.22)

    # 3 Takeaway Answer Cards (Q1, Q2, Q3)
    answers = [
        ("KẾT LUẬN Q1 · TỶ LỆ GHÉP LỚP", "+32,3 điểm %",
         "Tăng tỷ lệ ghép lớp từ 60,4% lên 92,7% (giảm 81,5% lượng học viên rớt lớp) trên cùng 10 gia sư khi thu thập tối thiểu 2–3 khung giờ rảnh.",
         YELLOW_BRIGHT),
        ("KẾT LUẬN Q2 · ĐỘ PHÙ HỢP LỊCH", "86,5 / 100 điểm",
         "Đánh đổi nhẹ 3,5 điểm trên tập đỗ để gom đủ nhóm 3–5 em, giúp nâng điểm hợp lịch toàn bộ người đăng ký thêm +28,0 điểm (trội Pareto).",
         RGBColor(110, 231, 183)),
        ("KẾT LUẬN Q3 · THỜI GIAN CHỜ & TẢI", "−54,4% giờ chờ",
         "Rút ngắn thời gian chờ từ 22,56h xuống 10,29h (99,3% chốt trong 2 ngày); giảm tải dò lịch thủ công cho Quản lý từ 49,7% xuống 8,7%.",
         RGBColor(253, 186, 116)),
    ]
    cw = 3.75
    gap = 0.24
    for idx, (tag, big, desc, col) in enumerate(answers):
        cx = 0.80 + idx * (cw + gap)
        add_box(s, cx, 2.42, cw, 3.05, FOREST_ELEVATED, FOREST_BORDER, border_pt=1.3)
        add_text(s, cx + 0.24, 2.62, cw - 0.48, 0.28, tag, fs=10.2, bold=True, color=col)
        add_text(s, cx + 0.24, 2.98, cw - 0.48, 0.60, big, fs=26.5, bold=True, color=WHITE)
        add_text(s, cx + 0.24, 3.70, cw - 0.48, 1.56, desc, fs=12.0, color=MINT_TEXT, line_spacing=1.32)

    # Closing Q&A Banner
    add_box(s, 0.80, 5.85, 11.73, 1.00, FOREST_ELEVATED, YELLOW_BRIGHT, border_pt=1.4)
    add_text(s, 1.10, 6.02, 7.60, 0.36,
             "Trân trọng cảm ơn Giảng viên và các bạn đã lắng nghe!",
             fs=17, bold=True, color=YELLOW_BRIGHT)
    add_text(s, 1.10, 6.42, 7.60, 0.30,
             "Nhóm 20 · Phoutthavong Xayavong (23021941) & Vũ Quốc Long (23020105)",
             fs=12, bold=False, color=WHITE)
    add_pill(s, 9.75, 6.12, 2.50, 0.46, "THẢO LUẬN & HỎI ĐÁP", YELLOW_BRIGHT, FOREST_DARK, fs=11.5)


def main():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    build_slide_1_cover(prs, blank)
    build_slide_2_problem_scope(prs, blank)
    build_slide_3_work_system(prs, blank)
    build_slide_4_resource_map(prs, blank)
    build_slide_5_bpmn_as_is(prs, blank)
    build_slide_6_diagnosis_metrics(prs, blank)
    build_slide_7_milp_simpy_model(prs, blank)
    build_slide_8_bpmn_to_be(prs, blank)
    build_slide_9_comparison_results(prs, blank)
    build_slide_10_sensitivity_pareto(prs, blank)
    build_slide_11_roadmap_governance(prs, blank)
    build_slide_12_conclusion(prs, blank)

    prs.save(PPTX_PATH)
    print(f"Successfully generated 12-slide presentation: {PPTX_PATH}")


if __name__ == "__main__":
    main()
