"""Normalize Arabic text and query terms for better retrieval."""

import re

# Map common variant spellings to canonical forms
_VARIANT_MAP = {
    "نيوكاسيل": "نيوكاسل",
    "النيوكاسيل": "النيوكاسل",
    "كوكسيديا": "كوكسيديا",
    "سالمونيلا": "سالمونيلا",
    "اتش بي": "ايب",
    "اتش ان": "اتش ان",
    "اتشNine": "اتش ان",
}


def normalize_text(text: str) -> str:
    """Normalize Arabic text by mapping variant spellings to canonical forms."""
    if not text:
        return ""
    normalized = text
    for variant, canonical in _VARIANT_MAP.items():
        normalized = re.sub(r"\b" + re.escape(variant) + r"\b", canonical, normalized)
    return normalized


def normalize_query(query: str) -> str:
    """Normalize a user query term-by-term."""
    if not query:
        return ""
    terms = query.split()
    normalized_terms = []
    for term in terms:
        canonical = _VARIANT_MAP.get(term)
        if not canonical:
            if term.startswith("ال") and len(term) > 2:
                inner = term[2:]
                inner_canonical = _VARIANT_MAP.get(inner)
                if inner_canonical:
                    canonical = "ال" + inner_canonical
        normalized_terms.append(canonical or term)
    return " ".join(normalized_terms)

