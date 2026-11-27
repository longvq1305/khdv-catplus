"""
Compile Bao_cao_Du_an_Nhom20_CatPlus_Draft1.md into publication-grade:
  1) Bao_cao_Du_an_Nhom20_CatPlus_Draft1.html (LaTeX/Booktabs VNU-UET academic layout)
  2) Bao_cao_Du_an_Nhom20_CatPlus_Draft1.pdf  (2-pass Chrome headless + PyMuPDF exact TOC & page numbers: Cover unnumbered, TOC='i', Body='1..N')
  3) Bao_cao_Du_an_Nhom20_CatPlus_Draft1.docx (Times New Roman, cover double border, TOC, Booktabs tables, numbered equations)
"""

import os
import re
import base64
import subprocess
import fitz  # PyMuPDF
import markdown
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(OUT_DIR, "Bao_cao_Du_an_Nhom20_CatPlus_Draft1.md")
HTML_PATH = os.path.join(OUT_DIR, "Bao_cao_Du_an_Nhom20_CatPlus_Draft1.html")
PDF_PATH = os.path.join(OUT_DIR, "Bao_cao_Du_an_Nhom20_CatPlus_Draft1.pdf")
DOCX_PATH = os.path.join(OUT_DIR, "Bao_cao_Du_an_Nhom20_CatPlus_Draft1.docx")
LOGO_PATH = os.path.join(OUT_DIR, "uet_logo.png")


def img_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def extract_headings(md_body):
    """Extract level-1 (## ) and level-2 (### ) headings in body."""
    items = []
    for line in md_body.splitlines():
        s = line.strip()
        if s.startswith("## "):
            title = s[3:].strip()
            m = re.match(r'^(\d+)\s+(.*)$', title)
            if m:
                items.append(("h2", m.group(1), m.group(2), title))
            else:
                items.append(("h2_unnum", "", title, title))
        elif s.startswith("### "):
            title = s[4:].strip()
            m = re.match(r'^(\d+\.\d+)\s+(.*)$', title)
            if m:
                items.append(("h3", m.group(1), m.group(2), title))
            else:
                items.append(("h3", "", title, title))
    return items


def preprocess_custom_blocks(md_body):
    """Convert {{EQ:...|(X.Y)}}, :::summary-box, figure captions, table captions, and code blocks into academic HTML."""
    lines = md_body.splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()

        # Equation marker {{EQ:html|(num)}}
        m_eq = re.match(r'^\{\{EQ:(.*)\|(\([^)]+\))\}\}$', s)
        if m_eq:
            expr_html = m_eq.group(1).strip()
            eq_num = m_eq.group(2).strip()
            out.append(
                f'<div class="eq-row"><div class="eq-spacer"></div>'
                f'<div class="eq-expr">{expr_html}</div>'
                f'<div class="eq-num">{eq_num}</div></div>'
            )
            i += 1
            continue

        # Summary box :::summary-box ... :::
        if s == ":::summary-box":
            i += 1
            box_title = "Tóm tắt chẩn đoán"
            box_lines = []
            while i < len(lines) and lines[i].strip() != ":::":
                bl = lines[i].strip()
                if bl.startswith("**") and bl.endswith("**") and not box_lines:
                    box_title = bl.strip("*")
                elif bl:
                    box_lines.append(bl)
                i += 1
            i += 1  # skip closing :::
            bullets = [b[2:].strip() for b in box_lines if b.startswith("- ")]
            tail = [b for b in box_lines if not b.startswith("- ")]
            li_html = "".join(f"<li>{markdown.markdown(b)[3:-4]}</li>" for b in bullets)
            tail_html = "".join(f"<p class='box-tail'>{markdown.markdown(t)[3:-4]}</p>" for t in tail)
            out.append(
                f'<div class="diag-box">'
                f'<div class="diag-box-header">{box_title}</div>'
                f'<div class="diag-box-body"><ul>{li_html}</ul>{tail_html}</div>'
                f'</div>'
            )
            continue

        # Code block ```python or ```text -> line-numbered or clean log box
        if s.startswith("```"):
            lang = s[3:].strip()
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1
            import html as html_lib
            if lang == "python":
                rows_html = []
                for idx, cl in enumerate(code_lines, 1):
                    esc = html_lib.escape(cl)
                    rows_html.append(
                        f'<div class="code-line"><span class="ln">{idx}</span>'
                        f'<span class="lc">{esc}</span></div>'
                    )
                out.append(f'<div class="code-frame">{"".join(rows_html)}</div>')
            else:
                esc_all = html_lib.escape("\n".join(code_lines))
                out.append(f'<div class="log-frame"><pre>{esc_all}</pre></div>')
            continue

        # Table caption: **Bảng X.Y.** ...
        if re.match(r'^\*\*Bảng\s+[A-Z0-9.]+\.\*\*', s):
            cap_inner = markdown.markdown(s)[3:-4]
            out.append(f'<p class="table-caption">{cap_inner}</p>')
            i += 1
            continue

        # Image + Figure caption right below it
        m_img = re.match(r'^!\[([^\]]*)\]\(([^)]+\.png)\)$', s)
        if m_img:
            alt = m_img.group(1)
            rel_p = m_img.group(2).lstrip("./")
            full_p = os.path.join(OUT_DIR, rel_p)
            b64 = img_to_b64(full_p) if os.path.exists(full_p) else ""
            cap_html = ""
            if i + 1 < len(lines) and lines[i + 1].strip().startswith("*Hình "):
                raw_cap = lines[i + 1].strip()[1:-1]
                # Bold "Hình X.Y." part matching sample PDF!
                raw_cap = re.sub(r'^(Hình\s+\d+\.\d+\.)', r'<strong>\1</strong>', raw_cap)
                cap_html = f'<div class="fig-caption">{raw_cap}</div>'
                i += 1
            out.append(
                f'<div class="fig-block">'
                f'<img src="data:image/png;base64,{b64}" alt="{alt}">'
                f'{cap_html}</div>'
            )
            i += 1
            continue

        out.append(line)
        i += 1

    return "\n".join(out)


