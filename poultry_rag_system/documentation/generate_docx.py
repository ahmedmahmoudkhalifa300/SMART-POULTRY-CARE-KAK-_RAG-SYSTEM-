# -*- coding: utf-8 -*-
"""
Script to generate a highly professional and styled .docx file in Arabic
documenting the entire Poultry Disease RAG & Vision System.
"""

import os
import sys
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# --- Helper Functions for RTL and Styling ---

def make_p_rtl(p, alignment=WD_ALIGN_PARAGRAPH.RIGHT):
    """Set right-to-left layout and right alignment on a paragraph."""
    p.alignment = alignment
    pPr = p._p.get_or_add_pPr()
    bidi = OxmlElement('w:bidi')
    bidi.set(qn('w:val'), '1')
    pPr.append(bidi)

def add_arabic_run(p, text, font_name="Arial", size_pt=11, bold=False, italic=False, color_rgb=None):
    """Add a run of text and explicitly configure complex script font for Arabic."""
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    if color_rgb:
        run.font.color.rgb = color_rgb
    
    # Configure fonts in XML for complex script rendering (RTL/Arabic)
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn('w:cs'), font_name)
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    
    # Add RTL marker to the run
    rtl = OxmlElement('w:rtl')
    rtl.set(qn('w:val'), '1')
    rPr.append(rtl)
    return run

def add_english_run(p, text, font_name="Calibri", size_pt=10.5, bold=False, italic=False, color_rgb=None):
    """Add a run of text and configure LTR/Latin script fonts."""
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    if color_rgb:
        run.font.color.rgb = color_rgb
        
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    return run

def make_table_rtl(table):
    """Configure a table to render right-to-left layout visually."""
    tblPr = table._tbl.tblPr
    bidiVisual = OxmlElement('w:bidiVisual')
    tblPr.append(bidiVisual)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

def set_cell_background(cell, fill_color):
    """Set the hex background color of a table cell (e.g. '0D3B66')."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_color)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set cell margins in twentieths of a point (dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m_type, m_val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m_type}')
        node.set(qn('w:w'), str(m_val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_styled_heading(doc, text, level, space_before=18, space_after=6):
    """Add an Arabic heading with specific size, color and spacing."""
    p = doc.add_paragraph()
    make_p_rtl(p, alignment=WD_ALIGN_PARAGRAPH.RIGHT)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    
    if level == 1:
        color = RGBColor(13, 59, 102) # Deep Blue
        size = 18
        add_arabic_run(p, text, size_pt=size, bold=True, color_rgb=color)
        
        # Add a bottom border line using paragraph borders XML or just an underline
        # We can add an underline to the run
    elif level == 2:
        color = RGBColor(26, 82, 118) # Medium Blue
        size = 14
        add_arabic_run(p, text, size_pt=size, bold=True, color_rgb=color)
    else:
        color = RGBColor(36, 113, 163) # Light Blue
        size = 12
        add_arabic_run(p, text, size_pt=size, bold=True, color_rgb=color)
    return p

def add_code_block(doc, code_text):
    """Add a LTR code block with Consolas font and light gray background shading."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Inches(0.2)
    p.paragraph_format.line_spacing = 1.0
    
    # Add background shading
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), 'F4F6F7')
    pPr.append(shd)
    
    run = add_english_run(p, code_text, font_name="Consolas", size_pt=9.5, color_rgb=RGBColor(44, 62, 80))
    return p

def add_callout(doc, title, text):
    """Add a highlighted box for important notes."""
    p = doc.add_paragraph()
    make_p_rtl(p, alignment=WD_ALIGN_PARAGRAPH.RIGHT)
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.left_indent = Inches(0.15)
    p.paragraph_format.right_indent = Inches(0.15)
    
    # Shading and left border
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), 'EBF5FB') # light blue tint
    pPr.append(shd)
    
    # Border
    pBdr = OxmlElement('w:pBdr')
    rightBdr = OxmlElement('w:right') # Right border for RTL callouts
    rightBdr.set(qn('w:val'), 'single')
    rightBdr.set(qn('w:sz'), '24') # 3pt
    rightBdr.set(qn('w:space'), '12')
    rightBdr.set(qn('w:color'), '2E86C1')
    pBdr.append(rightBdr)
    pPr.append(pBdr)
    
    add_arabic_run(p, "⚠️ " + title + ": ", size_pt=10.5, bold=True, color_rgb=RGBColor(26, 82, 118))
    add_arabic_run(p, text, size_pt=10.5, italic=True, color_rgb=RGBColor(44, 62, 80))
    return p

# --- Main Document Generation ---

