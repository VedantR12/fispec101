# engine/cache/llm_cache.py

import json
import hashlib
from pathlib import Path
from typing import Optional

CACHE_DIR = Path("engine/cache/llm")


def _stable_product_hash(product_data: dict) -> str:
    """
    Generates a stable hash for a product based on
    fields that materially affect LLM reasoning.
    """

    fingerprint = {
        "product_name": product_data.get("product_name"),
        "brand": product_data.get("brands"),
        "ingredients": sorted(product_data.get("ingredients", [])),
        "nutrition_100g": product_data.get("nutrition_100g", {})
    }

    raw = json.dumps(fingerprint, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def load_llm_cache(product_data: dict) -> Optional[dict]:
    """
    Returns cached LLM result if exists, else None.
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    product_hash = _stable_product_hash(product_data)
    cache_file = CACHE_DIR / f"{product_hash}.json"

    if not cache_file.exists():
        return None

    with open(cache_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_llm_cache(product_data: dict, llm_result: dict) -> None:
    """
    Saves LLM result to disk cache.
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    product_hash = _stable_product_hash(product_data)
    cache_file = CACHE_DIR / f"{product_hash}.json"

    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(llm_result, f, indent=2, ensure_ascii=False)