def build_html_doc(md_text, page_map=None):
    # Split body after <!-- TOC_END --> and ---
    parts = md_text.split("<!-- TOC_END -->")
    after_toc = parts[1].lstrip()
    if after_toc.startswith("---"):
        after_toc = after_toc[3:].lstrip()

    headings = extract_headings(after_toc)
    logo_b64 = img_to_b64(LOGO_PATH) if os.path.exists(LOGO_PATH) else ""

    # Build TOC HTML rows
    toc_rows = []
    for kind, num, text, full_title in headings:
        pg = page_map.get(full_title, "1") if page_map else "1"
        if kind == "h2":
            toc_rows.append(
                f'<div class="toc-row toc-h2">'
                f'<span class="toc-num">{num}</span>'
                f'<span class="toc-title">{text}</span>'
                f'<span class="toc-dots"></span>'
                f'<span class="toc-pg">{pg}</span></div>'
            )
        elif kind == "h2_unnum":
            toc_rows.append(
                f'<div class="toc-row toc-h2">'
                f'<span class="toc-title-unnum">{text}</span>'
                f'<span class="toc-dots"></span>'
                f'<span class="toc-pg">{pg}</span></div>'
            )
        else:
            toc_rows.append(
                f'<div class="toc-row toc-h3">'
                f'<span class="toc-num-sub">{num}</span>'
                f'<span class="toc-title">{text}</span>'
                f'<span class="toc-dots"></span>'
                f'<span class="toc-pg">{pg}</span></div>'
            )

    pre_body = preprocess_custom_blocks(after_toc)
    body_html = markdown.markdown(pre_body, extensions=["tables"])
    body_html = body_html.replace(
        "<h2>Tài liệu tham khảo</h2>",
        '<h2 class="ref-heading">Tài liệu tham khảo</h2>',
    ).replace(
        "<h2>Phụ lục: Khai báo minh bạch sử dụng AI</h2>",
        '<h2 class="app-heading">Phụ lục: Khai báo minh bạch sử dụng AI</h2>',
    )

    # Clean horizontal rules
    body_html = body_html.replace("<hr />", "").replace("<hr>", "")

    html_str = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Báo cáo Dự án Cuối kỳ INT3501 - Nhóm 20 - CatPlus</title>
<style>
@page {{
    size: A4 portrait;
    margin: 22mm 20mm 24mm 22mm;
}}
@page :first {{
    margin: 14mm 14mm 14mm 14mm;
}}
* {{
    box-sizing: border-box;
}}
body {{
    font-family: "Times New Roman", Times, Georgia, serif;
    font-size: 12pt;
    line-height: 1.45;
    color: #000000;
    margin: 0;
    padding: 0;
    background: #FFFFFF;
}}

/* --- COVER PAGE (Matches VNU-UET Sample Page 1) --- */
.cover-outer {{
    width: 100%;
    height: 268mm;
    border: 2.2pt solid #000000;
    padding: 3.5pt;
    page-break-after: always;
}}
.cover-inner {{
    width: 100%;
    height: 100%;
    border: 0.75pt solid #000000;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    padding: 20mm 16mm 16mm 16mm;
    text-align: center;
}}
.cover-uni {{
    font-size: 13.5pt;
    font-weight: bold;
    line-height: 1.55;
    letter-spacing: 0.2px;
}}
.cover-logo {{
    width: 38mm;
    height: 38mm;
    object-fit: contain;
    margin: 4mm 0;
}}
.cover-type {{
    font-size: 15pt;
    font-weight: bold;
    margin-bottom: 3mm;
}}
.cover-course {{
    font-size: 12.5pt;
    font-weight: normal;
}}
.cover-title {{
    font-size: 17.5pt;
    font-weight: bold;
    line-height: 1.38;
    text-transform: uppercase;
    margin: 4mm 0 4mm 0;
}}
.cover-subtitle {{
    font-size: 12pt;
    line-height: 1.48;
    max-width: 138mm;
    margin: 0 auto;
}}
.cover-authors {{
    font-size: 12.5pt;
    line-height: 1.65;
    margin-top: 6mm;
}}
.cover-group {{
    font-weight: bold;
    margin-bottom: 3mm;
}}
.author-table {{
    margin: 0 auto;
    border-collapse: collapse;
    font-size: 12.5pt;
}}
.author-table td {{
    border: none !important;
    padding: 2px 10px !important;
    text-align: left;
}}
.cover-footer {{
    font-size: 12.5pt;
    font-weight: bold;
}}

