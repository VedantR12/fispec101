# engine/scoring/category_guard.py

"""
Category-based normalization layer for FiSPEC.

Purpose:
- Prevent counter-intuitive scores (e.g., chips > paneer)
- Keep scores human-sensible without altering engine math
- Fully deterministic, transparent, and auditable

This layer NEVER increases scores beyond realistic category bounds.
"""

from typing import Tuple


# -------------------------
# CATEGORY DEFINITIONS
# -------------------------

CATEGORY_RULES = {
    "ultra_processed_snack": {
        "max": 6.5,
        "note": "Ultra-processed snack foods are capped due to high processing, fat, and salt."
    },
    "processed_snack": {
        "max": 7.0,
        "note": "Processed snacks have an upper cap due to moderate–high processing."
    },
    "sugary_beverage": {
        "max": 6.0,
        "note": "Sugary beverages are capped due to high sugar and low satiety."
    },
    "instant_food": {
        "max": 6.5,
        "note": "Instant foods are capped due to sodium and processing concerns."
    },
    "staple_food": {
        "min": 6.0,
        "note": "Staple foods are given a minimum floor due to dietary importance."
    },
    "whole_food": {
        "min": 6.5,
        "note": "Whole foods receive a minimum floor due to minimal processing."
    }
}


# -------------------------
# CATEGORY DETECTION
# -------------------------

def detect_category(product: dict) -> str:
    """
    Heuristic category detection using ingredients + additives.
    This is intentionally conservative.
    """

    ingredients = " ".join(product.get("ingredients", [])).lower()
    additives = product.get("additives", [])

    if any(x in ingredients for x in ["chips", "snack", "flavored", "fried"]):
        return "processed_snack"

    if len(additives) >= 5:
        return "ultra_processed_snack"

    if any(x in ingredients for x in ["cola", "soft drink", "soda"]):
        return "sugary_beverage"

    if any(x in ingredients for x in ["instant", "noodles", "cup"]):
        return "instant_food"

    if any(x in ingredients for x in ["rice", "dal", "wheat", "millet"]):
        return "staple_food"

    return "whole_food"


# -------------------------
# SCORE NORMALIZATION
# -------------------------

def apply_category_guard(
    score: float,
    product: dict
) -> Tuple[float, list[str]]:
    """
    Applies category-based bounds to the final FiSPEC score.

    Returns:
    - adjusted_score
    - guard_notes (list of applied rules)
    """

    notes = []
    category = detect_category(product)
    rules = CATEGORY_RULES.get(category)

    adjusted_score = score

    if not rules:
        return adjusted_score, notes

    if "max" in rules and adjusted_score > rules["max"]:
        adjusted_score = rules["max"]
        notes.append(
            f"Category guard applied ({category}): score capped at {rules['max']}"
        )

    if "min" in rules and adjusted_score < rules["min"]:
        adjusted_score = rules["min"]
        notes.append(
            f"Category guard applied ({category}): score raised to {rules['min']}"
        )

    return round(adjusted_score, 1), notes
