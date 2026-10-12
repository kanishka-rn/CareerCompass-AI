"""Centralized skill canonicalization used by all CareerCompass modules."""
from __future__ import annotations
import re
from collections.abc import Iterable

SKILL_ALIASES = {
    "py": "python", "python": "python", "js": "javascript", "javascript": "javascript", "html5": "html", "html": "html", "css3": "css", "css": "css",
    "ml": "machine learning", "machine learning": "machine learning", "ai": "artificial intelligence", "artificial intelligence": "artificial intelligence", "dl": "deep learning", "deep learning": "deep learning",
    "dsa": "data structures and algorithms", "data structures": "data structures and algorithms", "data structures and algorithms": "data structures and algorithms",
    "np": "numpy", "numpy": "numpy", "pd": "pandas", "pandas": "pandas", "powerbi": "power bi", "power bi": "power bi", "sql": "sql", "structured query language": "sql",
    "oop": "object oriented programming", "oops": "object oriented programming", "object oriented programming": "object oriented programming", "cv": "computer vision", "computer vision": "computer vision", "nlp": "natural language processing", "natural language processing": "natural language processing",
    "cyber security": "cybersecurity", "cybersecurity": "cybersecurity", "ethical hacker": "ethical hacking", "ethical hacking": "ethical hacking", "burp": "burp suite", "burpsuite": "burp suite", "burp suite": "burp suite",
    "aws cloud": "aws", "amazon web services": "aws", "aws": "aws", "gcp": "google cloud", "google cloud platform": "google cloud", "google cloud": "google cloud", "k8s": "kubernetes", "kubernetes": "kubernetes",
    "nodejs": "node.js", "node": "node.js", "node.js": "node.js", "reactjs": "react", "react.js": "react", "github": "git", "git hub": "git", "scikit learn": "scikit-learn", "sklearn": "scikit-learn", "data analytics": "data analysis", "digital electronics": "electronics", "embedded": "embedded systems",
}

def normalize_skill(skill: object) -> str:
    """Return a lower-case canonical skill; invalid or blank values become empty."""
    if not isinstance(skill, str): return ""
    cleaned = re.sub(r"\s+", " ", skill.strip().lower().replace("_", " "))
    return SKILL_ALIASES.get(cleaned, cleaned)

def normalize_skills(skills: str | Iterable[object] | None) -> list[str]:
    """Normalize delimited or iterable skills, remove duplicates, retain input order."""
    items = re.split(r"[,;/\n]+", skills) if isinstance(skills, str) else (skills or [])
    result: list[str] = []
    for item in items:
        canonical = normalize_skill(item)
        if canonical and canonical not in result: result.append(canonical)
    return result

def normalize_text(text: object) -> str:
    return re.sub(r"\s+", " ", str(text or "").strip().lower())
