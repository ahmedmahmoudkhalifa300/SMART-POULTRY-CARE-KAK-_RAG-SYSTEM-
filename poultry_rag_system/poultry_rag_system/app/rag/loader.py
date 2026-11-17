"""
Loads raw source documents (poultry disease PDFs/DOCXs) from disk so they can be
preprocessed and chunked for indexing into the local vector store.
"""

import os
import re
from dataclasses import dataclass
from pathlib import Path

from app.core.config import settings
from app.core.logger import get_logger
from app.rag.preprocessing import clean_text, remove_boilerplate

logger = get_logger(__name__)

try:
    from pypdf import PdfReader
except ImportError:  # pragma: no cover - import guard
    PdfReader = None

try:
    import pytesseract
except ImportError:  # pragma: no cover - import guard
    pytesseract = None

try:
    import fitz  # PyMuPDF
except ImportError:  # pragma: no cover - import guard
    fitz = None

try:
    from docx import Document
except ImportError:  # pragma: no cover - import guard
    Document = None


@dataclass
class RawDocument:
    source_path: str
    text: str
    metadata: dict


def _clean_extracted_page_text(text: str) -> str:
    """Clean page text to remove broken artifacts and repeated noise."""
    cleaned = remove_boilerplate(text)
    cleaned = re.sub(r"(?<!\w)([A-Za-z]{1,2})(?=\s+[A-Za-z]{1,2})", r"\1", cleaned)
    cleaned = re.sub(r"\s+([,.;:!?])", r"\1", cleaned)
    cleaned = re.sub(r"(?<!\d)\.(?!\d)", ". ", cleaned)
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
    
    # Remove duplicate sentences
    sentences = re.split(r"(?<=[.؟!])\s+", cleaned)
    seen = set()
    unique = []
    for sentence in sentences:
        s = sentence.strip()
        if not s:
            continue
        normalized = re.sub(r"\s+", " ", s)
        if normalized not in seen:
            seen.add(normalized)
            unique.append(s)
    cleaned = " ".join(unique)
    
    return cleaned


def _extract_text_with_pypdf(pdf_path: Path) -> tuple[str, int]:
    """Try to extract text directly from a PDF using pypdf."""
    if PdfReader is None:
        return "", 0

    try:
        reader = PdfReader(str(pdf_path))
    except Exception as exc:  # noqa: BLE001
        logger.warning("Unable to open PDF with pypdf for %s: %s", pdf_path, exc)
        return "", 0

    pages: list[str] = []
    for page_number, page in enumerate(reader.pages, start=1):
        try:
            page_text = page.extract_text(extraction_mode='layout') or ""
        except TypeError:
            page_text = page.extract_text() or ""
        if page_text.strip():
            cleaned_page = _clean_extracted_page_text(page_text)
            if cleaned_page.strip():
                pages.append(f"[Page {page_number}]\n{cleaned_page.strip()}")

    return "\n\n".join(pages).strip(), len(reader.pages)


def _extract_text_with_ocr(pdf_path: Path) -> str:
    """Fallback OCR for scanned PDFs when the text layer is empty."""
    if pytesseract is None or fitz is None:
        return ""

    try:
        os.environ["TESSDATA_PREFIX"] = str(settings.tessdata_prefix)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Could not set TESSDATA_PREFIX: %s", exc)

    try:
        doc = fitz.open(str(pdf_path))
    except Exception as exc:  # noqa: BLE001
        logger.warning("Could not open %s with PyMuPDF for OCR: %s", pdf_path, exc)
        return ""

    texts: list[str] = []
    try:
        for page_number in range(len(doc)):
            page = doc[page_number]
            try:
                pix = page.get_pixmap(dpi=300)
                from PIL import Image
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                extracted = pytesseract.image_to_string(img, lang="ara+eng", config="--psm 6")
            except Exception as exc:  # noqa: BLE001
                logger.warning("OCR failed for page %s in %s: %s", page_number, pdf_path, exc)
                continue

            cleaned_page = _clean_extracted_page_text(extracted)
            if cleaned_page.strip():
                texts.append(f"[Page {page_number + 1}]\n{cleaned_page.strip()}")
    finally:
        doc.close()

    return "\n\n".join(texts).strip()


def load_pdf(path: str | Path) -> RawDocument:
    """Load a single PDF and extract its raw text, using OCR for scanned files if needed."""
    pdf_path = Path(path)

    # Try pypdf first for clean text
    text, page_count = _extract_text_with_pypdf(pdf_path)

    # If pypdf text is too short or heavily corrupted, fall back to OCR
    if len(text.strip()) < 500:
        logger.info("Text from pypdf is too short for %s; trying OCR fallback", pdf_path)
        ocr_text = _extract_text_with_ocr(pdf_path)
        if len(ocr_text.strip()) > len(text.strip()):
            text = ocr_text
            page_count = page_count or 0

    if not text.strip():
        logger.warning("No text could be extracted from %s", pdf_path)

    metadata = {
        "source": pdf_path.name,
        "page_count": page_count or 0,
        "extracted_text_length": len(text),
    }
    return RawDocument(source_path=str(pdf_path), text=text, metadata=metadata)


def load_docx(path: str | Path) -> RawDocument:
    """Load a DOCX file and extract its text content."""
    docx_path = Path(path)

    if Document is None:
        logger.warning("python-docx is not installed; cannot load %s", docx_path)
        return RawDocument(source_path=str(docx_path), text="", metadata={"source": docx_path.name})

    try:
        doc = Document(str(docx_path))
    except Exception as exc:  # noqa: BLE001
        logger.warning("Unable to open DOCX %s: %s", docx_path, exc)
        return RawDocument(source_path=str(docx_path), text="", metadata={"source": docx_path.name})

    parts: list[str] = []

    # Extract paragraphs
    for i, para in enumerate(doc.paragraphs, start=1):
        text = para.text.strip()
        if text:
            parts.append(text)

    # Extract tables
    for ti, table in enumerate(doc.tables, start=1):
        table_rows: list[str] = []
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            table_rows.append(" | ".join(cells))
        if table_rows:
            parts.append(f"[Table {ti}]\n" + "\n".join(table_rows))

    text = "\n\n".join(parts).strip()

    metadata = {
        "source": docx_path.name,
        "page_count": len(doc.paragraphs),
        "extracted_text_length": len(text),
    }

    doc = None  # help GC
    return RawDocument(source_path=str(docx_path), text=text, metadata=metadata)


def load_document(path: str | Path) -> RawDocument | None:
    """Load a document by extension (.pdf or .docx)."""
    path = Path(path)
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return load_pdf(path)
    if suffix == ".docx":
        return load_docx(path)

    logger.warning("Unsupported file format: %s", path)
    return None


def load_documents_from_dir(directory: str | Path = "data/pdfs") -> list[RawDocument]:
    """Load every PDF and DOCX found in the target directory."""
    data_dir = Path(directory)
    if not data_dir.exists():
        return []

    documents: list[RawDocument] = []
    for path in sorted(data_dir.iterdir()):
        if path.suffix.lower() not in {".pdf", ".docx"}:
            continue
        try:
            doc = load_document(path)
            if doc is not None and doc.text.strip():
                documents.append(doc)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Skipping %s: %s", path, exc)
    return documents
