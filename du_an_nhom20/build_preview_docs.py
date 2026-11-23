"""
Build standalone HTML (print-ready A4 with unified Vietnamese fonts and embedded base64 images)
and Word (.docx) with proper bold/italic runs, formula callout boxes, and tables
from Bao_cao_Du_an_Nhom20_CatPlus_Draft1.md
"""

import os
import re
import base64
import markdown
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(OUT_DIR, "Bao_cao_Du_an_Nhom20_CatPlus_Draft1.md")
HTML_PATH = os.path.join(OUT_DIR, "Bao_cao_Du_an_Nhom20_CatPlus_Draft1.html")
DOCX_PATH = os.path.join(OUT_DIR, "Bao_cao_Du_an_Nhom20_CatPlus_Draft1.docx")


def set_cell_shading(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color_hex)
    tcPr.append(shd)


def add_formatted_runs(paragraph, text, base_size=10.5, default_italic=False, default_color=None):
    """Parse **bold** and *italic* and `code` into clean Word runs with Segoe UI font."""
    pattern = re.compile(r'(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)')
    pos = 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            r = paragraph.add_run(text[pos:m.start()])
            r.font.name = "Segoe UI"
            r.font.size = Pt(base_size)
            r.italic = default_italic
            if default_color:
                r.font.color.rgb = default_color
        token = m.group(0)
        if token.startswith("**") and token.endswith("**"):
            r = paragraph.add_run(token[2:-2])
            r.bold = True
            r.italic = default_italic
        elif token.startswith("*") and token.endswith("*"):
            r = paragraph.add_run(token[1:-1])
            r.italic = True
        elif token.startswith("`") and token.endswith("`"):
            r = paragraph.add_run(token[1:-1])
            r.bold = True
        r.font.name = "Segoe UI"
        r.font.size = Pt(base_size)
        if default_color:
            r.font.color.rgb = default_color
        pos = m.end()
    if pos < len(text):
        r = paragraph.add_run(text[pos:])
        r.font.name = "Segoe UI"
        r.font.size = Pt(base_size)
        r.italic = default_italic
        if default_color:
            r.font.color.rgb = default_color


def build_html(md_text):
    def repl_img(match):
        alt = match.group(1)
        rel_path = match.group(2).lstrip("./")
        full_p = os.path.join(OUT_DIR, rel_path)
        if os.path.exists(full_p):
            with open(full_p, "rb") as img_f:
                b64 = base64.b64encode(img_f.read()).decode("ascii")
            return f'![{alt}](data:image/png;base64,{b64})'
        return match.group(0)

    md_embedded = re.sub(r'!\[([^\]]*)\]\(([^)]+\.png)\)', repl_img, md_text)
    body_html = markdown.markdown(md_embedded, extensions=["tables", "fenced_code"])

    html_doc = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Báo cáo Dự án Nhóm 20 - Khoa học dịch vụ (INT3501) - CatPlus</title>
