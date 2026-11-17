"""
Generate PDF from the Viva Guide Markdown file.
Uses fpdf2 with Arabic-capable fonts.
"""

import os
import re
from fpdf import FPDF

# Paths
FONT_DIR = "C:/Windows/Fonts"
ARIAL_FONT = os.path.join(FONT_DIR, "arial.ttf")
ARIAL_BOLD = os.path.join(FONT_DIR, "arialbd.ttf")
MD_FILE = os.path.join(os.path.dirname(__file__), "PROJECT_VIVA_GUIDE_AR_EN.md")
PDF_FILE = os.path.join(os.path.dirname(__file__), "PROJECT_VIVA_GUIDE_AR_EN.pdf")


class VivaPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)
        # Add Arabic-capable fonts
        self.add_font("Arial", "", ARIAL_FONT, uni=True)
        self.add_font("Arial", "B", ARIAL_BOLD, uni=True)
        self.set_font("Arial", "", 10)

    def header(self):
        self.set_font("Arial", "B", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "Poultry Disease RAG System — Viva Guide", align="C", new_x="LMARGIN", new_y="NEXT")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def add_title(self, text, level=1):
        sizes = {1: 20, 2: 16, 3: 13, 4: 11}
        size = sizes.get(level, 10)
        self.set_font("Arial", "B", size)
        self.set_text_color(20, 60, 120)
        self.ln(4)
        self.multi_cell(0, size * 0.55, text)
        self.ln(2)
        if level <= 2:
            self.set_draw_color(91, 143, 168)
            self.set_line_width(0.5)
            self.line(10, self.get_y(), 120, self.get_y())
            self.ln(4)

    def add_body(self, text):
        self.set_font("Arial", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def add_code(self, text):
        self.set_fill_color(240, 240, 240)
        self.set_font("Arial", "", 8)
        self.set_text_color(50, 50, 50)
        x = self.get_x()
        self.set_x(x + 5)
        self.multi_cell(180, 4.5, text, fill=True)
        self.ln(2)

    def add_table_row(self, cells, bold=False, header=False):
        style = "B" if bold or header else ""
        self.set_font("Arial", style, 8)
        if header:
            self.set_fill_color(91, 143, 168)
            self.set_text_color(255, 255, 255)
        else:
            self.set_fill_color(255, 255, 255)
            self.set_text_color(30, 30, 30)

        col_width = 190 / max(len(cells), 1)
        for cell in cells:
            self.cell(col_width, 6, str(cell)[:60], border=1, fill=True)
        self.ln()

    def add_separator(self):
        self.ln(3)
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)


def parse_markdown(md_text):
    """Parse markdown into structured blocks."""
    blocks = []
    lines = md_text.split("\n")
    i = 0
    in_code = False
    code_buf = []
    in_table = False
    table_buf = []

    while i < len(lines):
        line = lines[i]

        # Code blocks
        if line.strip().startswith("```"):
            if in_code:
                blocks.append(("code", "\n".join(code_buf)))
                code_buf = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue

        if in_code:
            code_buf.append(line)
            i += 1
            continue

        # Tables
        if "|" in line and line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            # Skip separator rows (---|---|---)
            if all(re.match(r'^[-:]+$', c) for c in cells):
                i += 1
                continue
            table_buf.append(cells)
            # Check if next line is still a table row
            if i + 1 < len(lines) and "|" in lines[i + 1] and lines[i + 1].strip().startswith("|"):
                i += 1
                continue
            else:
                blocks.append(("table", table_buf))
                table_buf = []
                i += 1
                continue

        # Headers
        if line.startswith("#"):
            match = re.match(r'^(#{1,4})\s+(.+)$', line)
            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                # Remove markdown links
                text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
                blocks.append(("heading", (level, text)))
                i += 1
                continue

        # Horizontal rules
        if line.strip() in ("---", "***", "___"):
            blocks.append(("hr", ""))
            i += 1
            continue

        # Empty lines
        if not line.strip():
            i += 1
            continue

        # Regular text
        clean = line.strip()
        clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', clean)  # Remove bold
        clean = re.sub(r'\*([^*]+)\*', r'\1', clean)       # Remove italic
        clean = re.sub(r'`([^`]+)`', r'\1', clean)         # Remove inline code
        clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', clean)  # Remove links
        if clean:
            blocks.append(("text", clean))

        i += 1

    return blocks


def generate_pdf():
    print("Reading markdown file...")
    with open(MD_FILE, "r", encoding="utf-8") as f:
        md_text = f.read()

    print("Parsing markdown...")
    blocks = parse_markdown(md_text)

    print(f"Found {len(blocks)} blocks")

    pdf = VivaPDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Title page
    pdf.set_font("Arial", "B", 28)
    pdf.set_text_color(20, 60, 120)
    pdf.ln(30)
    pdf.cell(0, 15, "Poultry Disease RAG System", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(91, 143, 168)
    pdf.cell(0, 12, "Viva Defense Guide", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("Arial", "", 14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "Arabic + English Edition", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 8, "25 Professor Questions & Answers", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "10 Identified Bugs & Fixes", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Important Comparisons", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Viva Cheat Sheet", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 8, "Date: 2026-08-27", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Version: 1.0", align="C", new_x="LMARGIN", new_y="NEXT")

    # Content pages
    pdf.add_page()

    for block_type, content in blocks:
        # Check if we need a new page
        if pdf.get_y() > 260:
            pdf.add_page()

        if block_type == "heading":
            level, text = content
            # Start new page for major sections (level 1-2)
            if level <= 2 and pdf.get_y() > 50:
                pdf.add_page()
            pdf.add_title(text, level)

        elif block_type == "text":
            pdf.add_body(content)

        elif block_type == "code":
            pdf.add_code(content)

        elif block_type == "table":
            if content:
                # Header row
                pdf.add_table_row(content[0], header=True)
                # Data rows
                for row in content[1:]:
                    pdf.add_table_row(row)
                pdf.ln(3)

        elif block_type == "hr":
            pdf.add_separator()

    # Save
    print(f"Saving PDF to {PDF_FILE}...")
    pdf.output(PDF_FILE)
    print(f"PDF generated successfully: {PDF_FILE}")
    print(f"File size: {os.path.getsize(PDF_FILE) / 1024:.1f} KB")


if __name__ == "__main__":
    generate_pdf()
