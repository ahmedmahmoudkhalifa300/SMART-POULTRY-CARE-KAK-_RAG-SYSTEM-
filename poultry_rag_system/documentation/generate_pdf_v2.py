"""
Generate PDF from the Viva Guide Markdown file using headless Chromium.
This ensures proper Arabic RTL rendering, BiDi support, and character shaping.
"""

import os
import re
import subprocess
import tempfile
import markdown

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(SCRIPT_DIR, "PROJECT_VIVA_GUIDE_AR_EN.md")
PDF_FILE = os.path.join(SCRIPT_DIR, "PROJECT_VIVA_GUIDE_AR_EN.pdf")
HTML_FILE = os.path.join(SCRIPT_DIR, "PROJECT_VIVA_GUIDE_AR_EN.html")

# Browser paths
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def get_browser():
    """Find available browser."""
    if os.path.exists(CHROME_PATH):
        return CHROME_PATH
    if os.path.exists(EDGE_PATH):
        return EDGE_PATH
    raise RuntimeError("No Chrome or Edge browser found")


def md_to_html(md_text):
    """Convert markdown to HTML with proper extensions."""
    # Convert markdown to HTML
    html_body = markdown.markdown(
        md_text,
        extensions=[
            'tables',
            'fenced_code',
            'codehilite',
            'toc',
            'nl2br',
        ],
        extension_configs={
            'codehilite': {
                'css_class': 'highlight',
                'guess_lang': False,
            }
        }
    )
    return html_body


