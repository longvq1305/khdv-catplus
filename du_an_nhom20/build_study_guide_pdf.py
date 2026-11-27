"""
Compile Cam_Nang_Thuyet_Trinh_Va_Doc_Hieu_Du_An_Nhom20.md into a crisp,
easy-to-read A4 PDF handbook (Cam_Nang_Thuyet_Trinh_Va_Doc_Hieu_Du_An_Nhom20.pdf)
with full Vietnamese font fidelity, clean tables, Q&A callout cards, and page numbers.
"""

import os
import re
import base64
import shutil
import time
import subprocess
import markdown
import pymupdf

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(OUT_DIR, "Cam_Nang_Thuyet_Trinh_Va_Doc_Hieu_Du_An_Nhom20.md")
HTML_PATH = os.path.join(OUT_DIR, "Cam_Nang_Thuyet_Trinh_Va_Doc_Hieu_Du_An_Nhom20.html")
PDF_PATH = os.path.join(OUT_DIR, "Cam_Nang_Thuyet_Trinh_Va_Doc_Hieu_Du_An_Nhom20.pdf")
LOGO_PATH = os.path.join(OUT_DIR, "uet_logo.png")


def build_html():
    with open(MD_PATH, encoding="utf-8") as f:
        raw_md = f.read()

    # Replace file:/// markdown links with clean bold file names & normalize arrows
    clean_md = re.sub(r'\[([^\]]+)\]\(file:///[^)]+\)', r'**\1**', raw_md)
    clean_md = clean_md.replace(r"$\rightarrow$", "→")

    # Strip the top header lines from markdown body because we render a custom hero banner
    lines = clean_md.splitlines()
    body_start = 0
    for idx, ln in enumerate(lines):
        if ln.strip().startswith("> **"):
            body_start = idx
            break

    # Normalize Markdown lists: ensure 4-space indentation for nested bullets & blank line before top-level lists
    norm_lines = []
    for ln in lines[body_start:]:
        # Convert 2-space or 3-space indented sub-bullets to 4-space so Python-Markdown nests them properly
        m_sub = re.match(r'^( {2,3})([-*]\s+.*)$', ln)
        if m_sub:
            ln = "    " + m_sub.group(2)
        # Ensure blank line before top-level list if previous line was normal text
        if re.match(r'^([-*]|\d+\.)\s+', ln) and norm_lines:
            prev = norm_lines[-1].strip()
            if prev and not re.match(r'^([-*]|\d+\.|>|#)', prev):
                norm_lines.append("")
        # Ensure blank line inside blockquote before "> - "
        if ln.strip().startswith("> - ") and norm_lines:
            prev = norm_lines[-1].strip()
            if prev.startswith(">") and not prev.startswith("> -") and prev != ">":
                norm_lines.append(">")
        norm_lines.append(ln)

    md_body = "\n".join(norm_lines)
    body_html = markdown.markdown(md_body, extensions=["tables", "fenced_code", "sane_lists"])

    # Enhance Q&A h3 headings (Câu 1..10) with clean pill styling
    body_html = re.sub(
        r'<h3>(Câu\s+\d+\.)\s*(.*?)</h3>',
        r'<div class="qa-header"><span class="qa-badge">\1</span> <span class="qa-q">\2</span></div>',
        body_html,
    )

    logo_html = ""
    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as lf:
            b64 = base64.b64encode(lf.read()).decode("ascii")
        logo_html = f'<img class="banner-logo" src="data:image/png;base64,{b64}" alt="UET">'

    html_str = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Cẩm nang Đọc hiểu Báo cáo & Thuyết trình — Nhóm 20 CatPlus</title>
<style>
@page {{
    size: A4;
    margin: 16mm 16mm 18mm 16mm;
}}
* {{
    box-sizing: border-box;
}}
body {{
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.52;
    color: #14261E;
    margin: 0;
    padding: 0;
    background: #FFFFFF;
}}

/* Hero Header Banner */
.hero-banner {{
    background: #0F3D2E;
    color: #FFFFFF;
    border-radius: 10px;
    padding: 16px 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 14px;
}}
.banner-logo {{
    width: 58px;
    height: 58px;
    background: #FFFFFF;
    border-radius: 50%;
    padding: 4px;
    flex-shrink: 0;
}}
.banner-tag {{
    display: inline-block;
    background: #FBBF24;
    color: #0F3D2E;
    font-weight: 700;
    font-size: 8.5pt;
    padding: 2px 9px;
    border-radius: 99px;
    margin-bottom: 5px;
    letter-spacing: 0.3px;
}}
.banner-title {{
    font-size: 15pt;
    font-weight: 800;
    line-height: 1.25;
    margin: 0 0 5px 0;
    color: #FFFFFF;
}}
.banner-meta {{
    font-size: 9.5pt;
    color: #D1FAE5;
    margin: 0;
}}

/* Blockquotes (Callout boxes) */
blockquote {{
    margin: 10px 0 14px 0;
    padding: 10px 14px;
    background: #FFFBEB;
    border: 1px solid #FDE68A;
    border-radius: 8px;
    color: #14261E;
    page-break-inside: avoid;
}}
blockquote p {{
    margin: 4px 0;
}}

hr {{
    border: none;
    border-top: 1px solid #DAE2DE;
    margin: 16px 0;
}}

