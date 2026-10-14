"""
Data Preprocessing Pipeline: 
Cleans and standardizes raw text from Wikipedia and Wikidata APIs.
"""

import re
from typing import Iterable, List

UNWANTED_PREFIXES = (
    "list of ", "outline of ", "index of ", "category:", "portal:",
    "template:", "help:", "wikipedia:", "wikidata:", "file:", "talk:"
)

def clean_title(title: str) -> str:
    """Normalize whitespace, remove trailing spaces, and handle empty values."""
    if not isinstance(title, str) or not title.strip():
        return ""
    
    # Remove excessive whitespace
    cleaned = re.sub(r"\s+", " ", title).strip()
    return cleaned

def clean_titles(titles: Iterable[str], root_title: str = "", limit: int = 40) -> List[str]:
    """
    Data Science Preprocessing Step:
    - Removes duplicate entities.
    - Filters out self-references (root topic).
    - Removes structural/administrative pages (Lists, Indexes).
    - Removes purely numeric titles (like years '2024').
    """
    root_key = clean_title(root_title).casefold()
    seen = set()
    cleaned = []

    for raw_title in titles:
        title = clean_title(raw_title)
        key = title.casefold()

        # Filter empty, self-referencing, or duplicate titles
        if not title or key == root_key or key in seen:
            continue
            
        # Filter administrative namespaces and year-only titles
        if key.startswith(UNWANTED_PREFIXES) or re.match(r'^\d{1,4}$', key):
            continue

        seen.add(key)
        cleaned.append(title)
        
        # Cap the dataset size for performance and graph clarity
        if len(cleaned) >= limit:
            break

    return cleaned

def clean_summary(summary: str, max_length: int = 1500) -> str:
    """Standardizes summary text and limits length for UI readability."""
    if not isinstance(summary, str) or not summary.strip():
        return "No descriptive summary available for this concept in the current database."

    # Remove citations like [1], [2a]
    summary = re.sub(r"\[\d+[a-z]?\]", "", summary)
    
    # Normalize spaces
    summary = re.sub(r"\s+", " ", summary).strip()
    
    # Truncate gracefully without cutting off in the middle of a word
    if len(summary) > max_length:
        return summary[:max_length].rsplit(' ', 1)[0] + "..."
        
    return summary