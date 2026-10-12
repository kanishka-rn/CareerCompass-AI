"""Centralized canonicalization for profile interests and domain keywords."""
from __future__ import annotations

import re
from collections.abc import Iterable

from skill_normalizer import normalize_text

INTEREST_ALIASES = {
    "ai": "artificial intelligence", "ml": "machine learning", "dl": "deep learning",
    "data analytics": "data analysis", "data science": "data science", "data analysis": "data analysis",
    "defensive security": "cybersecurity", "ethical hacking": "ethical hacking", "web security": "web security", "network security": "network security",
    "cloud": "cloud computing", "cloud computing": "cloud computing", "devops": "devops", "infrastructure": "infrastructure",
    "embedded": "embedded systems", "embedded systems": "embedded systems", "structural engineering": "structural analysis",
}

def normalize_interest(interest: object) -> str:
    """Return a canonical free-text interest suitable for domain comparisons."""
    cleaned = normalize_text(interest)
    return INTEREST_ALIASES.get(cleaned, cleaned)

def normalize_interests(interests: str | Iterable[object] | None) -> list[str]:
    """Normalize delimited or iterable interests, removing duplicates in input order."""
    values = re.split(r"[,;/\n]+", interests) if isinstance(interests, str) else (interests or [])
    normalized: list[str] = []
    for value in values:
        canonical = normalize_interest(value)
        if canonical and canonical not in normalized:
            normalized.append(canonical)
    return normalized