def generate_document():
    doc = Document()
    
    # Configure A4 Page margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.header.is_linked_to_previous = False
        section.footer.is_linked_to_previous = False

    # Define Colors
    color_primary = RGBColor(13, 59, 102) # Deep Blue
    color_secondary = RGBColor(91, 143, 168) # Muted Teal
    
    # ==========================================
    # COVER PAGE (صفحة الغلاف)
    # ==========================================
    for _ in range(3):
        doc.add_paragraph() # Add spacing

    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_after = Pt(12)
    add_arabic_run(title_p, "نظام تشخيص أمراض الدواجن الذكي المعتمد على الاسترجاع المعزز بالتوليد (RAG) والرؤية الحاسوبية", size_pt=24, bold=True, color_rgb=color_primary)
    
    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_p.paragraph_format.space_after = Pt(36)
    add_arabic_run(sub_p, "دليل التوثيق الفني الشامل للمشروع وأدوات التطوير", size_pt=14, bold=False, color_rgb=color_secondary)
    
    for _ in range(8):
        doc.add_paragraph() # Add spacing

    info_p = doc.add_paragraph()
    info_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_arabic_run(info_p, "إعداد وتحليل: فريق عمل المشروع وتطوير الذكاء الاصطناعي\n", size_pt=12, bold=True)
    add_arabic_run(info_p, "تاريخ التوثيق: أغسطس 2026\n", size_pt=11, color_rgb=RGBColor(120, 120, 120))
    add_arabic_run(info_p, "الإصدار: 1.0 (دليل التقييم والمناقشة)", size_pt=10, italic=True)
    
    # Page Break
    doc.add_page_break()
    
    # ==========================================
    # 1. مقدمة ونظرة عامة على المشروع
    # ==========================================
    add_styled_heading(doc, "1. مقدمة ونظرة عامة على المشروع", level=1)
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "يعد مشروع ")
    add_arabic_run(p, "Poultry Disease RAG System", bold=True, color_rgb=color_primary)
    add_arabic_run(p, " مبادرة رائدة لدمج تقنيات الذكاء الاصطناعي الحديثة لدعم وتطوير قطاع تربية الدواجن في مصر. يهدف هذا النظام إلى مساعدة المربين والأطباء البيطريين وأخصائيي الإنتاج الداجني في تشخيص وتحديد أمراض الدواجن بدقة وسرعة، مع تقديم إرشادات علاجية ووقائية موثوقة ومبسطة بالعامية المصرية لتسهيل الفهم والتطبيق الفوري.")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "يتميز النظام بدمج قدرتين أساسيتين في خط إنتاج واحد متكامل:")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "1. التشخيص البصري المدعوم بالتعلم العميق (Computer Vision): ", bold=True)
    add_arabic_run(p, "يقوم مصنف صور مبني باستخدام ")
    add_english_run(p, "TensorFlow/Keras")
    add_arabic_run(p, " بتحليل صور الدواجن أو فضلاتها المرفوعة من قبل المستخدم، وتحديد احتمالية إصابتها بأحد الأمراض الأربعة (الكوكسيديا، السلمونيلا، نيوكاسل، أو حالة سليمة) مع إعطاء نسبة ثقة محددة للنموذج.")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "2. استرجاع المعلومات المعزز بالتوليد (RAG - Retrieval-Augmented Generation): ", bold=True)
    add_arabic_run(p, "يأخذ النظام نتيجة التشخيص البصري (أو سؤال المستخدم المباشر)، ويبحث دلالياً في قاعدة معرفية محلية غنية بملفات بيطرية ")
    add_english_run(p, "(PDF/DOCX)")
    add_arabic_run(p, " موثوقة لاستخلاص أدق التفاصيل حول الأسباب، الأعراض، بروتوكولات العلاج، والوقاية، ثم يصوغها عبر نموذج لغوي كبير ")
    add_english_run(p, "(GPT-4o-mini via OpenRouter)")
    add_arabic_run(p, " بلهجة مصرية عامية ممتازة تناسب المربي المصري البسيط.")

    add_callout(doc, "تنبيه هام", "هذا النظام تم بناؤه كأداة استرشادية مساعدة للتشخيص الفوري ودعم اتخاذ القرار البيطري، ولكنه لا يغني عن المعاينة الميدانية واستشارة الطبيب البيطري المتخصص.")

    # ==========================================
    # 2. الأدوات والتقنيات المستخدمة
    # ==========================================
    add_styled_heading(doc, "2. الأدوات والتقنيات المستخدمة في المشروع (Tech Stack)", level=1)
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "تم اختيار وتطوير مكونات النظام بعناية لضمان التوافق التام، والاستقرار في البيئة المحلية، والسرعة الفائقة في الاستجابة. يوضح الجدول التالي تفاصيل هذه الأدوات ودور كل منها:")

    # Table of Tech Stack
    table = doc.add_table(rows=1, cols=3)
    make_table_rtl(table)
    
    # Headers
    hdr_cells = table.rows[0].cells
    hdr_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hdr_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hdr_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    add_arabic_run(hdr_cells[0].paragraphs[0], "الأداة البرمجية", size_pt=10.5, bold=True, color_rgb=RGBColor(255, 255, 255))
    add_arabic_run(hdr_cells[1].paragraphs[0], "الدور في النظام", size_pt=10.5, bold=True, color_rgb=RGBColor(255, 255, 255))
    add_arabic_run(hdr_cells[2].paragraphs[0], "ملاحظات وتفاصيل التوافق", size_pt=10.5, bold=True, color_rgb=RGBColor(255, 255, 255))
    
    for cell in hdr_cells:
        set_cell_background(cell, "0D3B66")
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        
    tech_data = [
        ("FastAPI", "إطار عمل الخلفية (Backend API)", "يوفر نقاط نهاية سريعة وآمنة (/chat, /image/diagnose) للتحقق من المدخلات تلقائياً ومعالجة الطلبات."),
        ("Streamlit", "الواجهة الأمامية (Frontend UI)", "يوفر واجهة ويب تفاعلية سهلة الاستخدام تحتوي على لوحة تحكم ومساعد شات وواجهة لرفع وفحص الصور."),
        ("SQLite", "قاعدة البيانات الدائمة", "لحفظ تاريخ المحادثات وتاريخ التشخيصات بشكل محلي وخفيف، دون الحاجة لخادم منفصل."),
        ("Sentence-Transformers", "توليد تضمينات النصوص (Embeddings)", "يستخدم نموذج paraphrase-multilingual-MiniLM-L12-v2 لتوليد متجهات دلالية بـ 384 بعداً تدعم العربية والإنجليزية."),
        ("Cross-Encoder", "إعادة ترتيب النصوص (Reranking)", "يستخدم نموذج cross-encoder/ms-marco-MiniLM-L-6-v2 لتقييم دقة التطابق بين الاستعلام والقطع المسترجعة."),
        ("TensorFlow / Keras", "نموذج الرؤية الحاسوبية", "لتشغيل الموديل المدرب poultry_classifier.keras وتصنيف صور الطيور المرفوعة إلى 4 فئات."),
        ("OpenRouter", "الوصول للنماذج اللغوية (LLM)", "يستخدم لتوجيه الأسئلة والسياق إلى نموذج openai/gpt-4o-mini للحصول على شروحات ذكية وسريعة وبأقل تكلفة."),
        ("PyMuPDF + Tesseract OCR", "معالجة وتحميل المستندات", "استخراج النصوص من الـ PDFs مع إمكانية تحويل الصفحات لصور واستخراج النصوص منها ضوئياً في حال كانت scanned.")
    ]
    
    for tool, role, notes in tech_data:
        row_cells = table.add_row().cells
        make_p_rtl(row_cells[0].paragraphs[0])
        make_p_rtl(row_cells[1].paragraphs[0])
        make_p_rtl(row_cells[2].paragraphs[0])
        
        add_arabic_run(row_cells[0].paragraphs[0], tool, size_pt=10, bold=True)
        add_arabic_run(row_cells[1].paragraphs[0], role, size_pt=9.5)
        add_arabic_run(row_cells[2].paragraphs[0], notes, size_pt=9.5)
        
        for cell in row_cells:
            set_cell_background(cell, "F2F4F4")
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)

    doc.add_paragraph() # Spacing

    # ==========================================
    # 3. طرق معالجة النصوص
    # ==========================================
    add_styled_heading(doc, "3. طرق معالجة النصوص (Text Processing Pipeline)", level=1)
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "تمر عملية معالجة النصوص في هذا النظام بخطوات دقيقة تضمن تحويل الملفات المصدرية المكتوبة بصيغ مختلفة وبأقسام معقدة إلى بيانات مهيأة ومطهرة دلالياً للتخزين والاسترجاع السريع:")

    add_styled_heading(doc, "3.1 استخلاص النصوص ودعم الـ OCR البديل (Document Loading)", level=2)
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "يستطيع النظام قراءة صيغتين أساسيتين: ملفات الـ PDF والـ DOCX عبر وحدة ")
    add_english_run(p, "app/rag/loader.py", bold=True)
    add_arabic_run(p, ". بالنسبة لملفات الـ DOCX، يتم استخراج الفقرات والجداول المنسقة. أما بالنسبة لملفات الـ PDF، فيتبع النظام الاستراتيجية التالية:")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "• الاستخراج النصي الأساسي: ", bold=True)
    add_arabic_run(p, "يحاول النظام أولاً استخدام مكتبة ")
    add_english_run(p, "pypdf")
    add_arabic_run(p, " لاستخراج النص الرقمي بسرعة من الصفحات، مع الحفاظ على التنسيق التخطيطي للنصوص.")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "• مستخرج الـ OCR البديل: ", bold=True)
    add_arabic_run(p, "إذا وجد النظام أن النص المستخرج أقل من 500 حرف (مما يدل على أن الـ PDF عبارة عن مستند مصور أو سكانر لا يحتوي على طبقة نصوص)، يقوم تلقائياً بالتحويل لـ OCR باستخدام مكتبة ")
    add_english_run(p, "PyMuPDF (fitz)")
    add_arabic_run(p, " لتحويل صفحات الملف إلى صور بدقة ")
    add_arabic_run(p, "300 DPI", bold=True)
    add_arabic_run(p, "، ثم يمرر الصور إلى محرك ")
    add_english_run(p, "pytesseract")
    add_arabic_run(p, " مهيأ مسبقاً للغتين العربية والإنجليزية معاً ")
    add_english_run(p, "(ara+eng)", bold=True)
    add_arabic_run(p, " للحصول على النص الدقيق المكتوب داخل الصور.")

    add_styled_heading(doc, "3.2 تنظيف وتطبيع النصوص (Text Cleaning & Normalization)", level=2)
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "نظراً لأن استخراج النصوص من ملفات الـ PDF غالباً ما يصاحبه تشويش أو نصوص متكررة (مثل رؤوس الجداول والصفحات)، يقوم التابع ")
    add_english_run(p, "clean_text", bold=True)
    add_arabic_run(p, " بتنقية شاملة عبر:")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "- تطبيع الحروف: ", bold=True)
    add_arabic_run(p, "استخدام معيار NFKC لتسوية الحروف وعلامات الترقيم وتوحيد علامات الاقتباس وإزالة الحروف الخفية.")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "- إزالة التشويش والعبارات المكررة: ", bold=True)
    add_arabic_run(p, "التخلص من عبارات متكررة شائعة في المراجع مثل عبارة (تم إعداده خصيصاً للمربي المصري) أو (الدليل العلمي الشامل لـ...) التي تتكرر بكل صفحة وتفسد جودة التضمين.")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "- تنظيف الجمل المكررة وتطبيع النص العربي: ", bold=True)
    add_arabic_run(p, "يتم تشغيل كود ")
    add_english_run(p, "normalizer.py", bold=True)
    add_arabic_run(p, " الذي يستبدل التهجئات المختلفة لأسماء الأمراض بالصيغة القياسية لتسهيل مطابقتها الدلالية دائمًا، مثل تحويل (نيوكاسيل) إلى (نيوكاسل)، و(النيوكاسيل) إلى (النيوكاسل)، و(اتش بي / اتش ان) إلى اختصاراتها القياسية.")

    add_styled_heading(doc, "3.3 تقسيم النصوص إلى قطع (Chunking Strategy)", level=2)
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "من أهم ركائز الـ RAG هو الحفاظ على المعنى الكامل للفقرات دون بترها في منتصف الجملة. ينفذ النظام استراتيجية تقسيم ذكية ")
    add_english_run(p, "(app/rag/chunking.py)", bold=True)
    add_arabic_run(p, " كالتالي:")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "1. التقسيم الواعي بالجمل (Sentence-Aware) - المفضل: ", bold=True)
    add_arabic_run(p, "يقطع النص أولاً بناءً على علامات الترقيم (. ؟ !) ثم يدمج الجمل المتتالية معاً حتى يصل حجم القطعة إلى ما يقارب ")
    add_arabic_run(p, "450 حرفاً", bold=True)
    add_arabic_run(p, " (ما يعادل 56 كلمة تقريباً). هذا يضمن عدم قطع أي جملة في منتصفها ويحفظ تماسك الفكرة للـ LLM.")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "2. التقسيم المعتمد على الكلمات مع تداخل (Word-Based fallback): ", bold=True)
    add_arabic_run(p, "إذا كان النص خالياً من علامات الترقيم (كفقرة واحدة طويلة)، يتم استخدام نافذة منزلقة تقسم النص حسب الكلمات مع الاحتفاظ بـ ")
    add_arabic_run(p, "200 حرف تداخل (Overlap)", bold=True)
    add_arabic_run(p, " بين القطع المتتالية لتفادي ضياع السياق عند الحواف.")

    add_styled_heading(doc, "3.4 توليد التضمينات وإعادة الترتيب (Embeddings & Reranking)", level=2)
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "بعد التقسيم، يُحوّل النص إلى متجهات رياضية ويُسترجع كالتالي:")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "• نموذج التضمين: ", bold=True)
    add_arabic_run(p, "نستخدم نموذج ")
    add_english_run(p, "paraphrase-multilingual-MiniLM-L12-v2")
    add_arabic_run(p, " الذي يولد متجهات دلالية بـ 384 بعداً. هذا النموذج ممتاز لأنه يدعم اللغة العربية والإنجليزية بطلاقة وخفيف جداً ولا يستهلك موارد الخادم.")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "• قاعدة البيانات المتجهية المحلية (JSON Store): ", bold=True)
    add_arabic_run(p, "نظراً لصغر قاعدة المعرفة وحرصاً على بساطة التثبيت، تُحفظ المتجهات محلياً في ملف JSON ويتم حساب ")
    add_arabic_run(p, "شبه جيب التمام (Cosine Similarity)", bold=True)
    add_arabic_run(p, " للمطابقة الدلالية لاسترجاع أفضل 5 قطع متطابقة.")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "• محرك إعادة الترتيب (Reranking): ", bold=True)
    add_arabic_run(p, "لزيادة الدقة دلالياً وتجنب النتائج الشبيهة لفظياً فقط، يتم تمرير أفضل 5 قطع نصوص مع السؤال إلى نموذج ")
    add_english_run(p, "cross-encoder/ms-marco-MiniLM-L-6-v2")
    add_arabic_run(p, " الذي يقيم مدى الصلة بينهما بدقة شديدة ويعيد ترتيبها، ليختار النظام أفضل 3 قطع نصوص ويقدمها كأهم سياق للنموذج اللغوي.")

    # ==========================================
    # 4. قواعد البيانات والذاكرة
    # ==========================================
    add_styled_heading(doc, "4. قواعد البيانات وإدارة ذاكرة المحادثة (DB & Memory)", level=1)
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "يدير النظام نوعين من المعلومات بشكل متوازٍ: ذاكرة الجلسة التفاعلية قصيرة المدى لدعم المحادثات المستمرة، وقاعدة البيانات الدائمة طويلة المدى لحفظ تاريخ الاستخدام والتشخيصات:")

    add_styled_heading(doc, "4.1 ذاكرة المحادثة المؤقتة للجلسات (In-Memory Conversation Memory)", level=2)
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "للحفاظ على سياق النقاش (مثل عندما يسأل المربي: 'ما هي أعراض الكوكسيديا؟' ثم يتبعه بـ 'وكيف نعالجها؟' دون تكرار اسم المرض)، يوفر المكون ")
    add_english_run(p, "ConversationMemory", bold=True)
    add_arabic_run(p, " داخل ")
    add_english_run(p, "app/rag/pipeline.py")
    add_arabic_run(p, " ذاكرة ذكية:")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "- يتم حفظ الأسئلة والأجوبة السابقة في قاموس محلي بالذاكرة العشوائية مفهرس بمعرف الجلسة ")
    add_english_run(p, "(Session ID)", bold=True)
    add_arabic_run(p, ".")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "- تقتصر الذاكرة على الاحتفاظ بآخر ")
    add_arabic_run(p, "10 جولات محادثة", bold=True)
    add_arabic_run(p, " كحد أقصى لتجنب تجاوز الحد المسموح به من الكلمات (Context Window) للنموذج اللغوي الكبير.")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "- عند إرسال استعلام جديد للنموذج، يتم تضمين آخر 6 جولات من الذاكرة في تاريخ رسائل الـ Chat الممررة للنموذج اللغوي كجزء من سياق المحادثة الموجه.")

    add_styled_heading(doc, "4.2 قاعدة البيانات الدائمة (SQLite Persistence)", level=2)
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "يستخدم النظام قاعدة بيانات ")
    add_english_run(p, "SQLite", bold=True)
    add_arabic_run(p, " المخزنة محلياً في ")
    add_english_run(p, "data/history.sqlite3", bold=True)
    add_arabic_run(p, " لحفظ تاريخ الاستخدام والتشخيصات بشكل دائم. يتكون هيكل البيانات من جدولين رئيسيين:")

    add_code_block(doc, 
"CREATE TABLE chat_history (\n"
"    id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
"    question TEXT NOT NULL,\n"
"    answer TEXT NOT NULL,\n"
"    created_at TEXT NOT NULL\n"
");\n\n"
"CREATE TABLE diagnosis_history (\n"
"    id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
"    disease TEXT NOT NULL,\n"
"    confidence REAL NOT NULL,\n"
"    explanation TEXT NOT NULL,\n"
"    created_at TEXT NOT NULL\n"
");")

    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "• جدول تاريخ المحادثة ")
    add_english_run(p, "(chat_history)", bold=True)
    add_arabic_run(p, ": يسجل تفاصيل محادثات المساعد الذكي لمساعدة واجهة Streamlit على قراءة وحفظ وعرض سجل محادثات المربي السابقة.")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "• جدول تاريخ التشخيصات ")
    add_english_run(p, "(diagnosis_history)", bold=True)
    add_arabic_run(p, ": يسجل تفاصيل فحص الصور، متضمناً اسم المرض المشخص، ونسبة الثقة فيه، والنص الإرشادي المولد بالكامل وتوقيت العملية بالـ UTC.")

    # ==========================================
    # 5. نموذج الرؤية الحاسوبية
    # ==========================================
    add_styled_heading(doc, "5. نموذج الرؤية الحاسوبية بالتفصيل (Vision Model Deep Dive)", level=1)
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "تمثل وحدة الرؤية الحاسوبية بوابة التشخيص البصرية في النظام. هنا شرح دقيق لكيفية بناء النموذج، ومعالجة صوره، واستخلاص تنبؤاته بدقة بيطرية:")

    add_styled_heading(doc, "5.1 معمارية النموذج والبيانات المدخلة (Model Input & Shape)", level=2)
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "يعمل النموذج كأداة تصنيف صور ")
    add_english_run(p, "(Image Classifier)")
    add_arabic_run(p, " مصمم باستخدام شبكة عصبية التلافيفية (CNN) ومحفوظ بصيغة كراس المتكاملة ")
    add_english_run(p, "(.keras)", bold=True)
    add_arabic_run(p, "، حيث تم تدريبه لتصنيف الصور الطبية لفضلات أو أجسام الدواجن إلى الفئات التالية:")

    # Table of classes
    table = doc.add_table(rows=1, cols=3)
    make_table_rtl(table)
    
    hdr_cells = table.rows[0].cells
    hdr_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hdr_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hdr_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    add_arabic_run(hdr_cells[0].paragraphs[0], "فئة المرض (باللغة الإنجليزية)", size_pt=10.5, bold=True, color_rgb=RGBColor(255, 255, 255))
    add_arabic_run(hdr_cells[1].paragraphs[0], "الترجمة العربية والتشخيص المعادل", size_pt=10.5, bold=True, color_rgb=RGBColor(255, 255, 255))
    add_arabic_run(hdr_cells[2].paragraphs[0], "الوصف البيطري المبسط للمرض", size_pt=10.5, bold=True, color_rgb=RGBColor(255, 255, 255))
    
    for cell in hdr_cells:
        set_cell_background(cell, "1A5276")
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        
    class_data = [
        ("Coccidiosis", "الكوكسيديا", "مرض طفيلي خطير يصيب أمعاء الطيور ويدمر الأغشية المخاطية لها، وتظهر فضلات الطيور مصحوبة بدم أو مخاط مع إسهال شديد وخمول في القطيع."),
        ("Salmonella", "السلمونيلا", "عدوى بكتيرية حادة تصيب الدواجن، تسبب إسهالاً أبيض، وتؤدي إلى خمول وتراجع سريع في النمو ونسب نفوق عالية في الكتاكيت الصغيرة."),
        ("New Castle Disease", "مرض نيوكاسل (الروشة)", "مرض فيروسي فائق الخطورة وشديد العدوى، يؤثر على الجهاز التنفسي والهضمي والعصبي مسبباً التواء الرقبة وصوت حشرجة وإسهالاً أخضر ونفوقاً جماعياً."),
        ("Healthy", "حالة سليمة (صحي)", "لا يظهر بالصورة المرفوعة أي ملامح أو مؤشرات لأعراض مرضية واضحة، وتكون الطيور أو الفضلات في حالتها الطبيعية.")
    ]
    
    for cls_en, cls_ar, desc in class_data:
        row_cells = table.add_row().cells
        make_p_rtl(row_cells[0].paragraphs[0])
        make_p_rtl(row_cells[1].paragraphs[0])
        make_p_rtl(row_cells[2].paragraphs[0])
        
        add_arabic_run(row_cells[0].paragraphs[0], cls_en, size_pt=10, bold=True)
        add_arabic_run(row_cells[1].paragraphs[0], cls_ar, size_pt=9.5)
        add_arabic_run(row_cells[2].paragraphs[0], desc, size_pt=9.5)
        
        for cell in row_cells:
            set_cell_background(cell, "F9EBEA" if cls_en != "Healthy" else "EAF2F8")
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)

    doc.add_paragraph() # Spacing

    add_styled_heading(doc, "5.2 مراحل معالجة الصورة المدخلة (Image Preprocessing)", level=2)
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "لكي يتقبل نموذج تصنيف الصور الصورة المرفوعة ويقوم بمعالجتها بشكل سليم دون حدوث أخطاء اختلاف الأبعاد، تقوم وحدة ")
    add_english_run(p, "app/vision/preprocessing.py", bold=True)
    add_arabic_run(p, " بالعمليات المتتالية التالية:")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "1. قراءة الملف وتحويل قنوات الألوان: ", bold=True)
    add_arabic_run(p, "يتم فتح الصورة المرفوعة كملف بايتات خام وتحويلها إلى كائن ")
    add_english_run(p, "PIL Image")
    add_arabic_run(p, "، مع التأكد التام من تحويل نظام الألوان الخاص بها إلى نظام ")
    add_english_run(p, "RGB", bold=True)
    add_arabic_run(p, " ثلاثي القنوات لتفادي الأخطاء في حال كانت الصورة بلون رمادي أو تحتوي على قناة شفافة (Alpha Channel).")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "2. تغيير أبعاد الصورة (Resizing): ", bold=True)
    add_arabic_run(p, "تغيير الأبعاد لتطابق الحجم المدرب عليه النموذج تماماً وهو ")
    add_arabic_run(p, "224 × 224 بكسل", bold=True)
    add_arabic_run(p, "، وهو القياس الموحد الموصى به لتفادي فقدان المعالم أو استهلاك الموارد المفرط.")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "3. تطبيع قيم البكسل (Normalization): ", bold=True)
    add_arabic_run(p, "يتم تحويل قيم البكسلات من النطاق [0, 255] إلى النطاق العشري ")
    add_arabic_run(p, "[0.0, 1.0]", bold=True)
    add_arabic_run(p, " عن طريق قسمة قيم المصفوفة الرقمية للصورة على ")
    add_arabic_run(p, "255.0")
    add_arabic_run(p, "، مما يساعد النموذج الرياضي على معالجة الصورة بشكل مستقر وسريع.")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "4. توسيع الأبعاد (Expanding Dimensions): ", bold=True)
    add_arabic_run(p, "يتم توسيع أبعاد المصفوفة بإضافة بعد إضافي للدفعة (Batch Dimension) ليصبح شكل المدخلات الموجه للنموذج هو ")
    add_arabic_run(p, "(1, 224, 224, 3)", bold=True)
    add_arabic_run(p, " كما تتطلبه مكتبات TensorFlow للاستدلال.")

    add_styled_heading(doc, "5.3 الاستدلال وتطبيق عتبة الثقة (Inference & Confidence Threshold)", level=2)
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "عند تشغيل الاستدلال عبر التابع ")
    add_english_run(p, "predict_proba()", bold=True)
    add_arabic_run(p, "، يقوم النموذج بفرز احتمالية كل فئة مرضية من الفئات الأربعة. ويقوم كود ")
    add_english_run(p, "predictor.py", bold=True)
    add_arabic_run(p, " باختيار المؤشر صاحب القيمة القصوى ")
    add_english_run(p, "(argmax)", bold=True)
    add_arabic_run(p, " ليعلنه كمرض مشخص.")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "• عتبة الثقة البالغة 40% (Confidence Threshold): ", bold=True)
    add_arabic_run(p, "يتخذ النظام قراراً مهماً لحماية المستخدم بيطرياً. فإذا كانت نسبة ثقة النموذج في التشخيص ")
    add_arabic_run(p, "أقل من 40% (0.4)", bold=True)
    add_arabic_run(p, "، يتم إيقاف تدفق الشرح التلقائي وإرسال تحذير صريح للمربي يفيد بأن ثقة التشخيص البصري ضعيفة جداً ومشكوك فيها، ويحثه مباشرة على اللجوء للفحص البيطري الفوري من قِبل طبيب بشري متخصص لتفادي أي خطأ.")

    add_styled_heading(doc, "5.4 الربط التكاملي بين الرؤية والـ RAG في واجهة الشرح", level=2)
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "في حال تخطي عتبة الثقة، تقوم وحدة ")
    add_english_run(p, "DiagnosisExplainer", bold=True)
    add_arabic_run(p, " بربط ناتج الرؤية الحاسوبية بخط أنابيب الـ RAG تلقائياً:")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "1. يولد النظام استعلاماً سرياً دقيقاً باللغة الإنجليزية استناداً إلى اسم المرض المكتشف، للبحث دلالياً في قاعدة المعرفة عن (الأعراض، الأسباب، العلاج، والوقاية) الخاصة بهذا المرض بالتحديد.")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "2. يسترجع النظام القطع الأكثر صلة ويعيد ترتيبها، ثم يسلمها للموجه المخصص ")
    add_english_run(p, "SYSTEM_PROMPT_DIAGNOSIS", bold=True)
    add_arabic_run(p, " الذي يُلزم النموذج اللغوي بصياغة مخرجات الشرح بالترتيب وبالعامية المصرية تماماً كالتالي:")

    add_callout(doc, "تنسيق الشرح المرضي المولد للمربي",
                "\n🐔 تشخيص المرض: [اسم المرض] بثقة [النسبة].\n"
                "⚠️ يُرجى تأكيد التشخيص بواسطة طبيب بيطري.\n\n"
                "🦠 الأسباب: [كيفية العدوى والانتقال]\n\n"
                "🔍 الأعراض: [قائمة نقطية لأهم العلامات]\n\n"
                "💊 العلاج: [الأدوية والمضادات المذكورة بالمرجع بدقة دون اختراع]\n\n"
                "🛡️ الوقاية: [بروتوكول التطهير والتحصين ونظافة العنبر]\n\n"
                "📌 ملاحظة: النتيجة دي معمولة بالذكاء الاصطناعي بهدف المساعدة، لكنها ما تغنيش عن تشخيص الطبيب البيطري.")

    # ==========================================
    # 6. خاتمة وتطلعات مستقبلية
    # ==========================================
    add_styled_heading(doc, "6. التحديات والتطويرات المستقبلية للمشروع", level=1)
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "يمثل النظام الحالي نموذجاً أولياً فائق التماسك والترابط ")
    add_english_run(p, "(Highly Cohesive Scaffold)")
    add_arabic_run(p, "، ولكي يتم الانتقال به لبيئة الإنتاج الضخمة ومساعدة آلاف المربين في مصر، نقترح الخطوات التطويرية التالية:")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "1. الانتقال لقاعدة بيانات متجهية متخصصة: ", bold=True)
    add_arabic_run(p, "استبدال قاعدة بيانات JSON الحالية بمستودع متجهات مخصص مثل ")
    add_english_run(p, "ChromaDB")
    add_arabic_run(p, " أو ")
    add_english_run(p, "FAISS")
    add_arabic_run(p, " لدعم آلاف الملفات البيطرية وقراءتها بكفاءة وسرعة ودون استهلاك للذاكرة العشوائية.")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "2. توسيع نموذج الرؤية الحاسوبية: ", bold=True)
    add_arabic_run(p, "إضافة فئات أمراض جديدة (مثل أنفلونزا الطيور، الالتهاب الشعبي المعدي IB، مرض الجمبورو IBD) مع تدريب الموديل على آلاف الصور المتنوعة لزيادة دقة التشخيص البصري في مختلف ظروف الإضاءة بالمزارع.")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "3. استمرارية الجلسات والمصادقة: ", bold=True)
    add_arabic_run(p, "تطوير قاعدة البيانات لحفظ المحادثات المرتبطة بحسابات المربين، وتفعيل نظام مصادقة ")
    add_english_run(p, "(JWT Authentication)")
    add_arabic_run(p, " لتأمين وصول المستخدمين وتخصيص تجربة الاستخدام لكل مزارع.")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "4. التحديث اللحظي لقاعدة المعرفة: ", bold=True)
    add_arabic_run(p, "تفعيل نقطة النهاية المستهدفة ")
    add_english_run(p, "/upload/pdf", bold=True)
    add_arabic_run(p, " بالكامل، بحيث يستطيع المشرف أو الطبيب رفع ملف PDF جديد في واجهة Streamlit ليقوم النظام بقراءته وتقسيمه وحساب تضميناته وإضافته لقاعدة المعرفة فوراً ودون الحاجة لإعادة تشغيل النظام.")

    doc.add_paragraph() # Spacing
    
    p = doc.add_paragraph()
    make_p_rtl(p, alignment=WD_ALIGN_PARAGRAPH.CENTER)
    add_arabic_run(p, "=== تمت نهاية دليل التوثيق الفني للمشروع ===", size_pt=12, bold=True, color_rgb=color_primary)

    # Save to disk
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "poultry_rag_system_documentation.docx")
    doc.save(output_path)
    print(f"Document successfully created at: {output_path}")

if __name__ == "__main__":
    generate_document()
