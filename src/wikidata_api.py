"""Structured Data Extraction: Wikidata API for Knowledge Graphs."""

import requests
from urllib.parse import quote
from .data_cleaner import clean_summary, clean_title

API_URL = "https://www.wikidata.org/w/api.php"
HEADERS = {"User-Agent": "ConceptGraphProfessional/8.0"}

class WikidataAPIError(Exception):
    """Custom exception for Wikidata API failures."""
    pass

def _get(params: dict) -> dict:
    request_params = {"format": "json", "origin": "*", **params}
    try:
        response = requests.get(API_URL, params=request_params, headers=HEADERS, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise WikidataAPIError("Network Error: Could not connect to Wikidata.") from exc

def search_article(topic: str) -> dict:
    """Find a Wikidata entity (Q-ID) based on search phrase."""
    topic = clean_title(topic)
    if not topic: 
        raise WikidataAPIError("Invalid query.")

    data = _get({"action": "wbsearchentities", "search": topic, "language": "en", "limit": 1})
    results = data.get("search", [])
    
    if not results:
        raise WikidataAPIError(f"No structured entity found for '{topic}'. Try Wikipedia mode.")

    entity = results[0]
    return {
        "title": entity.get("label", topic), 
        "id": entity.get("id"),
        "summary": clean_summary(entity.get("description", "")),
        "url": entity.get("concepturi", f"https://www.wikidata.org/wiki/{entity.get('id')}"),
        "source": "Wikidata"
    }

def get_article_links(entity_id: str, limit: int = 60) -> list[str]:
    """Extracts structurally validated claims (relationships) connected to this entity."""
    data = _get({"action": "wbgetentities", "ids": entity_id, "languages": "en", "props": "claims"})
    claims = data.get("entities", {}).get(entity_id, {}).get("claims", {})

    related_ids = []
    for prop, claim_list in claims.items():
        for claim in claim_list:
            mainsnak = claim.get("mainsnak", {})
            if mainsnak.get("datatype") == "wikibase-item" and "datavalue" in mainsnak:
                qid = mainsnak["datavalue"]["value"]["id"]
                if qid not in related_ids:
                    related_ids.append(qid)
                    
            if len(related_ids) >= limit: 
                break
        if len(related_ids) >= limit: 
            break
            
    return related_ids

def get_article_details(q_ids: list[str]) -> dict[str, dict]:
    """Batch-fetches labels and descriptions for related Wikidata IDs."""
    result = {}
    for start in range(0, len(q_ids), 40):
        batch = q_ids[start:start + 40]
        if not batch: 
            continue
        
        data = _get({
            "action": "wbgetentities", "ids": "|".join(batch), 
            "languages": "en", "props": "labels|descriptions|info"
        })
        entities = data.get("entities", {})

        for qid, ent in entities.items():
            label = ent.get("labels", {}).get("en", {}).get("value")
            if not label: 
                continue
                
            desc = ent.get("descriptions", {}).get("en", {}).get("value", "")
            result[label] = {
                "summary": clean_summary(desc),
                "url": f"https://www.wikidata.org/wiki/{qid}"
            }
            
    return result