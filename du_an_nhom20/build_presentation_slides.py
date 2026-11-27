"""
Projector-Optimized 12-Slide Native PowerPoint Deck (Group 20 - INT3501 CatPlus)
Designed specifically for standard classroom projectors:
  - Minimal text: concise keywords & numbers (no paragraphs, no small subtitles)
  - Large fonts everywhere: Titles 25-36pt, Headers 17-19pt, Body 15-16.5pt,
    Tables 13.5-14.5pt, Chart labels 12.5-14pt, KPI callouts 34-42pt.
  - High-contrast borders (1.8-2.2pt) in Forest Green, Warm Amber-Yellow, Vibrant Orange.
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

# --- HIGH-CONTRAST CLASSROOM PROJECTOR PALETTE (Green - Yellow - Orange) ---
FOREST_DARK     = RGBColor(12, 54, 40)     # #0C3628
FOREST_ELEVATED = RGBColor(22, 82, 62)     # #16523E
FOREST_BORDER   = RGBColor(52, 138, 106)   # #348A6A

GREEN_PRIMARY   = RGBColor(21, 128, 61)    # #15803D
GREEN_SOFT_BG   = RGBColor(232, 252, 241)  # #E8FCF1

YELLOW_BRIGHT   = RGBColor(251, 191, 36)   # #FBBF24
AMBER_PRIMARY   = RGBColor(217, 119, 6)    # #D97706 (Strong projector contrast!)
AMBER_CHART     = RGBColor(245, 158, 11)   # #F59E0B
AMBER_TEXT      = RGBColor(161, 72, 7)     # #A14807
YELLOW_SOFT_BG  = RGBColor(254, 249, 224)  # #FEF9E0

ORANGE_PRIMARY  = RGBColor(234, 88, 12)    # #EA580C
ORANGE_TEXT     = RGBColor(180, 52, 8)     # #B43408
ORANGE_SOFT_BG  = RGBColor(255, 241, 228)  # #FFF1E4

INK_DARK        = RGBColor(15, 32, 24)     # #0F2018
INK_MUTED       = RGBColor(65, 86, 76)     # #41564C
SURFACE_NEUTRAL = RGBColor(244, 247, 245)  # #F4F7F5
BORDER_STRONG   = RGBColor(168, 186, 177)  # #A8BAB1
WHITE           = RGBColor(255, 255, 255)
MINT_BRIGHT     = RGBColor(167, 243, 208)  # #A7F3D0
PEACH_BRIGHT    = RGBColor(253, 186, 116)  # #FDBA74

FONT_MAIN = "Arial"
TOTAL_SLIDES = 12


def set_bg(slide, color):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg


def add_box(slide, x, y, w, h, fill_rgb, border_rgb=None, border_pt=1.8, rounded=True):
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


def add_circle_badge(slide, x, y, d, text, fill_rgb, text_rgb=WHITE, fs=14):
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


def add_pill(slide, x, y, w, h, text, fill_rgb, text_rgb, border_rgb=None, fs=11.5):
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    if len(pill.adjustments) > 0:
        pill.adjustments[0] = 0.5
    pill.fill.solid()
    pill.fill.fore_color.rgb = fill_rgb
    if border_rgb is not None:
        pill.line.color.rgb = border_rgb
        pill.line.width = Pt(1.5)
    else:
        pill.line.fill.background()
    tf = pill.text_frame
    tf.word_wrap = False
    tf.margin_left = Inches(0.14)
    tf.margin_right = Inches(0.14)
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


def add_text(slide, x, y, w, h, text, fs=16, bold=False, color=INK_DARK,
             align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP, line_spacing=1.22):
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


def add_bullets(slide, x, y, w, h, items, fs=15.5, color=INK_DARK, space_after=8, bullet_char="• "):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for idx, item in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(space_after)
        p.line_spacing = 1.24
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
            r.font.bold = False
            r.font.color.rgb = color
    return tb


def add_slide_header(slide, slide_num, tag_text, tag_theme, title_text):
    """Big-font clean header: category pill + page badge + 25.5pt bold Action Title."""
    set_bg(slide, WHITE)
    if tag_theme == "orange":
        bg_c, tx_c, bd_c = ORANGE_SOFT_BG, ORANGE_TEXT, ORANGE_PRIMARY
    elif tag_theme == "yellow":
        bg_c, tx_c, bd_c = YELLOW_SOFT_BG, AMBER_TEXT, AMBER_PRIMARY
    else:
        bg_c, tx_c, bd_c = GREEN_SOFT_BG, GREEN_PRIMARY, GREEN_PRIMARY

    pill_w = max(2.3, len(tag_text) * 0.115 + 0.45)
    add_pill(slide, 0.60, 0.34, pill_w, 0.36, tag_text, bg_c, tx_c, bd_c, fs=11.0)
    add_pill(slide, 11.75, 0.34, 0.98, 0.36, f"{slide_num} / {TOTAL_SLIDES}",
             SURFACE_NEUTRAL, INK_DARK, BORDER_STRONG, fs=11.0)

    add_text(slide, 0.60, 0.82, 12.13, 0.54, title_text,
             fs=25.0, bold=True, color=FOREST_DARK, line_spacing=1.10)


def style_chart_projector(chart, show_legend=False, legend_pos=XL_LEGEND_POSITION.TOP):
    chart.has_title = False
    chart.font.name = FONT_MAIN
    chart.font.size = Pt(12.5)
    chart.has_legend = show_legend
    if show_legend:
        chart.legend.position = legend_pos
        chart.legend.include_in_layout = False
        chart.legend.font.name = FONT_MAIN
        chart.legend.font.size = Pt(12.0)
        chart.legend.font.bold = True

    val_axis = chart.value_axis
    val_axis.minimum_scale = 0.0
    val_axis.has_major_gridlines = True
    val_axis.major_gridlines.format.line.color.rgb = BORDER_STRONG
    val_axis.major_gridlines.format.line.width = Pt(0.9)
    val_axis.format.line.fill.background()
    val_axis.tick_labels.font.name = FONT_MAIN
    val_axis.tick_labels.font.size = Pt(11.5)
    val_axis.tick_labels.font.bold = True
    val_axis.tick_labels.font.color.rgb = INK_MUTED

    cat_axis = chart.category_axis
    cat_axis.has_major_gridlines = False
    cat_axis.format.line.color.rgb = INK_MUTED
    cat_axis.tick_labels.font.name = FONT_MAIN
    cat_axis.tick_labels.font.size = Pt(12.5)
    cat_axis.tick_labels.font.bold = True
    cat_axis.tick_labels.font.color.rgb = INK_DARK


# ==============================================================================
# 12 PROJECTOR-READY SLIDES
# ==============================================================================

def build_slide_1_cover(prs, blank):
    s = prs.slides.add_slide(blank)
    set_bg(s, FOREST_DARK)

    c1 = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(10.3), Inches(-1.2), Inches(4.5), Inches(4.5))
    c1.fill.solid()
    c1.fill.fore_color.rgb = FOREST_ELEVATED
    c1.line.fill.background()

    add_pill(s, 0.75, 0.75, 5.55, 0.42,
             "INT3501 · KHOA HỌC DỊCH VỤ · ĐH CÔNG NGHỆ",
             FOREST_ELEVATED, YELLOW_BRIGHT, YELLOW_BRIGHT, fs=12.0)

    add_text(s, 0.75, 1.55, 7.60, 2.55,
             "Tối ưu ghép đôi\ngia sư – học viên và xếp lịch\ntrên nền tảng CatPlus",
             fs=36, bold=True, color=WHITE, line_spacing=1.18)

    add_text(s, 0.75, 4.25, 7.40, 0.75,
             "Quy hoạch nguyên gom nhóm (MILP) kết hợp mô phỏng hàng đợi SimPy",
             fs=17, bold=True, color=MINT_BRIGHT, line_spacing=1.25)

    add_box(s, 0.75, 5.35, 7.45, 1.42, FOREST_ELEVATED, YELLOW_BRIGHT, border_pt=1.8)
    add_pill(s, 1.00, 5.58, 1.45, 0.36, "NHÓM 20", YELLOW_BRIGHT, FOREST_DARK, fs=12.0)
    add_text(s, 1.00, 6.12, 7.00, 0.46,
             "Phoutthavong Xayavong (23021941)  ·  Vũ Quốc Long (23020105)",
             fs=15.5, bold=True, color=WHITE)

    # 3 Giant KPI Preview Cards
    highlights = [
        ("92,7%", "Tỷ lệ ghép lớp (+32,3%)", YELLOW_BRIGHT),
        ("−54,4%", "Thời gian chờ (còn 10,3 giờ)", MINT_BRIGHT),
        ("99,3%", "Chốt xong trong 2 ngày", PEACH_BRIGHT),
    ]
    for idx, (val, lbl, col) in enumerate(highlights):
        cy = 1.25 + idx * 1.92
        add_box(s, 8.65, cy, 4.00, 1.65, FOREST_ELEVATED, FOREST_BORDER, border_pt=1.8)
        add_text(s, 8.95, cy + 0.18, 3.50, 0.72, val, fs=36, bold=True, color=col)
        add_text(s, 8.95, cy + 0.98, 3.50, 0.48, lbl, fs=16.0, bold=True, color=WHITE)


def build_slide_2_problem_scope(prs, blank):
    s = prs.slides.add_slide(blank)
    add_slide_header(
        s, 2, "01 · BÀI TOÁN & PHẠM VI", "orange",
        "Xếp lịch thủ công đang làm nghẽn lớp nhóm tại CatPlus"
    )

    # Top row: 3 Bold Scope Cards
    stages = [
        ("ĐẦU VÀO TUYỂN SINH",
         ["60 học viên mới / tháng", "Cấp THCS (55%) & THPT (45%)", "14 khung giờ học / tuần"],
         YELLOW_SOFT_BG, AMBER_PRIMARY, AMBER_TEXT),
        ("QUY TẮC LỚP & NGUỒN LỰC",
         ["Lớp 1–1: Đúng 1 học viên", "Lớp Nhóm: Bắt buộc 3–5 em cùng cấp", "10 Gia sư · 2 CSKH · 1 Quản lý"],
         GREEN_SOFT_BG, GREEN_PRIMARY, GREEN_PRIMARY),
        ("CÁCH LÀM HIỆN TẠI (AS-IS)",
         ["CSKH chỉ hỏi 1 khung giờ đầu", "Nhắn Zalo hỏi từng gia sư", "Xếp tay tuần tự từng người"],
         ORANGE_SOFT_BG, ORANGE_PRIMARY, ORANGE_TEXT),
    ]
    cw = 3.75
    gap = 0.44
    for idx, (hdr, items, bg_c, bd_c, tx_c) in enumerate(stages):
        cx = 0.60 + idx * (cw + gap)
        add_box(s, cx, 1.58, cw, 2.45, bg_c, bd_c, border_pt=2.0)
        add_text(s, cx + 0.22, 1.76, cw - 0.44, 0.38, hdr, fs=16.0, bold=True, color=tx_c)
        add_bullets(s, cx + 0.22, 2.26, cw - 0.44, 1.65, items, fs=15.0, color=INK_DARK, space_after=8)

    for ax_x in [4.42, 8.61]:
        arr = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(ax_x), Inches(2.62), Inches(0.30), Inches(0.32))
        arr.fill.solid()
        arr.fill.fore_color.rgb = AMBER_PRIMARY
        arr.line.fill.background()

    # Bottom row: 3 Core Research Questions / KPIs
    add_text(s, 0.60, 4.24, 12.1, 0.36, "BA CÂU HỎI NGHIÊN CỨU & CHỈ SỐ ĐO LƯỜNG TRỌNG TÂM",
             fs=14.5, bold=True, color=INK_MUTED)

    kpis = [
        ("Q1", "Tỷ lệ ghép lớp (%)",
         "Tăng thêm bao nhiêu % học viên vào lớp?\nCần hỏi tối thiểu mấy khung giờ?",
         GREEN_PRIMARY, GREEN_SOFT_BG),
        ("Q2", "Độ phù hợp lịch (0–100)",
         "Đánh đổi ra sao giữa điểm ưu tiên cá nhân\nvà điểm hợp lịch toàn trung tâm?",
         AMBER_PRIMARY, YELLOW_SOFT_BG),
        ("Q3", "Thời gian chờ & Độ bận",
         "Giảm bao nhiêu giờ chờ (W, P90, ≤ 16h)\nvà giảm bao nhiêu % tải cho Quản lý?",
         ORANGE_PRIMARY, ORANGE_SOFT_BG),
    ]
    kw = 3.86
    kgap = 0.27
    for idx, (num, ttl, desc, col_c, bg_c) in enumerate(kpis):
        kx = 0.60 + idx * (kw + kgap)
        add_box(s, kx, 4.68, kw, 2.35, bg_c, col_c, border_pt=2.0)
        add_circle_badge(s, kx + 0.22, 4.90, 0.50, num, col_c, WHITE, fs=14)
        add_text(s, kx + 0.85, 4.96, kw - 1.05, 0.42, ttl, fs=17.5, bold=True, color=FOREST_DARK)
        add_text(s, kx + 0.22, 5.62, kw - 0.44, 1.25, desc, fs=15.0, color=INK_DARK, line_spacing=1.30)


def build_slide_3_work_system(prs, blank):
    s = prs.slides.add_slide(blank)
    add_slide_header(
        s, 3, "02 · HỆ THỐNG DỊCH VỤ", "yellow",
        "Khung Work System chỉ ra 4 lỗi cấu trúc gây rớt lớp nhóm"
    )

    # Left: Clean visual 9-block Work System diagram (large bold labels!)
    add_box(s, 0.60, 1.56, 6.15, 5.48, SURFACE_NEUTRAL, BORDER_STRONG, border_pt=1.8)
    add_text(s, 0.85, 1.72, 5.65, 0.36, "9 THÀNH PHẦN WORK SYSTEM TẠI CATPLUS",
             fs=14.5, bold=True, color=FOREST_DARK)

    # Top pair
    add_box(s, 0.85, 2.20, 2.72, 1.22, YELLOW_SOFT_BG, AMBER_PRIMARY, border_pt=1.8)
    add_text(s, 1.00, 2.34, 2.42, 0.34, "1. Khách hàng", fs=15.5, bold=True, color=AMBER_TEXT)
    add_text(s, 1.00, 2.72, 2.42, 0.58, "Học sinh & Phụ huynh", fs=14.0, color=INK_DARK)

    add_box(s, 3.78, 2.20, 2.72, 1.22, GREEN_SOFT_BG, GREEN_PRIMARY, border_pt=1.8)
    add_text(s, 3.93, 2.34, 2.42, 0.34, "2. Dịch vụ đầu ra", fs=15.5, bold=True, color=GREEN_PRIMARY)
    add_text(s, 3.93, 2.72, 2.42, 0.58, "Lớp 1–1 & Nhóm 3–5 em", fs=14.0, color=INK_DARK)

    # Middle 2x2 core
    mid = [
        ("3. Quy trình", "Hỏi giờ → Dò lịch → Chốt"),
        ("4. Con người", "2 CSKH · 1 QL · 10 Gia sư"),
        ("5. Thông tin", "Giờ rảnh trò & ca trống thầy"),
        ("6. Công nghệ", "Web nội bộ · Zalo / ĐT"),
    ]
    for idx, (m_t, m_s) in enumerate(mid):
        col = idx % 2
        row = idx // 2
        mx = 0.85 + col * 2.93
        my = 3.58 + row * 1.04
        add_box(s, mx, my, 2.72, 0.92, WHITE, BORDER_STRONG, border_pt=1.5)
        add_text(s, mx + 0.14, my + 0.12, 2.45, 0.32, m_t, fs=15.0, bold=True, color=FOREST_DARK)
        add_text(s, mx + 0.14, my + 0.46, 2.45, 0.38, m_s, fs=13.5, color=INK_MUTED)

    # Bottom 3 foundation blocks
    fnd = ["7. Chiến lược", "8. Môi trường", "9. Hạ tầng"]
    for idx, f_lbl in enumerate(fnd):
        fx = 0.85 + idx * 1.91
        add_box(s, fx, 5.82, 1.82, 0.96, GREEN_SOFT_BG, GREEN_PRIMARY, border_pt=1.5)
        add_text(s, fx + 0.08, 5.88, 1.66, 0.84, f_lbl, fs=14.5, bold=True,
                 color=FOREST_DARK, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    # Right: 4 Bold System Failure Cards
    add_text(s, 7.00, 1.56, 5.70, 0.36, "4 ĐIỂM LỖI HỆ THỐNG CẦN THÁO GỠ",
             fs=14.5, bold=True, color=ORANGE_TEXT)

    errs = [
        ("01", "Lỗi thông tin", "Chỉ hỏi 1 khung giờ; lịch gia sư tản mát trên Zalo"),
        ("02", "Lỗi hoạt động", "Xếp lẻ từng ca → nhóm bị rải mỏng 1–2 em (< 3)"),
        ("03", "Lỗi công nghệ", "Phần mềm chỉ lưu hậu kiểm, thiếu gợi ý gom nhóm"),
        ("04", "Lỗi thiết chế", "Thiếu nhịp gom đợt & phương án gia sư dự phòng"),
    ]
    for idx, (code, ettl, edesc) in enumerate(errs):
        ey = 2.02 + idx * 1.27
        add_box(s, 7.00, ey, 5.73, 1.13, ORANGE_SOFT_BG, ORANGE_PRIMARY, border_pt=2.0)
        add_circle_badge(s, 7.20, ey + 0.30, 0.50, code, ORANGE_PRIMARY, WHITE, fs=14)
        add_text(s, 7.85, ey + 0.14, 4.70, 0.36, ettl, fs=17.0, bold=True, color=ORANGE_TEXT)
        add_text(s, 7.85, ey + 0.54, 4.70, 0.48, edesc, fs=14.5, color=INK_DARK)


def build_slide_4_resource_map(prs, blank):
    s = prs.slides.add_slide(blank)
    add_slide_header(
        s, 4, "03 · BẢN ĐỒ NGUỒN LỰC", "yellow",
        "Bản đồ nguồn lực và cơ chế đồng tạo giá trị"
    )

    img_path = os.path.join(OUT_DIR, "slide_fig_resource_map.png")
    add_box(s, 0.60, 1.54, 8.35, 5.52, WHITE, BORDER_STRONG, border_pt=1.8)
    s.shapes.add_picture(img_path, Inches(0.70), Inches(1.62), width=Inches(8.15))

    cards = [
        ("TÀI NGUYÊN TOÁN HẠNG", GREEN_PRIMARY, GREEN_SOFT_BG,
         ["Hồ sơ học viên & cấp học", "14 khung giờ học / tuần"]),
        ("TÀI NGUYÊN TOÁN TỬ", AMBER_PRIMARY, YELLOW_SOFT_BG,
         ["Kỹ năng CSKH & Quản lý", "10 Gia sư + Thuật toán MILP"]),
        ("CHUỖI TẠO GIÁ TRỊ", ORANGE_PRIMARY, ORANGE_SOFT_BG,
         ["Đầu ra: Mã lớp hợp lệ", "Kết quả: Đúng nhóm, ít chờ"]),
    ]
    for idx, (hdr, col_c, bg_c, items) in enumerate(cards):
        cy = 1.54 + idx * 1.88
        add_box(s, 9.15, cy, 3.58, 1.74, bg_c, col_c, border_pt=2.0)
        add_pill(s, 9.33, cy + 0.16, 2.85, 0.34, hdr, col_c, WHITE, fs=10.8)
        add_bullets(s, 9.33, cy + 0.64, 3.24, 1.00, items, fs=15.0, color=INK_DARK, space_after=6)


def build_slide_5_bpmn_as_is(prs, blank):
    s = prs.slides.add_slide(blank)
    add_slide_header(
        s, 5, "04 · QUY TRÌNH BPMN AS-IS", "orange",
        "Quy trình hiện tại: Chờ Zalo và vòng lặp hỏi đổi lịch"
    )

    img_path = os.path.join(OUT_DIR, "slide_fig_bpmn_as_is.png")
    add_box(s, 0.60, 1.50, 12.13, 4.65, WHITE, BORDER_STRONG, border_pt=1.8)
    s.shapes.add_picture(img_path, Inches(0.72), Inches(1.56), width=Inches(11.88))

    pills = [
        ("1. Chuyển giao", "Chỉ lấy 1 khung giờ", YELLOW_SOFT_BG, AMBER_PRIMARY, AMBER_TEXT),
        ("2. Chờ đợi", "Đợi Zalo 2,5–7,5 giờ", ORANGE_SOFT_BG, ORANGE_PRIMARY, ORANGE_TEXT),
        ("3. Nghẽn nhóm", "Kẹt lẻ 1–2 em (< 3)", ORANGE_SOFT_BG, ORANGE_PRIMARY, ORANGE_TEXT),
        ("4. Làm lại", "Đổi giờ tối đa 2 vòng", YELLOW_SOFT_BG, AMBER_PRIMARY, AMBER_TEXT),
    ]
    pw = 2.88
    gap = 0.20
    for idx, (pttl, psub, bg_c, bd_c, tx_c) in enumerate(pills):
        px = 0.60 + idx * (pw + gap)
        add_box(s, px, 6.26, pw, 0.88, bg_c, bd_c, border_pt=1.8)
        add_text(s, px + 0.16, 6.34, pw - 0.32, 0.34, pttl, fs=15.5, bold=True, color=tx_c)
        add_text(s, px + 0.16, 6.70, pw - 0.32, 0.34, psub, fs=14.0, bold=False, color=INK_DARK)


def build_slide_6_diagnosis_metrics(prs, blank):
    s = prs.slides.add_slide(blank)
    add_slide_header(
        s, 6, "05 · CHẨN ĐOÁN ĐỊNH LƯỢNG", "orange",
        "Chặng dò lịch chiếm 69,4% giờ chờ — 39,6% hồ sơ bị rớt"
    )

    # Left: Big Horizontal Bar Chart
    add_box(s, 0.60, 1.54, 6.80, 5.52, WHITE, BORDER_STRONG, border_pt=1.8)
    add_text(s, 0.85, 1.72, 6.30, 0.38,
             "THỜI GIAN TỪNG CHẶNG (TỔNG W = 22,56 GIỜ ≈ 2,8 NGÀY)",
             fs=14.5, bold=True, color=FOREST_DARK)

    chart_data = CategoryChartData()
    chart_data.categories = [
        "3. Chốt nhập học (22%)",
        "2. Dò lịch & đổi giờ (69%)",
        "1. Gọi tư vấn đầu (9%)",
    ]
    chart_data.add_series("Giờ", (4.96, 15.66, 1.95))

    gf = s.shapes.add_chart(
        XL_CHART_TYPE.BAR_CLUSTERED,
        Inches(0.80), Inches(2.20), Inches(6.40), Inches(3.65),
        chart_data
    )
    ch = gf.chart
    style_chart_projector(ch, show_legend=False)
    ch.value_axis.maximum_scale = 20.0

    plot = ch.plots[0]
    plot.gap_width = 75
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    dl.number_format = '0.00"h"'
    dl.font.name = FONT_MAIN
    dl.font.size = Pt(14.0)
    dl.font.bold = True
    dl.font.color.rgb = INK_DARK

    for idx_pt, col_rgb in enumerate([GREEN_PRIMARY, ORANGE_PRIMARY, AMBER_CHART]):
        pt = plot.series[0].points[idx_pt]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = col_rgb

    add_box(s, 0.85, 6.02, 6.30, 0.82, ORANGE_SOFT_BG, ORANGE_PRIMARY, border_pt=1.8)
    add_text(s, 1.05, 6.14, 5.90, 0.58,
             "Điểm nghẽn nằm ở chờ Zalo & đổi giờ (15,66h), không phải do CSKH!",
             fs=14.5, bold=True, color=ORANGE_TEXT, valign=MSO_ANCHOR.MIDDLE)

    # Right: 2x2 Giant Stat Callouts
    stats = [
        ("39,6%", "Học viên rớt lớp", "17,5 / 23,8 ca do thiếu nhóm", ORANGE_PRIMARY, ORANGE_SOFT_BG),
        ("18,0%", "Xong ≤ 2 ngày", "P90 kéo dài tới 31,3 giờ", ORANGE_PRIMARY, ORANGE_SOFT_BG),
        ("49,7%", "Quỹ giờ Quản lý", "Mất nửa ngày dò lịch tay", AMBER_PRIMARY, YELLOW_SOFT_BG),
        ("5,64 ca", "Hồ sơ tồn đọng TB", "Định luật Little (L = λW)", GREEN_PRIMARY, GREEN_SOFT_BG),
    ]
    sw, sh = 2.48, 2.64
    for idx, (big_num, st_ttl, st_sub, col_c, bg_c) in enumerate(stats):
        col = idx % 2
        row = idx // 2
        sx = 7.62 + col * (sw + 0.15)
        sy = 1.54 + row * (sh + 0.24)
        add_box(s, sx, sy, sw, sh, bg_c, col_c, border_pt=2.0)
        add_text(s, sx + 0.18, sy + 0.22, sw - 0.36, 0.82, big_num, fs=36, bold=True, color=col_c)
        add_text(s, sx + 0.18, sy + 1.16, sw - 0.36, 0.46, st_ttl, fs=16.5, bold=True, color=FOREST_DARK)
        add_text(s, sx + 0.18, sy + 1.72, sw - 0.36, 0.72, st_sub, fs=14.0, color=INK_DARK, line_spacing=1.22)


def build_slide_7_milp_simpy_model(prs, blank):
    s = prs.slides.add_slide(blank)
    add_slide_header(
        s, 7, "06 · MÔ HÌNH TỐI ƯU & MÔ PHỎNG", "green",
        "Kết hợp Quy hoạch nguyên MILP & Mô phỏng hàng đợi SimPy"
    )

    # Column 1: Inputs
    add_box(s, 0.60, 1.54, 3.65, 5.52, YELLOW_SOFT_BG, AMBER_PRIMARY, border_pt=2.0)
    add_circle_badge(s, 0.82, 1.76, 0.50, "01", AMBER_PRIMARY, WHITE, fs=14)
    add_text(s, 1.44, 1.84, 2.65, 0.42, "Đầu vào chuẩn", fs=18.5, bold=True, color=FOREST_DARK)
    add_bullets(s, 0.82, 2.52, 3.22, 4.30, [
        "Quy mô: 60 học viên & 10 gia sư / tháng",
        "Hỏi lịch: Tối đa 3 khung giờ rảnh / em",
        "Điểm hợp lịch: 100 · 80 · 60 điểm",
        "Trần gia sư: Tối đa 3–5 lớp / người",
    ], fs=15.5, color=INK_DARK, space_after=14)

    # Column 2: MILP
    add_box(s, 4.45, 1.54, 4.42, 5.52, GREEN_SOFT_BG, GREEN_PRIMARY, border_pt=2.4)
    add_circle_badge(s, 4.67, 1.76, 0.50, "02", GREEN_PRIMARY, WHITE, fs=14)
    add_text(s, 5.30, 1.84, 3.40, 0.42, "Tối ưu MILP", fs=18.5, bold=True, color=FOREST_DARK)

    add_box(s, 4.67, 2.46, 3.98, 1.22, WHITE, GREEN_PRIMARY, border_pt=1.5)
    add_text(s, 4.85, 2.56, 3.62, 0.30, "BIẾN NHỊ PHÂN {0, 1}", fs=12.5, bold=True, color=GREEN_PRIMARY)
    add_text(s, 4.85, 2.92, 3.62, 0.66, "Ghép lớp x  ·  Mở lớp y  ·  Lớp ảo u", fs=15.0, bold=True, color=INK_DARK)

    add_box(s, 4.67, 3.84, 3.98, 1.32, FOREST_DARK, FOREST_DARK, border_pt=1.5)
    add_text(s, 4.85, 3.94, 3.62, 0.30, "HÀM MỤC TIÊU", fs=12.5, bold=True, color=YELLOW_BRIGHT)
    add_text(s, 4.85, 4.32, 3.62, 0.72, "min Z = 1000·∑u − ∑w·x + γ·∑y", fs=16.0, bold=True, color=WHITE)

    add_box(s, 4.67, 5.32, 3.98, 1.52, WHITE, ORANGE_PRIMARY, border_pt=1.8)
    add_text(s, 4.85, 5.42, 3.62, 0.30, "KHÓA CỨNG SĨ SỐ NHÓM", fs=12.5, bold=True, color=ORANGE_TEXT)
    add_text(s, 4.85, 5.80, 3.62, 0.92, "3 · y  ≤  ∑ x  ≤  5 · y\n(Thời gian giải < 0,5 giây)", fs=16.0, bold=True, color=INK_DARK)

    # Column 3: SimPy
    add_box(s, 9.07, 1.54, 3.66, 5.52, ORANGE_SOFT_BG, ORANGE_PRIMARY, border_pt=2.0)
    add_circle_badge(s, 9.29, 1.76, 0.50, "03", ORANGE_PRIMARY, WHITE, fs=14)
    add_text(s, 9.91, 1.84, 2.65, 0.42, "Hàng đợi SimPy", fs=18.5, bold=True, color=FOREST_DARK)
    add_bullets(s, 9.29, 2.52, 3.22, 4.30, [
        "Mô phỏng: Vòng lặp đổi giờ & gom đợt",
        "Nhịp chạy: 2 đợt/ngày (11h30 & 17h30)",
        "Thực tế: Tính cả 8% gia sư bận đột xuất",
        "Kiểm chứng: 20 chu kỳ tháng (seed = 42)",
    ], fs=15.5, color=INK_DARK, space_after=14)


def build_slide_8_bpmn_to_be(prs, blank):
    s = prs.slides.add_slide(blank)
    add_slide_header(
        s, 8, "07 · QUY TRÌNH CẢI TIẾN (TO-BE)", "green",
        "Quy trình TO-BE: Gợi ý MILP 2 đợt/ngày — Duyệt trong 1 vòng"
    )

    img_path = os.path.join(OUT_DIR, "slide_fig_bpmn_to_be.png")
    add_box(s, 0.60, 1.50, 12.13, 3.92, WHITE, BORDER_STRONG, border_pt=1.8)
    s.shapes.add_picture(img_path, Inches(0.72), Inches(1.56), width=Inches(11.88))

    rules = [
        ("Đủ nhóm 3–5 / Lớp 1–1", "Quản lý bấm duyệt ngay vòng 1",
         GREEN_SOFT_BG, GREEN_PRIMARY, GREEN_PRIMARY),
        ("Gia sư bận đột xuất (8%)", "Chọn ngay gia sư dự phòng số 2",
         YELLOW_SOFT_BG, AMBER_PRIMARY, AMBER_TEXT),
        ("Nhóm mới có 2 học viên", "Giữ chờ thêm 1 đợt (nửa ngày)",
         YELLOW_SOFT_BG, AMBER_PRIMARY, AMBER_TEXT),
        ("Rơi vào lớp ảo (u = 1)", "Gọi thương lượng giờ ngay ngày đầu",
         ORANGE_SOFT_BG, ORANGE_PRIMARY, ORANGE_TEXT),
    ]
    rw = 2.88
    gap = 0.20
    for idx, (r_ttl, r_desc, bg_c, bd_c, tx_c) in enumerate(rules):
        rx = 0.60 + idx * (rw + gap)
        add_box(s, rx, 5.58, rw, 1.50, bg_c, bd_c, border_pt=2.0)
        add_text(s, rx + 0.16, 5.72, rw - 0.32, 0.50, r_ttl, fs=15.5, bold=True, color=tx_c, line_spacing=1.18)
        add_text(s, rx + 0.16, 6.32, rw - 0.32, 0.64, r_desc, fs=14.2, color=INK_DARK, line_spacing=1.20)


def build_slide_9_comparison_results(prs, blank):
    s = prs.slides.add_slide(blank)
    add_slide_header(
        s, 9, "08 · KẾT QUẢ ĐỐI CHỨNG", "green",
        "TO-BE tăng ghép lớp lên 92,7% và giảm 54,4% thời gian chờ"
    )

    # Top 4 Big Hero KPI Cards
    cards = [
        ("92,7%", "Tỷ lệ ghép lớp", "Tăng +32,3% (từ 60,4%)", GREEN_PRIMARY, GREEN_SOFT_BG),
        ("86,5 đ", "Hợp lịch chung", "Tăng +28,0 đ (từ 58,5 đ)", AMBER_PRIMARY, YELLOW_SOFT_BG),
        ("10,29h", "Giờ chờ TB", "Giảm 54,4% (từ 22,56h)", GREEN_PRIMARY, GREEN_SOFT_BG),
        ("8,7%", "Độ bận Quản lý", "Giảm sâu từ 49,7%", ORANGE_PRIMARY, ORANGE_SOFT_BG),
    ]
    cw = 2.88
    gap = 0.20
    for idx, (val, ttl, sub, col_c, bg_c) in enumerate(cards):
        cx = 0.60 + idx * (cw + gap)
        add_box(s, cx, 1.52, cw, 1.72, bg_c, col_c, border_pt=2.0)
        add_text(s, cx + 0.18, 1.62, cw - 0.36, 0.68, val, fs=34, bold=True, color=col_c)
        add_text(s, cx + 0.18, 2.34, cw - 0.36, 0.38, ttl, fs=16.0, bold=True, color=FOREST_DARK)
        add_text(s, cx + 0.18, 2.74, cw - 0.36, 0.38, sub, fs=13.8, bold=True, color=INK_MUTED)

    # Bottom Left: Big Grouped Column Chart
    add_box(s, 0.60, 3.42, 6.25, 3.68, WHITE, BORDER_STRONG, border_pt=1.8)

    c_data = CategoryChartData()
    c_data.categories = ["Ghép lớp (%)", "Hợp lịch (đ)", "Xong ≤ 16h (%)"]
    c_data.add_series("AS-IS", (60.4, 58.5, 18.0))
    c_data.add_series("TO-BE (2 ca)", (87.8, 82.7, 98.8))
    c_data.add_series("TO-BE (3 ca)", (92.7, 86.5, 99.3))

    gf = s.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED,
        Inches(0.75), Inches(3.55), Inches(5.95), Inches(3.42),
        c_data
    )
    ch = gf.chart
    style_chart_projector(ch, show_legend=True, legend_pos=XL_LEGEND_POSITION.TOP)
    ch.value_axis.maximum_scale = 118.0
    plot = ch.plots[0]
    plot.gap_width = 95
    plot.overlap = -12
    plot.has_data_labels = True
    plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    plot.data_labels.number_format = "0.0"
    plot.data_labels.font.name = FONT_MAIN
    plot.data_labels.font.size = Pt(12.0)
    plot.data_labels.font.bold = True

    for s_idx, col_rgb in enumerate([ORANGE_PRIMARY, AMBER_CHART, GREEN_PRIMARY]):
        ser = plot.series[s_idx]
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = col_rgb

    # Bottom Right: Big-Font 6-row Table (14pt!)
    add_box(s, 7.05, 3.42, 5.68, 3.68, WHITE, BORDER_STRONG, border_pt=1.8)
    rows_data = [
        ["Chỉ số", "AS-IS", "MILP 1 ca", "MILP 3 ca"],
        ["Ghép lớp", "60,4%", "58,3%", "92,7%"],
        ["Rớt / tháng", "23,8 ca", "25,0 ca", "4,4 ca"],
        ["Hợp lịch đỗ", "96,8 đ", "100,0 đ", "93,3 đ"],
        ["Giờ chờ TB", "22,6h", "9,7h", "10,3h"],
        ["Chờ P90", "31,3h", "12,8h", "13,2h"],
    ]
    tbl_shp = s.shapes.add_table(len(rows_data), 4, Inches(7.22), Inches(3.60), Inches(5.34), Inches(3.32))
    tbl = tbl_shp.table
    for c_i, w_val in enumerate([Inches(1.74), Inches(1.15), Inches(1.20), Inches(1.25)]):
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
            run.font.size = Pt(13.8)
            run.font.bold = (r_i == 0 or c_i in (0, 3))
            if r_i == 0:
                run.font.color.rgb = WHITE
            elif c_i == 3:
                run.font.color.rgb = GREEN_PRIMARY
            elif c_i == 1 and r_i in (1, 2, 4):
                run.font.color.rgb = ORANGE_TEXT
            else:
                run.font.color.rgb = INK_DARK


def build_slide_10_sensitivity_pareto(prs, blank):
    s = prs.slides.add_slide(blank)
    add_slide_header(
        s, 10, "09 · ĐỘ NHẠY & PARETO", "yellow",
        "Cần hỏi từ 2 khung giờ; hiệu quả bền vững khi thiếu gia sư"
    )

    # Left: Sensitivity Chart + 2 Bold Takeaways
    add_box(s, 0.60, 1.54, 5.95, 5.52, WHITE, BORDER_STRONG, border_pt=1.8)
    add_text(s, 0.82, 1.70, 5.50, 0.36, "TỶ LỆ GHÉP THEO SỐ CA HỎI & SỐ GIA SƯ (%)",
             fs=14.2, bold=True, color=FOREST_DARK)

    s_data = CategoryChartData()
    s_data.categories = ["1 ca", "2 ca", "3 ca", "6 GS", "10 GS", "12 GS"]
    s_data.add_series("AS-IS", (60.8, 60.8, 60.8, 50.1, 63.1, 62.2))
    s_data.add_series("TO-BE", (58.3, 87.8, 92.1, 75.3, 93.9, 91.9))

    gf1 = s.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED,
        Inches(0.75), Inches(2.10), Inches(5.65), Inches(3.48),
        s_data
    )
    ch1 = gf1.chart
    style_chart_projector(ch1, show_legend=True, legend_pos=XL_LEGEND_POSITION.TOP)
    ch1.value_axis.maximum_scale = 115.0
    p1 = ch1.plots[0]
    p1.gap_width = 85
    p1.overlap = -10
    p1.has_data_labels = True
    p1.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    p1.data_labels.number_format = "0"
    p1.data_labels.font.name = FONT_MAIN
    p1.data_labels.font.size = Pt(11.8)
    p1.data_labels.font.bold = True

    p1.series[0].format.fill.solid()
    p1.series[0].format.fill.fore_color.rgb = ORANGE_PRIMARY
    p1.series[1].format.fill.solid()
    p1.series[1].format.fill.fore_color.rgb = GREEN_PRIMARY

    add_box(s, 0.82, 5.70, 5.50, 1.16, GREEN_SOFT_BG, GREEN_PRIMARY, border_pt=1.8)
    add_bullets(s, 1.00, 5.80, 5.15, 0.98, [
        "Hỏi 1 ca: Chỉ đạt 58%  →  Hỏi 2–3 ca: Vọt lên 88–92%",
        "6 gia sư + MILP (75%)  >  12 gia sư xếp tay (62%)",
    ], fs=14.0, color=INK_DARK, space_after=6)

    # Right: Big-Font Pareto Table + 3 Short Trade-offs
    add_box(s, 6.75, 1.54, 5.98, 5.52, WHITE, BORDER_STRONG, border_pt=1.8)
    add_text(s, 6.98, 1.70, 5.50, 0.36, "ĐƯỜNG BIÊN PARETO THEO CHI PHÍ MỞ CA (γ)",
             fs=14.2, bold=True, color=FOREST_DARK)

    p_rows = [
        ["Trọng số γ", "Ca mở", "Ghép lớp", "Chính sách"],
        ["γ = 10", "33,3", "91,3%", "Tối đa nhận lớp (Đề xuất)"],
        ["γ = 1.065", "32,2", "89,4%", "Bỏ lớp 1–1 ưu tiên 3"],
        ["γ = 1.085", "29,7", "85,3%", "Dồn nhóm 4–5 em (Cao điểm)"],
        ["γ = 1.105", "8,9", "50,7%", "Chỉ mở lớp nhóm đông"],
    ]
    ptbl_s = s.shapes.add_table(len(p_rows), 4, Inches(6.95), Inches(2.16), Inches(5.58), Inches(2.50))
    ptbl = ptbl_s.table
    for ci, wv in enumerate([Inches(1.30), Inches(0.95), Inches(1.10), Inches(2.23)]):
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
            rn.font.size = Pt(13.2)
            rn.font.bold = (ri in (0, 1))
            rn.font.color.rgb = WHITE if ri == 0 else (GREEN_PRIMARY if ri == 1 and ci < 3 else INK_DARK)

    add_box(s, 6.95, 4.82, 5.58, 2.04, YELLOW_SOFT_BG, AMBER_PRIMARY, border_pt=1.8)
    add_text(s, 7.15, 4.92, 5.20, 0.34, "3 ĐÁNH ĐỔI VẬN HÀNH", fs=14.2, bold=True, color=AMBER_TEXT)
    add_bullets(s, 7.15, 5.30, 5.20, 1.48, [
        "Gọi đầu +3–5 phút  →  Xóa gọi đổi lịch nhiều ngày",
        "Đợi gom đợt nửa ngày  →  Tổng chờ vẫn giảm 54,4%",
        "Giảm 3,5 điểm cá nhân  →  Cứu thêm +32,3% học viên",
    ], fs=13.8, color=INK_DARK, space_after=6)


def build_slide_11_roadmap_governance(prs, blank):
    s = prs.slides.add_slide(blank)
    add_slide_header(
        s, 11, "10 · TRIỂN KHAI & GIÁM SÁT", "green",
        "Lộ trình 2 giai đoạn không tăng nhân sự & Minh bạch dữ liệu"
    )

    # Left: 2-Step Roadmap + 4 BSC Cards
    add_box(s, 0.60, 1.54, 6.00, 2.72, GREEN_SOFT_BG, GREEN_PRIMARY, border_pt=2.0)
    add_circle_badge(s, 0.84, 1.78, 0.48, "B1", AMBER_PRIMARY, WHITE, fs=13)
    add_text(s, 1.46, 1.76, 4.95, 0.36, "Tuần 1–2: Chuẩn hóa dữ liệu đầu vào", fs=16.5, bold=True, color=AMBER_TEXT)
    add_text(s, 1.46, 2.16, 4.95, 0.64, "Form hỏi 2–3 khung giờ & bảng ca trống gia sư đầu tuần", fs=14.8, color=INK_DARK)

    add_circle_badge(s, 0.84, 3.00, 0.48, "B2", GREEN_PRIMARY, WHITE, fs=13)
    add_text(s, 1.46, 2.98, 4.95, 0.36, "Từ tuần 3: Chạy gợi ý MILP song song", fs=16.5, bold=True, color=GREEN_PRIMARY)
    add_text(s, 1.46, 3.38, 4.95, 0.64, "Nhúng nút gợi ý 11h30 & 17h30; đối chứng thực tế 1 tháng", fs=14.8, color=INK_DARK)

    add_text(s, 0.60, 4.44, 6.00, 0.34, "4 GÓC NHÌN GIÁM SÁT (BALANCED SCORECARD)",
             fs=14.2, bold=True, color=FOREST_DARK)
    bsc = [
        ("Tài chính", "Sĩ số nhóm ≥ 3,8 em/lớp", YELLOW_SOFT_BG, AMBER_PRIMARY, AMBER_TEXT),
        ("Khách hàng", "Ghép 92,7% · SLA ≤ 16h", GREEN_SOFT_BG, GREEN_PRIMARY, GREEN_PRIMARY),
        ("Quy trình", "Độ bận Quản lý ~8,7%", SURFACE_NEUTRAL, BORDER_STRONG, FOREST_DARK),
        ("Mở rộng", "Đếm u = 1 để tuyển gia sư", ORANGE_SOFT_BG, ORANGE_PRIMARY, ORANGE_TEXT),
    ]
    bw, bh = 2.90, 1.02
    for idx, (b_t, b_s, bg_c, bd_c, tx_c) in enumerate(bsc):
        col = idx % 2
        row = idx // 2
        bx = 0.60 + col * (bw + 0.20)
        by = 4.86 + row * (bh + 0.16)
        add_box(s, bx, by, bw, bh, bg_c, bd_c, border_pt=1.8)
        add_text(s, bx + 0.16, by + 0.12, bw - 0.32, 0.34, b_t, fs=15.0, bold=True, color=tx_c)
        add_text(s, bx + 0.16, by + 0.50, bw - 0.32, 0.40, b_s, fs=13.8, color=INK_DARK)

    # Right: Concise Limitations & AI Transparency
    add_box(s, 6.85, 1.54, 5.88, 2.72, YELLOW_SOFT_BG, AMBER_PRIMARY, border_pt=2.0)
    add_text(s, 7.10, 1.72, 5.40, 0.36, "GIỚI HẠN & HƯỚNG PHÁT TRIỂN", fs=16.0, bold=True, color=AMBER_TEXT)
    add_bullets(s, 7.10, 2.20, 5.40, 1.90, [
        "Dữ liệu hiện tại: Mô phỏng tái lập (seed = 42, 20 tháng)",
        "Bước tiếp: Chạy script nạp CSV lịch sử thật từ máy chủ",
        "Mở rộng: Ghép xen học viên mới vào lớp nhóm đang học",
    ], fs=14.8, color=INK_DARK, space_after=10)

    add_box(s, 6.85, 4.48, 5.88, 2.58, SURFACE_NEUTRAL, BORDER_STRONG, border_pt=2.0)
    add_text(s, 7.10, 4.66, 5.40, 0.36, "KHAI BÁO MINH BẠCH CÔNG CỤ AI", fs=16.0, bold=True, color=FOREST_DARK)
    add_bullets(s, 7.10, 5.14, 5.40, 1.80, [
        "Hỗ trợ: Viết mã mô phỏng MILP/SimPy & kết xuất sơ đồ",
        "Nhóm 20 kiểm chứng: Thiết kế nghiệp vụ thật, tự kiểm tra toàn bộ công thức, BPMN 2.0 và số liệu chạy",
    ], fs=14.8, color=INK_DARK, space_after=10)


def build_slide_12_conclusion(prs, blank):
    s = prs.slides.add_slide(blank)
    set_bg(s, FOREST_DARK)

    c1 = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(10.5), Inches(-1.0), Inches(4.2), Inches(4.2))
    c1.fill.solid()
    c1.fill.fore_color.rgb = FOREST_ELEVATED
    c1.line.fill.background()

    add_pill(s, 0.75, 0.58, 2.60, 0.40, "TỔNG KẾT ĐỀ TÀI",
             FOREST_ELEVATED, YELLOW_BRIGHT, YELLOW_BRIGHT, fs=12.0)

    add_text(s, 0.75, 1.18, 11.88, 0.58,
             "Chuẩn hóa đầu vào + Tối ưu MILP bứt phá trên cùng nhân sự",
             fs=25.0, bold=True, color=WHITE)

    answers = [
        ("Q1 · TỶ LỆ GHÉP LỚP", "60,4% → 92,7%",
         "Tăng +32,3 điểm %\nGiảm 81,5% học viên rớt lớp\n(khi hỏi 2–3 khung giờ)",
         YELLOW_BRIGHT),
        ("Q2 · ĐỘ HỢP LỊCH", "58,5 → 86,5 đ",
         "Tăng +28,0 điểm toàn tập\nGom đủ nhóm 3–5 học viên\nTrội Pareto hoàn toàn",
         MINT_BRIGHT),
        ("Q3 · THỜI GIAN CHỜ", "22,6h → 10,3h",
         "Giảm 54,4% thời gian chờ\n99,3% chốt trong ≤ 2 ngày\nQuản lý giảm bận còn 8,7%",
         PEACH_BRIGHT),
    ]
    cw = 3.82
    gap = 0.21
    for idx, (tag, big, desc, col) in enumerate(answers):
        cx = 0.75 + idx * (cw + gap)
        add_box(s, cx, 2.05, cw, 3.45, FOREST_ELEVATED, col, border_pt=2.0)
        add_text(s, cx + 0.24, 2.28, cw - 0.48, 0.36, tag, fs=13.5, bold=True, color=col)
        add_text(s, cx + 0.24, 2.74, cw - 0.48, 0.72, big, fs=31, bold=True, color=WHITE)
        add_text(s, cx + 0.24, 3.66, cw - 0.48, 1.65, desc, fs=16.0, bold=True, color=MINT_BRIGHT, line_spacing=1.35)

    add_box(s, 0.75, 5.82, 11.88, 1.08, FOREST_ELEVATED, YELLOW_BRIGHT, border_pt=2.0)
    add_text(s, 1.05, 5.98, 7.60, 0.42,
             "Trân trọng cảm ơn Thầy/Cô và các bạn đã lắng nghe!",
             fs=19.5, bold=True, color=YELLOW_BRIGHT)
    add_text(s, 1.05, 6.44, 7.60, 0.34,
             "Nhóm 20  ·  Phoutthavong Xayavong (23021941)  &  Vũ Quốc Long (23020105)",
             fs=14.0, bold=True, color=WHITE)
    add_pill(s, 9.65, 6.10, 2.70, 0.52, "THẢO LUẬN & HỎI ĐÁP", YELLOW_BRIGHT, FOREST_DARK, fs=13.5)


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
    print(f"Successfully generated projector-optimized 12-slide presentation: {PPTX_PATH}")


if __name__ == "__main__":
    main()