/* --- TABLE OF CONTENTS PAGE (Matches Sample Page 2) --- */
.toc-page {{
    page-break-after: always;
    padding-top: 1mm;
}}
.toc-heading {{
    font-size: 17pt;
    font-weight: bold;
    margin: 0 0 4.5mm 0;
}}
.toc-row {{
    display: flex;
    align-items: baseline;
    line-height: 1.40;
    font-size: 11pt;
}}
.toc-h2 {{
    font-weight: bold;
    margin-top: 1.7mm;
}}
.toc-h3 {{
    font-weight: normal;
    padding-left: 7mm;
}}
.toc-num {{
    width: 7mm;
    flex-shrink: 0;
}}
.toc-num-sub {{
    width: 10mm;
    flex-shrink: 0;
}}
.toc-title, .toc-title-unnum {{
    flex-shrink: 0;
}}
.toc-dots {{
    flex-grow: 1;
    border-bottom: 1px dotted #333333;
    margin: 0 6px;
    position: relative;
    top: -3px;
}}
.toc-pg {{
    flex-shrink: 0;
    min-width: 6mm;
    text-align: right;
}}

/* --- MAIN ACADEMIC BODY --- */
.main-body h2 {{
    font-size: 15.5pt;
    font-weight: bold;
    margin: 18pt 0 8pt 0;
    color: #000000;
    border: none;
    page-break-after: avoid;
}}
.main-body h2.ref-heading, .main-body h2.app-heading {{
    page-break-before: always;
    border-bottom: 0.75pt solid #000000;
    padding-bottom: 4pt;
    margin-top: 4pt;
}}
.main-body h3 {{
    font-size: 13pt;
    font-weight: bold;
    margin: 13pt 0 6pt 0;
    color: #000000;
    page-break-after: avoid;
}}
.main-body p {{
    margin: 0 0 7pt 0;
    text-align: justify;
    text-indent: 1.6em;
    overflow-wrap: break-word;
}}
.main-body p.table-caption {{
    text-align: center;
    text-indent: 0;
    font-size: 10.8pt;
    margin: 12pt 0 5pt 0;
    page-break-after: avoid;
}}
.main-body ul, .main-body ol {{
    margin: 4pt 0 8pt 0;
    padding-left: 22pt;
}}
.main-body li {{
    margin-bottom: 4pt;
    text-align: justify;
}}
.main-body code {{
    font-family: Consolas, "Courier New", monospace;
    font-size: 9.8pt;
    background: none;
    overflow-wrap: anywhere;
}}

/* --- BOOKTABS THREE-LINE TABLES --- */
.main-body table {{
    width: 100%;
    border-collapse: collapse;
    border-top: 1.5pt solid #000000;
    border-bottom: 1.5pt solid #000000;
    margin: 0 0 12pt 0;
    font-size: 10.3pt;
    line-height: 1.35;
    page-break-inside: auto;
}}
.main-body thead th {{
    border-bottom: 0.75pt solid #000000;
    border-left: none;
    border-right: none;
    padding: 5pt 6pt;
    font-weight: bold;
    background: transparent;
    color: #000000;
    vertical-align: bottom;
}}
.main-body tbody td {{
    border: none;
    padding: 4.5pt 6pt;
    vertical-align: top;
    background: transparent;
}}
.main-body tr {{
    page-break-inside: avoid;
}}

/* --- EQUATIONS (Right-numbered like LaTeX) --- */
.eq-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 9pt 0 9pt 0;
    font-size: 11.5pt;
    page-break-inside: avoid;
}}
.eq-spacer {{
    width: 36pt;
}}
.eq-expr {{
    text-align: center;
    flex-grow: 1;
}}
.eq-num {{
    width: 36pt;
    text-align: right;
}}
.frac {{
    display: inline-flex;
    flex-direction: column;
    vertical-align: middle;
    text-align: center;
    padding: 0 3px;
    font-size: 10.5pt;
    line-height: 1.1;
}}
.frac .num {{
    border-bottom: 0.7pt solid #000000;
    padding: 0 2px 1px 2px;
}}
.frac .den {{
    padding: 1px 2px 0 2px;
}}

