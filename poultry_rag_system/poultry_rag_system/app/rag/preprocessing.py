"""Text cleaning and normalization applied to raw document text before chunking."""

import re
import unicodedata

from app.core.logger import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Known noise fragments produced by corrupted PDF text extraction.
# These appear in the poultry disease PDFs as repeated text-box artifacts.
# ---------------------------------------------------------------------------
_NOISE_PATTERNS = [
    # Vaccination guide noise
    r"تم\s*إعداده\s*خصيصاً\s*للمربي\s*المصري(?:\s*[\|\.]\s*(?:م\.\s*أجنتك\s*\d+)?)?",
    r"ولكنها",
    r"أجنتك",
    r"م\.\s*أجنتك\s*\d+",
    r"قاعدة",
    r"هذا",
    r"صفحة\s*\d+\s*من\s*\d+",
    r"الدليل\s*العلمي\s*الشامل\s*لأمراض\s*وتحصين\s*دواجن\s*التسم(?:دواجن\s*التسم)*",
    # Management guide noise
    r"الشغل\s*ده\s*بيبدأ\s*قبل\s*الاستلام\s*ب",
    r"تدمر",
    r"القطيع",
    r"كان",
    r"أمراض",
    r"دليل\s*التربية\s*العملي\s*لنجاح\s*دورة\s*تسم(?:مهم\s*جداً)?",
    r"روشتة\s*عملية\s*مجربة\s*من\s*أرض\s*العنبر\s*-\s*من\s*التطهير\s*حتى\s*البيع\s*بالعامية\s*المصر",
    # Common OCR artifacts
    r"ولكنها(?:في|ف)?",
    r"أجنتك\s*",
    r"\b(?:٠|٥|٤|٦|٨|٠٠|٥٠)\b",
    r"[\*\-\+]{2,}",
]

# Words that are pure noise when isolated or heavily repeated
_NOISE_WORDS = {
    "أجنتك", "قاعدة", "هذا", "تدمر", "كان",
    "م.", "م", "٠", "٥", "٤", "٦", "٨", "٠٠", "٥٠",
    "ولكنها", "أولاً", "ثانياً", "صفحة", "ده", "هي",
}


def _remove_noise(text: str) -> str:
    for pattern in _NOISE_PATTERNS:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    return text


def _remove_noise_words(text: str) -> str:
    tokens = text.split()
    cleaned = [token for token in tokens if token not in _NOISE_WORDS]
    return " ".join(cleaned)


def _dedup_words(text: str) -> str:
    tokens = text.split()
    if not tokens:
        return text
    result = [tokens[0]]
    for token in tokens[1:]:
        if token != result[-1]:
            result.append(token)
    return " ".join(result)


def _remove_duplicate_sentences(text: str) -> str:
    sentences = re.split(r"(?<=[.؟!])\s+", text)
    seen = set()
    unique = []
    for sentence in sentences:
        s = sentence.strip()
        if not s:
            continue
        # Normalize for comparison
        normalized = re.sub(r"\s+", " ", s)
        if normalized not in seen:
            seen.add(normalized)
            unique.append(s)
    return " ".join(unique)


def _remove_repeated_words(text: str) -> str:
    tokens = text.split()
    if not tokens:
        return text
    result = [tokens[0]]
    for token in tokens[1:]:
        if token != result[-1]:
            result.append(token)
    return " ".join(result)


def _clean_symbols(text: str) -> str:
    text = re.sub(r"[()\[\]{}<>/\\|~`@#$%^&*_=+;]", " ", text)
    text = re.sub(r"\s{2,}", " ", text).strip()
    return text


def clean_text(text: str) -> str:
    """Normalize extracted PDF text into a cleaner string for chunking."""
    if not text:
        return ""

    normalized = unicodedata.normalize("NFKC", text)
    normalized = normalized.replace("“", '"').replace("”", '"').replace("’", "'")
    normalized = normalized.replace("\u00a0", " ")
    normalized = normalized.replace("\u200f", "")
    normalized = normalized.replace("\u200e", "")
    normalized = normalized.replace("|", " ")

    normalized = re.sub(r"([A-Za-z])\s*-\s*\n\s*", r"\1", normalized)
    normalized = re.sub(r"([A-Za-z])\s*-\s*", r"\1", normalized)
    normalized = re.sub(r"\n{2,}", "\n\n", normalized)
    normalized = re.sub(r"([\w])\s+(?=[،.;:!?])", r"\1", normalized)
    normalized = re.sub(r"(?<!\d)([.]{2,})(?!\d)", ".", normalized)
    normalized = re.sub(r"(?<!\w)\.(?!\w)", ". ", normalized)
    normalized = re.sub(r"[ \t\r\f\v]+", " ", normalized)
    normalized = re.sub(r"\s*\n\s*", " ", normalized)
    normalized = re.sub(r"\s{2,}", " ", normalized).strip()

    normalized = _remove_noise(normalized)
    normalized = _remove_noise_words(normalized)
    normalized = _dedup_words(normalized)
    normalized = _remove_duplicate_sentences(normalized)
    normalized = _clean_symbols(normalized)
    normalized = re.sub(r"\s{2,}", " ", normalized).strip()

    return normalized


def remove_boilerplate(text: str, patterns: list[str] | None = None) -> str:
    """Strip recurring boilerplate from extracted document text."""
    if not text:
        return ""

    regex_patterns = patterns or [
        r"copyright.*?$",
        r"all rights reserved.*?$",
        r"page\s*\d+.*?$",
    ]
    cleaned = text
    for pattern in regex_patterns:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE | re.MULTILINE)
    return re.sub(r"\s{2,}", " ", cleaned).strip()
