# -*- coding: utf-8 -*-
"""
Script to generate a highly professional and styled .docx file in Arabic
documenting specifically the Vision Model for the Poultry Disease RAG System.
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
    elif level == 2:
        color = RGBColor(26, 82, 118) # Medium Blue
        size = 14
        add_arabic_run(p, text, size_pt=size, bold=True, color_rgb=color)
    else:
        color = RGBColor(36, 113, 163) # Light Blue
        size = 12
        add_arabic_run(p, text, size_pt=size, bold=True, color_rgb=color)
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
    add_arabic_run(title_p, "الدليل التفصيلي لنموذج الرؤية الحاسوبية", size_pt=26, bold=True, color_rgb=color_primary)
    
    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_p.paragraph_format.space_after = Pt(36)
    add_arabic_run(sub_p, "ضمن نظام تشخيص أمراض الدواجن الذكي (Poultry Disease RAG System)", size_pt=16, bold=False, color_rgb=color_secondary)
    
    for _ in range(8):
        doc.add_paragraph() # Add spacing

    info_p = doc.add_paragraph()
    info_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_arabic_run(info_p, "إعداد وتحليل: فريق عمل المشروع وتطوير الذكاء الاصطناعي\n", size_pt=12, bold=True)
    add_arabic_run(info_p, "تاريخ التوثيق: أغسطس 2026\n", size_pt=11, color_rgb=RGBColor(120, 120, 120))
    add_arabic_run(info_p, "الإصدار: 1.0 (توثيق تقني للنموذج)", size_pt=10, italic=True)
    
    # Page Break
    doc.add_page_break()
    
    # ==========================================
    # 1. مقدمة عن نموذج الرؤية
    # ==========================================
    add_styled_heading(doc, "1. مقدمة عن نموذج الرؤية الحاسوبية", level=1)
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "تمثل وحدة الرؤية الحاسوبية ")
    add_english_run(p, "(Computer Vision Module)")
    add_arabic_run(p, " بوابة التشخيص البصرية في نظام أمراض الدواجن. يعتمد النظام على نموذج ذكاء اصطناعي مدرب لتحليل صور الدواجن أو فضلاتها المرفوعة من قبل المربي، ليقوم باكتشاف ما إذا كان الطائر سليماً أو مصاباً بأحد الأمراض المحددة.")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "الهدف من النموذج هو تقديم أداة مساعدة سريعة للتشخيص الأولي ودعم اتخاذ القرار البيطري، مع ربطه لاحقاً بنظام استرجاع المعلومات ")
    add_english_run(p, "(RAG)")
    add_arabic_run(p, " لتوليد إرشادات علاجية ووقائية بالعامية المصرية.")

    # ==========================================
    # 2. معمارية النموذج والبيانات المدخلة
    # ==========================================
    add_styled_heading(doc, "2. معمارية النموذج (Model Architecture)", level=1)
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "يعمل النموذج كأداة تصنيف صور ")
    add_english_run(p, "(Image Classifier)")
    add_arabic_run(p, " مصمم باستخدام شبكة عصبية تلافيفية ")
    add_english_run(p, "(CNN)")
    add_arabic_run(p, " ومحفوظ بصيغة كراس المتكاملة ")
    add_english_run(p, "(models/poultry_classifier.keras)", bold=True)
    add_arabic_run(p, ". تم بناء هذا النموذج باستخدام إطار عمل ")
    add_english_run(p, "TensorFlow / Keras", bold=True)
    add_arabic_run(p, ".")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "وحدة معالجة الاستدلال الخاصة بالنموذج متواجدة داخل ملف ")
    add_english_run(p, "app/vision/classifier.py", bold=True)
    add_arabic_run(p, "، حيث تم بناء غلاف (Wrapper) بنمط (Singleton) لضمان تحميل الموديل مرة واحدة فقط في الذاكرة عند بدء تشغيل الخادم، مما يضمن سرعة كبيرة في معالجة الصور المتتالية.")

    add_styled_heading(doc, "2.1 الفئات المرضية المدرب عليها النموذج (Classes)", level=2)
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "تم تدريب النموذج على تصنيف الصور المدخلة إلى 4 فئات رئيسية:")

    # Table of classes
    table = doc.add_table(rows=1, cols=3)
    make_table_rtl(table)
    
    hdr_cells = table.rows[0].cells
    hdr_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hdr_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hdr_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    add_arabic_run(hdr_cells[0].paragraphs[0], "فهرس الفئة (Index)", size_pt=10.5, bold=True, color_rgb=RGBColor(255, 255, 255))
    add_arabic_run(hdr_cells[1].paragraphs[0], "اسم المرض (الإنجليزي / العربي)", size_pt=10.5, bold=True, color_rgb=RGBColor(255, 255, 255))
    add_arabic_run(hdr_cells[2].paragraphs[0], "نبذة عن الفئة", size_pt=10.5, bold=True, color_rgb=RGBColor(255, 255, 255))
    
    for cell in hdr_cells:
        set_cell_background(cell, "1A5276")
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        
    class_data = [
        ("0", "Coccidiosis (الكوكسيديا)", "مرض طفيلي خطير يصيب الأمعاء، ويُستدل عليه بفضلات دموية أو مخاطية."),
        ("1", "Healthy (حالة سليمة / صحي)", "لا توجد مؤشرات لأعراض مرضية، والطائر سليم."),
        ("2", "New Castle Disease (نيوكاسل)", "مرض فيروسي يصيب الجهاز العصبي والتنفسي، يسبب التواء الرقبة وإسهال أخضر."),
        ("3", "Salmonella (السلمونيلا)", "عدوى بكتيرية حادة، تسبب إسهالاً أبيض وتراجع في النمو.")
    ]
    
    for idx, cls_name, desc in class_data:
        row_cells = table.add_row().cells
        make_p_rtl(row_cells[0].paragraphs[0], alignment=WD_ALIGN_PARAGRAPH.CENTER)
        make_p_rtl(row_cells[1].paragraphs[0])
        make_p_rtl(row_cells[2].paragraphs[0])
        
        add_arabic_run(row_cells[0].paragraphs[0], idx, size_pt=10, bold=True)
        add_arabic_run(row_cells[1].paragraphs[0], cls_name, size_pt=10, bold=True)
        add_arabic_run(row_cells[2].paragraphs[0], desc, size_pt=9.5)
        
        for cell in row_cells:
            set_cell_background(cell, "F9EBEA" if idx != "1" else "EAF2F8")
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)

    # ==========================================
    # 3. مراحل المعالجة المسبقة للصورة
    # ==========================================
    add_styled_heading(doc, "3. مراحل المعالجة المسبقة للصورة (Image Preprocessing)", level=1)
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "لكي يتقبل نموذج التصنيف الصورة المرفوعة ويقوم بمعالجتها بشكل سليم دون أخطاء في الأبعاد، تقوم وحدة ")
    add_english_run(p, "app/vision/preprocessing.py", bold=True)
    add_arabic_run(p, " بالعمليات المتتالية التالية:")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "1. قراءة الملف وتحويل قنوات الألوان (RGB Conversion): ", bold=True)
    add_arabic_run(p, "يتم فتح الصورة المرفوعة كملف بايتات خام وتحويلها إلى كائن ")
    add_english_run(p, "PIL Image")
    add_arabic_run(p, "، مع التأكد التام من تحويل نظام الألوان الخاص بها إلى نظام ")
    add_english_run(p, "RGB", bold=True)
    add_arabic_run(p, " ثلاثي القنوات. هذا التحويل ضروري لتفادي الأخطاء في حال كانت الصورة تحتوي على قناة شفافة (Alpha) مثل صور PNG، أو إذا كانت صورة ذات تدرج رمادي (Grayscale).")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "2. تغيير أبعاد الصورة (Resizing): ", bold=True)
    add_arabic_run(p, "يتطلب النموذج المدرب أبعاداً محددة لجميع الصور المدخلة. لذا يتم تغيير أبعاد الصورة لتطابق الحجم القياسي وهو ")
    add_arabic_run(p, "224 × 224 بكسل", bold=True)
    add_arabic_run(p, ".")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "3. تطبيع قيم البكسل (Normalization): ", bold=True)
    add_arabic_run(p, "يتم تحويل قيم البكسلات التي تكون في النطاق الرقمي المعتاد [0, 255] إلى نطاق عشري صغير يقع بين ")
    add_arabic_run(p, "[0.0, 1.0]", bold=True)
    add_arabic_run(p, "، وذلك من خلال قسمة قيم المصفوفة الرقمية (Numpy Array) للصورة على الرقم ")
    add_arabic_run(p, "255.0")
    add_arabic_run(p, ". يساعد هذا التطبيع الشبكة العصبية على التعلم بشكل أسرع والحفاظ على استقرار العمليات الحسابية أثناء الاستدلال.")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "4. توسيع الأبعاد (Expanding Dimensions): ", bold=True)
    add_arabic_run(p, "تتوقع واجهة TensorFlow (أو Keras) تلقي دفعة (Batch) من الصور حتى لو كانت صورة واحدة. لذلك يتم إضافة بعد جديد (Batch Dimension) ليصبح شكل المصفوفة النهائي الموجه للنموذج هو ")
    add_arabic_run(p, "(1, 224, 224, 3)", bold=True)
    add_arabic_run(p, ".")

    # ==========================================
    # 4. الاستدلال واتخاذ القرار (Inference & Threshold)
    # ==========================================
    add_styled_heading(doc, "4. الاستدلال وتطبيق عتبة الثقة (Inference Logic & Threshold)", level=1)
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "بعد إعداد الصورة، تبدأ عملية التوقع من خلال ملف ")
    add_english_run(p, "app/vision/predictor.py", bold=True)
    add_arabic_run(p, ":")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "• استخراج الاحتماليات (Probabilities): ", bold=True)
    add_arabic_run(p, "يقوم التابع ")
    add_english_run(p, "predict_proba()", bold=True)
    add_arabic_run(p, " بإخراج مصفوفة من 4 قيم احتمالية، كل قيمة تمثل نسبة احتمال انتماء الصورة لفئة معينة من الفئات الأربعة. ويتم اختيار الفئة صاحبة أعلى قيمة بواسطة دالة ")
    add_english_run(p, "argmax", bold=True)
    add_arabic_run(p, ".")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "• عتبة الثقة الحرجة (40% Confidence Threshold): ", bold=True)
    add_arabic_run(p, "للحفاظ على الموثوقية البيطرية وعدم تضليل المربي بمعلومات خاطئة، يعتمد النظام على عتبة ثقة صارمة. إذا كانت نسبة ثقة النموذج في التشخيص ")
    add_arabic_run(p, "أقل من 40% (0.4)", bold=True)
    add_arabic_run(p, "، يرفض النظام تقديم خطة علاجية قطعية. بدلاً من ذلك، يقوم بإيقاف تدفق الـ RAG ويولد تحذيراً صريحاً يوضح للمربي أن نتيجة التصنيف غير دقيقة، وينصحه بإعادة التقاط صورة أوضح أو استشارة طبيب بيطري فوراً.")

    # ==========================================
    # 5. التكامل مع محرك RAG والشرح البيطري
    # ==========================================
    add_styled_heading(doc, "5. التكامل بين النموذج البصري ونظام RAG", level=1)
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "في حال تجاوزت نسبة ثقة النموذج العتبة المطلوبة (أعلى من 40%)، يتدخل مكون ")
    add_english_run(p, "app/vision/explainer.py", bold=True)
    add_arabic_run(p, " لإنشاء الجسر بين الرؤية الحاسوبية ونظام استرجاع المعلومات:")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "1. يقوم النظام آلياً بتوليد استعلام استكشافي صامت باللغة الإنجليزية كالتالي: ")
    add_english_run(p, "'symptoms causes treatment prevention of {disease_name} in poultry'")
    add_arabic_run(p, ".")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "2. يُرسل هذا الاستعلام إلى محرك الـ RAG، الذي يبحث في الملفات البيطرية الموثوقة المحفوظة بالـ Vector Store، ليستخرج أهم الفقرات المتعلقة بالمرض المحدد.")
    
    p = doc.add_paragraph()
    make_p_rtl(p)
    add_arabic_run(p, "3. يتم تمرير نتائج الـ RAG إلى النموذج اللغوي (LLM) مع موجه خاص ")
    add_english_run(p, "(SYSTEM_PROMPT_DIAGNOSIS)")
    add_arabic_run(p, " يجبر النموذج على صياغة الشرح بالعامية المصرية المبسطة وتضمين رموز تعبيرية محددة لتسهيل القراءة.")

    add_callout(doc, "هيكل الشرح النهائي المولد للمربي",
                "\n🐔 تشخيص المرض: [اسم المرض] بثقة [النسبة].\n"
                "⚠️ يُرجى تأكيد التشخيص بواسطة طبيب بيطري.\n\n"
                "🦠 الأسباب: [مسببات المرض المستخرجة من المستندات البيطرية]\n\n"
                "🔍 الأعراض: [الأعراض المرئية والظاهرية على القطيع]\n\n"
                "💊 العلاج: [الأدوية والمضادات الموثوقة الموجودة بالمرجع]\n\n"
                "🛡️ الوقاية: [إجراءات التطهير والتحصين]\n\n"
                "📌 ملاحظة: النتيجة دي معمولة بالذكاء الاصطناعي للمساعدة، وما تغنيش عن الطبيب البيطري.")
    
    # Save to disk
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "poultry_vision_model_documentation.docx")
    doc.save(output_path)
    print(f"Document successfully created at: {output_path}")

if __name__ == "__main__":
    generate_document()