/* --- FIGURES --- */
.fig-block {{
    margin: 12pt 0 12pt 0;
    text-align: center;
    page-break-inside: avoid;
}}
.fig-block img {{
    max-width: 98%;
    max-height: 125mm;
    height: auto;
    display: block;
    margin: 0 auto 5pt auto;
}}
.fig-caption {{
    font-size: 10.8pt;
    line-height: 1.38;
    text-align: center;
    max-width: 95%;
    margin: 0 auto;
}}

/* --- SUMMARY BOX (Matches Sample Page 11) --- */
.diag-box {{
    border: 0.8pt solid #000000;
    margin: 12pt 0 14pt 0;
    page-break-inside: avoid;
}}
.diag-box-header {{
    font-weight: bold;
    padding: 5pt 10pt;
    border-bottom: 0.6pt solid #000000;
    font-size: 11.2pt;
}}
.diag-box-body {{
    padding: 6pt 10pt 7pt 10pt;
    font-size: 11pt;
}}
.diag-box-body ul {{
    margin: 2pt 0 5pt 0;
    padding-left: 16pt;
}}
.diag-box-body p.box-tail {{
    text-indent: 0;
    margin: 4pt 0 0 0;
}}

/* --- CODE & LOG FRAMES (Matches Sample Pages 15-16) --- */
.code-frame {{
    border: 0.75pt solid #000000;
    padding: 6pt 8pt;
    margin: 8pt 0 12pt 0;
    font-family: Consolas, "Courier New", monospace;
    font-size: 8.6pt;
    line-height: 1.36;
    page-break-inside: avoid;
}}
.code-line {{
    display: flex;
    white-space: pre-wrap;
    word-break: break-word;
}}
.code-line .ln {{
    width: 20pt;
    color: #555555;
    text-align: right;
    padding-right: 7pt;
    flex-shrink: 0;
    user-select: none;
    font-size: 7.8pt;
}}
.code-line .lc {{
    flex-grow: 1;
}}
.log-frame {{
    border: 0.75pt solid #000000;
    padding: 6pt 9pt;
    margin: 8pt 0 12pt 0;
    page-break-inside: avoid;
}}
.log-frame pre {{
    margin: 0;
    font-family: Consolas, "Courier New", monospace;
    font-size: 8.5pt;
    line-height: 1.35;
    white-space: pre-wrap;
}}
</style>
</head>
<body>

<!-- PAGE 1: COVER PAGE -->
<div class="cover-outer">
  <div class="cover-inner">
    <div class="cover-uni">
      ĐẠI HỌC QUỐC GIA HÀ NỘI<br>
      TRƯỜNG ĐẠI HỌC CÔNG NGHỆ
    </div>

    <img class="cover-logo" src="data:image/png;base64,{logo_b64}" alt="Logo ĐH Công nghệ">

    <div>
      <div class="cover-type">BÁO CÁO DỰ ÁN CUỐI KỲ</div>
      <div class="cover-course">Học phần: Khoa học dịch vụ (INT3501)</div>
    </div>

    <div>
      <div class="cover-title">
        TỐI ƯU HÓA QUY TRÌNH GHÉP ĐÔI<br>
        GIA SƯ – HỌC VIÊN VÀ XẾP LỊCH HỌC<br>
        TRÊN NỀN TẢNG CATPLUS
      </div>
      <div class="cover-subtitle">
        So sánh phương án xếp lịch thủ công cơ sở (AS-IS) và quy hoạch nguyên gom nhóm (MILP), kết hợp mô phỏng hàng đợi SimPy, trên hệ thống dịch vụ đào tạo lập trình CatPlus
      </div>
    </div>

    <div class="cover-authors">
      <div class="cover-group">Nhóm 20</div>
      <table class="author-table">
        <tr><td colspan="2">Sinh viên thực hiện:</td></tr>
        <tr><td>23021941</td><td>Phoutthavong Xayavong</td></tr>
        <tr><td>[Điền MSV]</td><td>Vũ Quốc Long</td></tr>
      </table>
    </div>

    <div class="cover-footer">Hà Nội, 2026</div>
  </div>
</div>

<!-- PAGE 2: TABLE OF CONTENTS -->
<div class="toc-page">
  <div class="toc-heading">Mục lục</div>
  {"".join(toc_rows)}
</div>

<!-- MAIN BODY -->
<div class="main-body">
{body_html}
</div>