<style>
@page {{ size: A4 portrait; margin: 15mm 14mm 15mm 14mm; }}
body {{
    font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, Arial, sans-serif;
    font-size: 10.8pt;
    line-height: 1.62;
    color: #0F172A;
    max-width: 960px;
    margin: 24px auto;
    padding: 0 22px;
    background: #FFFFFF;
}}
h1 {{
    font-size: 16pt;
    color: #1E3A8A;
    border-bottom: 2.5px solid #2563EB;
    padding-bottom: 6px;
    margin-top: 0;
}}
h2 {{
    font-size: 13pt;
    color: #1D4ED8;
    border-bottom: 1px solid #CBD5E1;
    padding-bottom: 4px;
    margin-top: 24px;
}}
h3 {{
    font-size: 11.2pt;
    color: #1E293B;
    margin-top: 16px;
}}
p {{
    margin: 8px 0;
    text-align: justify;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 9.6pt;
}}
th, td {{
    border: 1px solid #CBD5E1;
    padding: 7px 9px;
    vertical-align: top;
    text-align: left;
}}
th {{
    background-color: #EFF6FF;
    color: #1E3A8A;
    font-weight: 600;
}}
tr:nth-child(even) td {{
    background-color: #F8FAFC;
}}
img {{
    max-width: 100%;
    height: auto;
    display: block;
    margin: 14px auto 6px auto;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
}}
blockquote {{
    background: #F0F9FF;
    border-left: 4px solid #2563EB;
    border-radius: 4px;
    margin: 12px 0;
    padding: 10px 14px;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 10.2pt;
    color: #0F172A;
}}
blockquote p {{
    margin: 4px 0;
    text-align: left;
}}
code {{
    background: #F1F5F9;
    padding: 1px 5px;
    border-radius: 3px;
    font-family: "Segoe UI", Arial, sans-serif;
    font-weight: 600;
    font-size: 9.8pt;
    color: #1E3A8A;
}}
hr {{
    border: none;
    border-top: 1px solid #E2E8F0;
    margin: 20px 0;
}}
</style>
</head>
<body>
{body_html}
</body>
</html>"""
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_doc)
    print(f"Saved {HTML_PATH}")


def build_docx(md_text):
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Segoe UI"
    style.font.size = Pt(10.5)

    for h_lvl in ["Title", "Heading 1", "Heading 2", "Heading 3"]:
        if h_lvl in doc.styles:
            doc.styles[h_lvl].font.name = "Segoe UI"

    lines = md_text.splitlines()
    i = 0
    while i < len(lines):
        raw_line = lines[i]
        line = raw_line.strip()
        if not line or line == "---":
            i += 1
            continue

        # Headings
        if line.startswith("# "):
            h = doc.add_heading(line[2:].strip(), level=0)
            for r in h.runs:
                r.font.name = "Segoe UI"
            i += 1
            continue
        elif line.startswith("## "):
            h = doc.add_heading(line[3:].strip(), level=1)
            for r in h.runs:
                r.font.name = "Segoe UI"
            i += 1
            continue
        elif line.startswith("### "):
            h = doc.add_heading(line[4:].strip(), level=2)
            for r in h.runs:
                r.font.name = "Segoe UI"
            i += 1
            continue

        # Image
        m_img = re.match(r'^!\[([^\]]*)\]\(([^)]+\.png)\)', line)
        if m_img:
            rel_path = m_img.group(2).lstrip("./")
            full_p = os.path.join(OUT_DIR, rel_path)
            if os.path.exists(full_p):
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.add_run()
                run.add_picture(full_p, width=Inches(6.2))
            i += 1
            continue

        # Image caption (*Hình ...*)
        if line.startswith("*Hình ") and line.endswith("*"):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_formatted_runs(p, line[1:-1], base_size=9.2, default_italic=True, default_color=RGBColor(71, 85, 105))
            i += 1
            continue

        # Formula Box / Blockquote (> ...)
        if line.startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                q_txt = lines[i].strip()[1:].strip()
                if q_txt:
                    quote_lines.append(q_txt)
                i += 1
            if quote_lines:
                tbl = doc.add_table(rows=1, cols=1)
                cell = tbl.cell(0, 0)
                set_cell_shading(cell, "F0F9FF")
                cell.paragraphs[0].text = ""
                for q_idx, ql in enumerate(quote_lines):
                    p = cell.paragraphs[0] if q_idx == 0 else cell.add_paragraph()
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    add_formatted_runs(p, ql, base_size=10.0)
            continue

        # Table block
        if line.startswith("|"):
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
                table.style = "Table Grid"
                for r_idx, r_cells in enumerate(rows_data):
                    for c_idx in range(min(n_cols, len(r_cells))):
                        cell = table.cell(r_idx, c_idx)
                        if r_idx == 0:
                            set_cell_shading(cell, "EFF6FF")
                        cell.paragraphs[0].text = ""
                        sub_lines = r_cells[c_idx].split("<br>")
                        for s_idx, sl in enumerate(sub_lines):
                            p = cell.paragraphs[0] if s_idx == 0 else cell.add_paragraph()
                            p.paragraph_format.space_before = Pt(1)
                            p.paragraph_format.space_after = Pt(1)
                            add_formatted_runs(p, sl.strip(), base_size=9.2)
                            if r_idx == 0:
                                for r in p.runs:
                                    r.bold = True
            continue

        # Bullet list or numbered list or normal paragraph
        if line.startswith("- ") or line.startswith("* "):
            p = doc.add_paragraph(style="List Bullet")
            add_formatted_runs(p, line[2:].strip(), base_size=10.5)
        else:
            p = doc.add_paragraph()
            add_formatted_runs(p, line, base_size=10.5)
        i += 1

    doc.save(DOCX_PATH)
    print(f"Saved {DOCX_PATH}")


def main():
    with open(MD_PATH, encoding="utf-8") as f:
        md_text = f.read()
    build_html(md_text)
    build_docx(md_text)


if __name__ == "__main__":
    main()
