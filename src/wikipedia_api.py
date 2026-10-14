"""Unstructured Data Extraction: Wikipedia MediaWiki REST API."""

import requests
from urllib.parse import quote
from .data_cleaner import clean_summary, clean_title, clean_titles

API_URL = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "ConceptGraphProfessional/8.0"}

class WikipediaAPIError(Exception):
    """Custom exception for Wikipedia extraction failures."""
    pass

def _get(params: dict) -> dict:
    """Base REST request executor with error handling."""
    request_params = {"format": "json", "origin": "*", **params}
    try:
        response = requests.get(API_URL, params=request_params, headers=HEADERS, timeout=15)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        raise WikipediaAPIError("Network Error: Could not connect to Wikipedia API.") from exc
        
    if "error" in data:
        raise WikipediaAPIError(f"API Error: {data['error'].get('info', 'Unknown error')}")
        
    return data

def search_article(topic: str) -> dict:
    """Finds the canonical Wikipedia article and extracts its introductory summary."""
    topic = clean_title(topic)
    if not topic: 
        raise WikipediaAPIError("Invalid search query.")

    search_data = _get({"action": "query", "list": "search", "srsearch": topic, "srlimit": 3})
    results = search_data.get("query", {}).get("search", [])
    
    if not results:
        raise WikipediaAPIError(f"Zero results found for '{topic}'. Try broadening your search.")

    match = next((item for item in results if item.get("title", "").casefold() == topic.casefold()), results[0])
    requested_title = match["title"]

    article_data = _get({
        "action": "query", "prop": "extracts|info", "exintro": 1, 
        "explaintext": 1, "inprop": "url", "redirects": 1, "titles": requested_title
    })
    
    pages = article_data.get("query", {}).get("pages", {})
    page = next(iter(pages.values()), None)

    if not page or "missing" in page:
        raise WikipediaAPIError("Critical Error: Article index missing.")

    title = clean_title(page.get("title", requested_title))
    url = page.get("fullurl", f"https://en.wikipedia.org/wiki/{quote(title.replace(' ', '_'))}")

    return {
        "title": title, 
        "summary": clean_summary(page.get("extract", "")),
        "url": url, 
        "source": "Wikipedia"
    }

def get_article_links(title: str, limit: int = 60) -> list[str]:
    """Extracts outgoing hyperlinks (edges) from the root article."""
    data = _get({
        "action": "query", "prop": "links", "titles": title, 
        "plnamespace": 0, "pllimit": "max", "redirects": 1
    })
    
    pages = data.get("query", {}).get("pages", {})
    page = next(iter(pages.values()), {})
    
    raw_links = [item.get("title", "") for item in page.get("links", [])]
    return clean_titles(raw_links, root_title=title, limit=limit)

def get_article_details(titles: list[str]) -> dict[str, dict]:
    """Batch-fetches summaries and URLs for a list of related concepts."""
    result = {}
    for start in range(0, len(titles), 20):
        batch = titles[start:start + 20]
        if not batch: 
            continue

        data = _get({
            "action": "query", "prop": "extracts|info", "exintro": 1, 
            "explaintext": 1, "inprop": "url", "redirects": 1, "titles": "|".join(batch)
        })
        
        pages = data.get("query", {}).get("pages", {})

        for page in pages.values():
            if "missing" in page: 
                continue
                
            actual_title = clean_title(page.get("title", ""))
            if not actual_title: 
                continue

            result[actual_title] = {
                "summary": clean_summary(page.get("extract", "")),
                "url": page.get("fullurl", f"https://en.wikipedia.org/wiki/{quote(actual_title.replace(' ', '_'))}")
            }
            
    return result