</body>
</html>"""
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_str)
    return headings


def render_pdf_via_chrome():
    chrome_candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    browser = next((p for p in chrome_candidates if os.path.exists(p)), None)
    if not browser:
        raise RuntimeError("No Chrome/Edge found for PDF export.")

    file_url = "file:///" + HTML_PATH.replace("\\", "/")
    raw_pdf = os.path.join(OUT_DIR, "_raw_temp.pdf")
    if os.path.exists(raw_pdf):
        os.remove(raw_pdf)

    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={raw_pdf}",
        file_url,
    ]
    subprocess.run(cmd, check=True, timeout=45)
    return raw_pdf


def discover_page_numbers_and_stamp(raw_pdf, headings):
    """
    Find where TOC ends (usually page index 1, or 1..k if TOC spans >1 page),
    discover exact body page numbers (1-based starting at first body page),
    and stamp Roman 'i' on TOC and '1..N' on body pages!
    """
    doc = fitz.open(raw_pdf)
    # Find page index where "1 Bối cảnh và câu hỏi phân tích" starts (skipping cover=0 and TOC=1)
    first_body_idx = 2
    for p_idx in range(1, len(doc)):
        txt = doc[p_idx].get_text()
        if "1.1 Vấn đề dịch vụ" in txt:
            first_body_idx = p_idx
            break

    page_map = {}
    search_start = first_body_idx
    for kind, num, text, full_title in headings:
        for p_idx in range(search_start, len(doc)):
            txt = doc[p_idx].get_text()
            if full_title in txt or text in txt:
                page_map[full_title] = str(p_idx - first_body_idx + 1)
                search_start = p_idx
                break
        if full_title not in page_map:
            page_map[full_title] = str(max(1, search_start - first_body_idx + 1))

    doc.close()
    return page_map, first_body_idx


def stamp_page_numbers(raw_pdf, first_body_idx, final_pdf):
    roman = ["i", "ii", "iii", "iv"]
    doc = fitz.open(raw_pdf)
    for p_idx, page in enumerate(doc):
        if p_idx == 0:
            continue  # Cover page has no page number
        elif p_idx < first_body_idx:
            lbl = roman[p_idx - 1]
        else:
            lbl = str(p_idx - first_body_idx + 1)

        rect = page.rect
        footer_box = fitz.Rect(0, rect.height - 42, rect.width, rect.height - 18)
        page.insert_textbox(
            footer_box,
            lbl,
            fontsize=11,
            fontname="tiro",  # Times-Roman standard PDF font
            align=fitz.TEXT_ALIGN_CENTER,
            color=(0, 0, 0),
        )
    doc.save(final_pdf)
    total_pages = len(doc)
    doc.close()
    return total_pages


def set_booktabs_borders(table):
    """Apply academic Booktabs 3-line horizontal borders (top, header-bottom, bottom) and remove vertical borders."""
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for b_name, val, sz in [
        ("top", "single", "12"),
        ("bottom", "single", "12"),
        ("insideH", "none", "0"),
        ("left", "none", "0"),
        ("right", "none", "0"),
        ("insideV", "none", "0"),
    ]:
        el = OxmlElement(f"w:{b_name}")
        el.set(qn("w:val"), val)
        el.set(qn("w:sz"), sz)
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "000000")
        borders.append(el)
    tblPr.append(borders)

    # Bottom thin border on header row cells
    if len(table.rows) > 0:
        for cell in table.rows[0].cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = OxmlElement("w:tcBorders")
            b_el = OxmlElement("w:bottom")
            b_el.set(qn("w:val"), "single")
            b_el.set(qn("w:sz"), "6")
            b_el.set(qn("w:space"), "0")
            b_el.set(qn("w:color"), "000000")
            tcBorders.append(b_el)
            tcPr.append(tcBorders)


def set_single_box_border(table):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for b_name in ["top", "bottom", "left", "right", "insideH"]:
        el = OxmlElement(f"w:{b_name}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "6")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "000000")
        borders.append(el)
    tblPr.append(borders)


def html_inline_to_plain_runs(paragraph, text, font_size=11.5, bold_override=False, italic_override=False):
    """Convert simple Markdown/HTML inline tags (**bold**, *italic*, <i>, <sub>, <sup>, `code`, <span class='frac'>) into clean Times New Roman runs."""
    # Convert HTML frac to (num / den) for clean Word inline representation
    text = re.sub(
        r'<span class="frac"><span class="num">(.*?)</span><span class="den">(.*?)</span></span>',
        r'(\1) / (\2)',
        text,
    )
    text = text.replace("&emsp;", "   ")
    token_re = re.compile(
        r'(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|<i>.*?</i>|<sub>.*?</sub>|<sup>.*?</sup>)'
    )
    pos = 0
    for m in token_re.finditer(text):
        if m.start() > pos:
            raw = re.sub(r'<[^>]+>', '', text[pos:m.start()])
            r = paragraph.add_run(raw)
            r.font.name = "Times New Roman"
            r.font.size = Pt(font_size)
            r.bold = bold_override
            r.italic = italic_override
        tk = m.group(0)
        if tk.startswith("**"):
            r = paragraph.add_run(re.sub(r'<[^>]+>', '', tk[2:-2]))
            r.bold = True
            r.italic = italic_override
            r.font.name = "Times New Roman"
            r.font.size = Pt(font_size)
        elif tk.startswith("*"):
            r = paragraph.add_run(re.sub(r'<[^>]+>', '', tk[1:-1]))
            r.italic = True
            r.bold = bold_override
            r.font.name = "Times New Roman"
            r.font.size = Pt(font_size)
        elif tk.startswith("`"):
            r = paragraph.add_run(tk[1:-1])
            r.font.name = "Consolas"
            r.font.size = Pt(font_size - 1.5)
            r.bold = bold_override
        elif tk.startswith("<i>"):
            r = paragraph.add_run(re.sub(r'<[^>]+>', '', tk[3:-4]))
            r.italic = True
            r.bold = bold_override
            r.font.name = "Times New Roman"
            r.font.size = Pt(font_size)
        elif tk.startswith("<sub>"):
            r = paragraph.add_run(re.sub(r'<[^>]+>', '', tk[5:-6]))
            r.font.subscript = True
            r.font.name = "Times New Roman"
            r.font.size = Pt(font_size)
        elif tk.startswith("<sup>"):
            r = paragraph.add_run(re.sub(r'<[^>]+>', '', tk[5:-6]))
            r.font.superscript = True
            r.font.name = "Times New Roman"
            r.font.size = Pt(font_size)
        pos = m.end()
    if pos < len(text):
        raw = re.sub(r'<[^>]+>', '', text[pos:])
        r = paragraph.add_run(raw)
        r.font.name = "Times New Roman"
        r.font.size = Pt(font_size)
        r.bold = bold_override
        r.italic = italic_override


def build_docx(md_text, headings, page_map):
    doc = Document()
    for sec in doc.sections:
        sec.top_margin = Cm(2.2)
        sec.bottom_margin = Cm(2.4)
        sec.left_margin = Cm(2.4)
        sec.right_margin = Cm(2.0)

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)

    # --- COVER PAGE ---
    cover_tbl = doc.add_table(rows=1, cols=1)
    cover_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_cell = cover_tbl.cell(0, 0)
    tcPr = c_cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for b_name in ["top", "bottom", "left", "right"]:
        b_el = OxmlElement(f"w:{b_name}")
        b_el.set(qn("w:val"), "double")
        b_el.set(qn("w:sz"), "12")
        b_el.set(qn("w:space"), "6")
        b_el.set(qn("w:color"), "000000")
        tcBorders.append(b_el)
    tcPr.append(tcBorders)

    p0 = c_cell.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.space_before = Pt(14)
    p0.paragraph_format.space_after = Pt(16)
    r_uni = p0.add_run("ĐẠI HỌC QUỐC GIA HÀ NỘI\nTRƯỜNG ĐẠI HỌC CÔNG NGHỆ")
    r_uni.bold = True
    r_uni.font.name = "Times New Roman"
    r_uni.font.size = Pt(13.5)

    if os.path.exists(LOGO_PATH):
        p_logo = c_cell.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(18)
        p_logo.add_run().add_picture(LOGO_PATH, width=Inches(1.45))

    p_type = c_cell.add_paragraph()
    p_type.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_type.paragraph_format.space_after = Pt(22)
    rt1 = p_type.add_run("BÁO CÁO DỰ ÁN CUỐI KỲ\n")
    rt1.bold = True
    rt1.font.name = "Times New Roman"
    rt1.font.size = Pt(15)
    rt2 = p_type.add_run("Học phần: Khoa học dịch vụ (INT3501)")
    rt2.font.name = "Times New Roman"
    rt2.font.size = Pt(12.5)

    p_tit = c_cell.add_paragraph()
    p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tit.paragraph_format.space_after = Pt(12)
    rt_m = p_tit.add_run(
        "TỐI ƯU HÓA QUY TRÌNH GHÉP ĐÔI\nGIA SƯ – HỌC VIÊN VÀ XẾP LỊCH HỌC\nTRÊN NỀN TẢNG CATPLUS"
    )
    rt_m.bold = True
    rt_m.font.name = "Times New Roman"
    rt_m.font.size = Pt(17)

    p_sub = c_cell.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(36)
    rt_s = p_sub.add_run(
        "So sánh phương án xếp lịch thủ công cơ sở (AS-IS) và quy hoạch nguyên gom nhóm (MILP),\n"
        "kết hợp mô phỏng hàng đợi SimPy, trên hệ thống dịch vụ đào tạo lập trình CatPlus"
    )
    rt_s.font.name = "Times New Roman"
    rt_s.font.size = Pt(12)

    p_aut = c_cell.add_paragraph()
    p_aut.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_aut.paragraph_format.space_after = Pt(48)
    rg = p_aut.add_run("Nhóm 20\n\n")
    rg.bold = True
    rg.font.name = "Times New Roman"
    rg.font.size = Pt(12.5)
    ra = p_aut.add_run("Sinh viên thực hiện:\n23021941    Phoutthavong Xayavong\n[Điền MSV]  Vũ Quốc Long")
    ra.font.name = "Times New Roman"
    ra.font.size = Pt(12.5)

    p_ft = c_cell.add_paragraph()
    p_ft.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ft.paragraph_format.space_after = Pt(12)
    rf = p_ft.add_run("Hà Nội, 2026")
    rf.bold = True
    rf.font.name = "Times New Roman"
    rf.font.size = Pt(12.5)

    doc.add_page_break()

    # --- TOC PAGE ---
    p_toc_h = doc.add_paragraph()
    p_toc_h.paragraph_format.space_after = Pt(14)
    rtoc = p_toc_h.add_run("Mục lục")
    rtoc.bold = True
    rtoc.font.name = "Times New Roman"
    rtoc.font.size = Pt(17)

    toc_tbl = doc.add_table(rows=len(headings), cols=2)
    toc_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (kind, num, text, full_title) in enumerate(headings):
        pg = page_map.get(full_title, "1")
        row = toc_tbl.rows[idx]
        p_l = row.cells[0].paragraphs[0]
        p_r = row.cells[1].paragraphs[0]
        p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_l.paragraph_format.space_before = Pt(2 if kind == "h3" else 5)
        p_l.paragraph_format.space_after = Pt(2)
        if kind == "h3":
            p_l.paragraph_format.left_indent = Cm(0.65)
        lbl = f"{num}   {text}" if num else text
        rl = p_l.add_run(lbl)
        rr = p_r.add_run(pg)
        for r in (rl, rr):
            r.font.name = "Times New Roman"
            r.font.size = Pt(11.5)
            r.bold = kind in ("h2", "h2_unnum")

    doc.add_page_break()

    # --- MAIN BODY ---
    after_toc = md_text.split("<!-- TOC_END -->")[1].lstrip()
    if after_toc.startswith("---"):
        after_toc = after_toc[3:].lstrip()

    lines = after_toc.splitlines()
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if not s or s == "---":
            i += 1
            continue

        if s.startswith("## "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(s[3:].strip())
            r.bold = True
            r.font.name = "Times New Roman"
            r.font.size = Pt(15)
            i += 1
            continue

        if s.startswith("### "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(11)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(s[4:].strip())
            r.bold = True
            r.font.name = "Times New Roman"
            r.font.size = Pt(13)
            i += 1
            continue

        # Equation {{EQ:...|(X.Y)}}
        m_eq = re.match(r'^\{\{EQ:(.*)\|(\([^)]+\))\}\}$', s)
        if m_eq:
            eq_tbl = doc.add_table(rows=1, cols=2)
            eq_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            p_expr = eq_tbl.cell(0, 0).paragraphs[0]
            p_expr.alignment = WD_ALIGN_PARAGRAPH.CENTER
            html_inline_to_plain_runs(p_expr, m_eq.group(1).strip(), font_size=11.5)
            p_num = eq_tbl.cell(0, 1).paragraphs[0]
            p_num.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            rn = p_num.add_run(m_eq.group(2).strip())
            rn.font.name = "Times New Roman"
            rn.font.size = Pt(11.5)
            i += 1
            continue

        # Summary box
        if s == ":::summary-box":
            i += 1
            b_title = "Tóm tắt chẩn đoán"
            b_items = []
            while i < len(lines) and lines[i].strip() != ":::":
                bl = lines[i].strip()
                if bl.startswith("**") and bl.endswith("**") and not b_items:
                    b_title = bl.strip("*")
                elif bl:
                    b_items.append(bl)
                i += 1
            i += 1
            btbl = doc.add_table(rows=2, cols=1)
            set_single_box_border(btbl)
            ph = btbl.cell(0, 0).paragraphs[0]
            rh = ph.add_run(b_title)
            rh.bold = True
            rh.font.name = "Times New Roman"
            rh.font.size = Pt(11.5)
            c_body = btbl.cell(1, 0)
            c_body.paragraphs[0].text = ""
            for idx_b, bi in enumerate(b_items):
                pb = c_body.paragraphs[0] if idx_b == 0 else c_body.add_paragraph()
                pb.paragraph_format.space_after = Pt(3)
                prefix = "• " if bi.startswith("- ") else ""
                clean_bi = bi[2:].strip() if bi.startswith("- ") else bi
                html_inline_to_plain_runs(pb, prefix + clean_bi, font_size=11)
            continue

        # Code / Log block
        if s.startswith("```"):
            lang = s[3:].strip()
            i += 1
            c_lines = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                c_lines.append(lines[i])
                i += 1
            i += 1
            ctbl = doc.add_table(rows=1, cols=1)
            set_single_box_border(ctbl)
            cell = ctbl.cell(0, 0)
            cell.paragraphs[0].text = ""
            for idx_c, cl in enumerate(c_lines):
                pc = cell.paragraphs[0] if idx_c == 0 else cell.add_paragraph()
                pc.paragraph_format.space_before = Pt(0)
                pc.paragraph_format.space_after = Pt(1)
                txt_line = f"{idx_c+1:2d}  {cl}" if lang == "python" else cl
                rc = pc.add_run(txt_line)
                rc.font.name = "Consolas"
                rc.font.size = Pt(8.5)
            continue

        # Table caption
        if re.match(r'^\*\*Bảng\s+[A-Z0-9.]+\.\*\*', s):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            html_inline_to_plain_runs(p, s, font_size=11)
            i += 1
            continue

        # Markdown Table -> Booktabs table
        if s.startswith("|"):
            tbl_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                tbl_lines.append(lines[i].strip())
                i += 1
            rows_data = []
            for tl in tbl_lines:
                cells = [c.strip() for c in tl.strip("|").split("|")]
                if all(re.match(r'^:?-{2,}:?$', c) for c in cells):
                    continue
                rows_data.append(cells)
            if rows_data:
                n_cols = max(len(r) for r in rows_data)
                table = doc.add_table(rows=len(rows_data), cols=n_cols)
                table.alignment = WD_TABLE_ALIGNMENT.CENTER
                set_booktabs_borders(table)
                for r_idx, r_cells in enumerate(rows_data):
                    for c_idx in range(min(n_cols, len(r_cells))):
                        cell = table.cell(r_idx, c_idx)
                        p = cell.paragraphs[0]
                        p.text = ""
                        p.paragraph_format.space_before = Pt(2)
                        p.paragraph_format.space_after = Pt(2)
                        html_inline_to_plain_runs(
                            p, r_cells[c_idx], font_size=10.0, bold_override=(r_idx == 0)
                        )
            continue

        # Image + Caption
        m_img = re.match(r'^!\[([^\]]*)\]\(([^)]+\.png)\)$', s)
        if m_img:
            rel_p = m_img.group(2).lstrip("./")
            full_p = os.path.join(OUT_DIR, rel_p)
            if os.path.exists(full_p):
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(8)
                p.paragraph_format.keep_with_next = True
                p.add_run().add_picture(full_p, width=Inches(6.1))
            if i + 1 < len(lines) and lines[i + 1].strip().startswith("*Hình "):
                raw_cap = lines[i + 1].strip()[1:-1]
                raw_cap = re.sub(r'^(Hình\s+\d+\.\d+\.)', r'**\1**', raw_cap)
                pc = doc.add_paragraph()
                pc.alignment = WD_ALIGN_PARAGRAPH.CENTER
                pc.paragraph_format.space_after = Pt(8)
                html_inline_to_plain_runs(pc, raw_cap, font_size=10.5)
                i += 1
            i += 1
            continue

        # Bullet list
        if s.startswith("- "):
            p = doc.add_paragraph(style="List Bullet")
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_after = Pt(3)
            html_inline_to_plain_runs(p, s[2:].strip(), font_size=11.5)
            i += 1
            continue

        # Numbered list (1. ...) or Reference [1] ...
        if re.match(r'^(\d+\.\s+|\[\d+\]\s+)', s):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent = Cm(0.6)
            p.paragraph_format.first_line_indent = Cm(-0.6)
            p.paragraph_format.space_after = Pt(4)
            html_inline_to_plain_runs(p, s, font_size=11.5)
            i += 1
            continue

        # Regular justified paragraph with first-line indent
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.first_line_indent = Cm(0.75)
        p.paragraph_format.space_after = Pt(5)
        html_inline_to_plain_runs(p, s, font_size=12.0)
        i += 1

    doc.save(DOCX_PATH)
    print(f"Saved {DOCX_PATH}")


def update_markdown_toc(md_text, headings, page_map):
    lines = ["<!-- TOC_START -->"]
    for kind, num, text, full_title in headings:
        pg = page_map.get(full_title, "1")
        if kind == "h2":
            lines.append(f"- **{num} {text}** *(trang {pg})*")
        elif kind == "h2_unnum":
            lines.append(f"- **{text}** *(trang {pg})*")
        else:
            lines.append(f"  - {num} {text} *(trang {pg})*")
    lines.append("<!-- TOC_END -->")
    new_toc = "\n".join(lines)
    updated = re.sub(r'<!-- TOC_START -->.*?<!-- TOC_END -->', new_toc, md_text, flags=re.DOTALL)
    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write(updated)


def main():
    with open(MD_PATH, encoding="utf-8") as f:
        md_text = f.read()

    # Pass 1: Build HTML with placeholder TOC pages & export raw PDF
    headings = build_html_doc(md_text, page_map=None)
    raw_pdf_1 = render_pdf_via_chrome()
    page_map, first_body_idx = discover_page_numbers_and_stamp(raw_pdf_1, headings)
    print("Discovered exact section page numbers:", page_map)

    # Pass 2: Rebuild HTML with exact TOC page numbers, re-export PDF, and stamp Roman 'i' + '1..N'
    build_html_doc(md_text, page_map=page_map)
    raw_pdf_2 = render_pdf_via_chrome()
    _, first_body_idx_2 = discover_page_numbers_and_stamp(raw_pdf_2, headings)
    total_pages = stamp_page_numbers(raw_pdf_2, first_body_idx_2, PDF_PATH)
    if os.path.exists(raw_pdf_2):
        os.remove(raw_pdf_2)
    print(f"Saved {PDF_PATH} ({total_pages} total pages, {total_pages - first_body_idx_2} body pages)")

    # Update Markdown TOC & Build matching DOCX
    update_markdown_toc(md_text, headings, page_map)
    build_docx(md_text, headings, page_map)


if __name__ == "__main__":
    main()