/* Section Headings */
h2 {{
    background: #ECFDF5;
    color: #0F3D2E;
    border: 1px solid #A7F3D0;
    padding: 7px 12px;
    border-radius: 7px;
    font-size: 12.2pt;
    font-weight: 800;
    margin: 18px 0 10px 0;
    page-break-after: avoid;
}}
h3 {{
    color: #C2410C;
    font-size: 11.2pt;
    font-weight: 700;
    margin: 14px 0 6px 0;
    page-break-after: avoid;
}}
h4 {{
    background: #F7F9F8;
    border-left: 3.5px solid #15803D;
    color: #0F3D2E;
    font-size: 10.4pt;
    font-weight: 700;
    padding: 5px 10px;
    margin: 11px 0 5px 0;
    border-radius: 0 5px 5px 0;
    page-break-after: avoid;
}}

p {{
    margin: 5px 0 8px 0;
    text-align: left;
}}

ul, ol {{
    margin: 4px 0 10px 0;
    padding-left: 20px;
}}
li {{
    margin-bottom: 5px;
}}
li > ul {{
    margin-top: 4px;
}}

code {{
    font-family: Consolas, "Courier New", monospace;
    font-size: 9.4pt;
    background: #F3F6F4;
    color: #0F3D2E;
    padding: 1px 5px;
    border-radius: 4px;
    font-weight: 600;
}}

/* Clean Academic & Study Tables */
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0 14px 0;
    font-size: 9.5pt;
}}
thead th {{
    background: #0F3D2E;
    color: #FFFFFF;
    font-weight: 700;
    padding: 7px 9px;
    text-align: left;
    border: 1px solid #0F3D2E;
}}
tbody td {{
    padding: 6px 9px;
    border: 1px solid #DAE2DE;
    vertical-align: top;
}}
tbody tr:nth-child(even) {{
    background: #F8FAF9;
}}
tr {{
    page-break-inside: avoid;
}}

/* Q&A Styled Header */
.qa-header {{
    background: #FFF7ED;
    border: 1px solid #FED7AA;
    border-radius: 7px;
    padding: 6px 11px;
    margin: 12px 0 5px 0;
    page-break-after: avoid;
    page-break-inside: avoid;
}}
.qa-badge {{
    display: inline-block;
    background: #EA580C;
    color: #FFFFFF;
    font-weight: 700;
    font-size: 9pt;
    padding: 1px 7px;
    border-radius: 5px;
    margin-right: 4px;
}}
.qa-q {{
    font-weight: 700;
    color: #9A3412;
    font-size: 10.4pt;
}}
</style>
</head>
<body>

<div class="hero-banner">
  {logo_html}
  <div>
    <div class="banner-tag">TÀI LIỆU ĐỌC HIỂU BẢN CHẤT TỪ GỐC · KHOA HỌC DỊCH VỤ (INT3501)</div>
    <div class="banner-title">Giải nghĩa Sâu Lý thuyết, Cơ chế Toán MILP – Hàng đợi SimPy & Mạch Tư duy CatPlus</div>
    <p class="banner-meta">Đề tài Nhóm 20: Tối ưu hóa ghép đôi gia sư – học viên & xếp lịch học &nbsp;|&nbsp; Phoutthavong Xayavong (23021941) · Vũ Quốc Long (23020105)</p>
  </div>
</div>

{body_html}

</body>
</html>"""

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_str)


def export_stamped_pdf():
    chrome_candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    browser = next((p for p in chrome_candidates if os.path.exists(p)), None)
    if not browser:
        raise RuntimeError("No Chrome/Edge found.")

    temp_html = os.path.join(OUT_DIR, "_temp_guide.html")
    raw_pdf = os.path.join(OUT_DIR, "_temp_guide_raw.pdf")
    shutil.copyfile(HTML_PATH, temp_html)
    if os.path.exists(raw_pdf):
        os.remove(raw_pdf)

    file_url = "file:///" + temp_html.replace("\\", "/")
    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={raw_pdf}",
        file_url,
    ]
    try:
        subprocess.run(cmd, check=True, timeout=45)
    finally:
        for _ in range(5):
            try:
                if os.path.exists(temp_html):
                    os.remove(temp_html)
                break
            except OSError:
                time.sleep(0.3)

    doc = pymupdf.open(raw_pdf)
    total = len(doc)
    for idx, page in enumerate(doc):
        r = page.rect
        footer_box = pymupdf.Rect(45, r.height - 34, r.width - 45, r.height - 14)
        arial_ttf = r"C:\Windows\Fonts\arial.ttf"
        if os.path.exists(arial_ttf):
            page.insert_textbox(
                footer_box,
                f"Cẩm nang Thuyết trình & Đọc hiểu Báo cáo — Nhóm 20 (INT3501)   ·   Trang {idx + 1} / {total}",
                fontsize=8.6,
                fontname="F0",
                fontfile=arial_ttf,
                align=pymupdf.TEXT_ALIGN_CENTER,
                color=(0.32, 0.40, 0.36),
            )
        else:
            page.insert_textbox(
                footer_box,
                f"Trang {idx + 1} / {total}",
                fontsize=9.0,
                fontname="helv",
                align=pymupdf.TEXT_ALIGN_CENTER,
                color=(0.32, 0.40, 0.36),
            )
    doc.save(PDF_PATH)
    doc.close()
    if os.path.exists(raw_pdf):
        os.remove(raw_pdf)
    print(f"Saved {PDF_PATH} ({total} pages)")
    return total


if __name__ == "__main__":
    build_html()
    export_stamped_pdf()
