# engine/scoring/fispec_score.py

def calculate_fispec_score(nutrition_100g: dict) -> dict:
    """
    Deterministic FiSPEC scoring engine.
    Returns a score (0–10) and transparent engine notes.
    """

    score = 10.0
    notes = []

    notes.append("Base score initialized at 10.0")

    energy = nutrition_100g.get("energy_kcal")
    fat = nutrition_100g.get("fat")
    sugar = nutrition_100g.get("sugars")
    salt = nutrition_100g.get("salt")
    protein = nutrition_100g.get("protein")
    fiber = nutrition_100g.get("fiber")

    if energy is None:
        notes.append("Energy value not available: no penalty applied")
    elif energy > 350:
        score -= 2.0
        notes.append("High energy density (>350 kcal/100g): −2.0")

    if fat is None:
        notes.append("Fat value is not available: penalty applied")
        score -= 1.5
    elif fat > 15:
        score -= 2.0
        notes.append("High total fat (>15 g/100g): −2.0")

    if sugar is None:
        notes.append("Sugar value is not available: penalty applied")
        score -= 3
    elif sugar > 12:
        score -= 1.5
        notes.append("High sugar (>12 g/100g): −1.5")

    if salt is None:
        notes.append("Salt value is not available: penalty applied")
        score -= 2
    elif salt > 1.5:
        score -= 1.5
        notes.append("High salt (>1.5 g/100g): −1.5")
        
    if protein is None:
        notes.append("Protein data not available: no positive contribution considered")

    if fiber is None:
        notes.append("Fiber data not available: no positive contribution considered")

    score = max(0.0, round(score, 1))

    notes.append(f"Final engine FiSPEC score: {score}")

    return {
        "engine_fispec_score": score,
        "engine_notes": notes
    }