def build_full_html(html_body):
    """Build complete HTML document with proper RTL/LTR CSS."""
    return f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Poultry Disease RAG System — Viva Guide</title>
    <style>
        /* ===== FONTS ===== */
        @font-face {{
            font-family: 'NotoSansArabic';
            src: local('Noto Sans Arabic'), local('NotoSansArabic');
        }}

        /* ===== BASE ===== */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Tahoma', 'Noto Sans Arabic', 'Segoe UI', Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.7;
            color: #1a1a1a;
            background: #ffffff;
            direction: rtl;
            text-align: right;
            padding: 0;
        }}

        /* ===== PAGE SETUP ===== */
        @page {{
            size: A4;
            margin: 20mm 18mm 25mm 18mm;
            @bottom-center {{
                content: counter(page);
                font-size: 9pt;
                color: #888;
            }}
        }}

        @page :first {{
            margin-top: 0;
            @bottom-center {{ content: none; }}
        }}

        /* ===== HEADINGS ===== */
        h1 {{
            font-size: 24pt;
            font-weight: bold;
            color: #0d3b66;
            margin: 30pt 0 12pt 0;
            padding-bottom: 8pt;
            border-bottom: 3px solid #5b8fa8;
            page-break-after: avoid;
            direction: rtl;
            text-align: right;
        }}

        h2 {{
            font-size: 18pt;
            font-weight: bold;
            color: #1a5276;
            margin: 24pt 0 10pt 0;
            padding-bottom: 6pt;
            border-bottom: 2px solid #5b8fa8;
            page-break-after: avoid;
            direction: rtl;
            text-align: right;
        }}

        h3 {{
            font-size: 14pt;
            font-weight: bold;
            color: #2471a3;
            margin: 18pt 0 8pt 0;
            page-break-after: avoid;
            direction: rtl;
            text-align: right;
        }}

        h4 {{
            font-size: 12pt;
            font-weight: bold;
            color: #2e86c1;
            margin: 14pt 0 6pt 0;
            page-break-after: avoid;
            direction: rtl;
            text-align: right;
        }}

        /* ===== PARAGRAPHS ===== */
        p {{
            margin: 6pt 0;
            text-align: justify;
            direction: rtl;
            unicode-bidi: embed;
        }}

        /* ===== LISTS ===== */
        ul, ol {{
            margin: 8pt 0;
            padding-right: 24pt;
            padding-left: 0;
            direction: rtl;
        }}

        li {{
            margin: 4pt 0;
            text-align: right;
            direction: rtl;
        }}

        /* ===== TABLES ===== */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 12pt 0;
            font-size: 10pt;
            direction: rtl;
            page-break-inside: avoid;
        }}

        thead {{
            background-color: #5b8fa8;
            color: #ffffff;
        }}

        th {{
            padding: 8pt 10pt;
            text-align: right;
            font-weight: bold;
            border: 1px solid #4a7a95;
            direction: rtl;
        }}

        td {{
            padding: 7pt 10pt;
            text-align: right;
            border: 1px solid #ddd;
            direction: rtl;
        }}

        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}

        tr:hover {{
            background-color: #e8f4f8;
        }}

        /* ===== CODE BLOCKS — ALWAYS LTR ===== */
        pre {{
            background-color: #1e1e2e;
            color: #cdd6f4;
            padding: 12pt 14pt;
            border-radius: 8px;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 9pt;
            line-height: 1.5;
            direction: ltr !important;
            text-align: left !important;
            unicode-bidi: isolate;
            overflow-x: auto;
            margin: 10pt 0;
            page-break-inside: avoid;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}

        code {{
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 9.5pt;
            background-color: #f0f0f0;
            padding: 1pt 4pt;
            border-radius: 3px;
            direction: ltr !important;
            unicode-bidi: isolate;
        }}

        pre code {{
            background-color: transparent;
            padding: 0;
            direction: ltr !important;
            text-align: left !important;
        }}

        /* ===== BLOCKQUOTE ===== */
        blockquote {{
            border-right: 4px solid #5b8fa8;
            border-left: none;
            padding: 8pt 16pt;
            margin: 10pt 0;
            background-color: #f0f7fb;
            color: #2c3e50;
            direction: rtl;
        }}

        /* ===== HORIZONTAL RULE ===== */
        hr {{
            border: none;
            border-top: 2px solid #5b8fa8;
            margin: 20pt 0;
        }}

        /* ===== STRONG / BOLD ===== */
        strong, b {{
            font-weight: bold;
            color: #1a1a1a;
        }}

        /* ===== LINKS ===== */
        a {{
            color: #2471a3;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        /* ===== SPECIAL: English/LTR content inside RTL ===== */
        /* Technical terms, file paths, API endpoints stay LTR */
        .ltr {{
            direction: ltr;
            text-align: left;
            unicode-bidi: isolate;
            display: inline;
        }}

        /* ===== TITLE PAGE ===== */
        .title-page {{
            text-align: center;
            direction: rtl;
            page-break-after: always;
            padding-top: 80pt;
        }}

        .title-page h1 {{
            font-size: 32pt;
            border: none;
            color: #0d3b66;
            margin-bottom: 8pt;
        }}

        .title-page .subtitle {{
            font-size: 20pt;
            color: #5b8fa8;
            margin-bottom: 30pt;
        }}

        .title-page .edition {{
            font-size: 14pt;
            color: #666;
            margin-bottom: 40pt;
        }}

        .title-page .features {{
            font-size: 12pt;
            color: #444;
            line-height: 2.2;
        }}

        .title-page .date {{
            font-size: 10pt;
            color: #999;
            margin-top: 40pt;
        }}

        /* ===== SECTION BREAKS ===== */
        .section-break {{
            page-break-before: always;
        }}

        /* ===== EMOJI FALLBACK ===== */
        /* Ensure emoji don't break layout */
        .emoji {{
            font-family: 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji', sans-serif;
        }}

        /* ===== PRINT OPTIMIZATIONS ===== */
        @media print {{
            body {{
                font-size: 10pt;
            }}

            pre {{
                font-size: 8.5pt;
                white-space: pre-wrap;
            }}

            table {{
                font-size: 9pt;
            }}

            h1 {{ font-size: 22pt; }}
            h2 {{ font-size: 16pt; }}
            h3 {{ font-size: 13pt; }}
        }}
    </style>
</head>
<body>
{html_body}
</body>
</html>'''


def convert_html_to_pdf(html_path, pdf_path, browser_path):
    """Use headless Chromium to convert HTML to PDF."""
    # Use absolute file URL
    abs_html_path = os.path.abspath(html_path).replace("\\", "/")
    file_url = f"file:///{abs_html_path}"

    cmd = [
        browser_path,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-software-rasterizer",
        f"--print-to-pdf={os.path.abspath(pdf_path)}",
        "--print-to-pdf-no-header",
        "--no-pdf-header-footer",
        "--disable-extensions",
        "--disable-plugins",
        file_url,
    ]

    print(f"Running: {' '.join(cmd[:6])}...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

    if result.returncode != 0:
        print(f"STDERR: {result.stderr}")
        raise RuntimeError(f"Browser returned {result.returncode}")

    if not os.path.exists(pdf_path):
        raise RuntimeError("PDF file was not created")

    size_kb = os.path.getsize(pdf_path) / 1024
    print(f"PDF created: {pdf_path} ({size_kb:.1f} KB)")


def main():
    print("=" * 60)
    print("  PDF Generation — Arabic RTL Support via Chromium")
    print("=" * 60)

    # 1. Read markdown
    print("\n[1/4] Reading markdown file...")
    with open(MD_FILE, "r", encoding="utf-8") as f:
        md_text = f.read()
    print(f"  Read {len(md_text)} characters")

    # 2. Convert to HTML
    print("\n[2/4] Converting markdown to HTML...")
    html_body = md_to_html(md_text)
    full_html = build_full_html(html_body)

    # 3. Save HTML (for debugging)
    print("\n[3/4] Saving HTML file...")
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"  HTML saved: {HTML_FILE}")

    # 4. Convert to PDF
    print("\n[4/4] Converting HTML to PDF via headless Chromium...")
    browser = get_browser()
    print(f"  Using browser: {browser}")
    convert_html_to_pdf(HTML_FILE, PDF_FILE, browser)

    # Verify
    print("\n" + "=" * 60)
    print("  VERIFICATION")
    print("=" * 60)
    pdf_size = os.path.getsize(PDF_FILE)
    print(f"  PDF file: {PDF_FILE}")
    print(f"  PDF size: {pdf_size / 1024:.1f} KB")
    print(f"  HTML file: {HTML_FILE}")
    print(f"  HTML size: {os.path.getsize(HTML_FILE) / 1024:.1f} KB")
    print("\n  Arabic RTL rendering handled by Chromium's BiDi engine.")
    print("  Technical terms (FastAPI, Python, etc.) remain LTR.")
    print("  Code blocks remain LTR.")
    print("=" * 60)


if __name__ == "__main__":
    main()
