def is_beverage(product: dict) -> bool:
    """
    Detect if a product belongs to beverage category
    """

    categories = (product.get("categories") or "").lower()

    beverage_keywords = [
        "beverage",
        "drink",
        "soda",
        "juice",
        "energy drink",
        "soft drink"
    ]

    return any(keyword in categories for keyword in beverage_keywords)


def beverage_sugar_penalty(sugar):
    """
    Stronger sugar penalty for beverages
    """

    if sugar is None:
        return 0

    if sugar >= 10:
        return 4.0
    elif sugar >= 8:
        return 3.0
    elif sugar >= 5:
        return 2.0
    elif sugar >= 2:
        return 1.0

    return 0


def calculate_fispec_score(product: dict, nutrition_100g: dict) -> dict:

    score = 10.0
    notes = []

    notes.append("Base score initialized at 10.0")

    energy = nutrition_100g.get("energy_kcal")
    fat = nutrition_100g.get("fat")
    sugar = nutrition_100g.get("sugars")
    salt = nutrition_100g.get("salt")
    protein = nutrition_100g.get("protein")
    fiber = nutrition_100g.get("fiber")

    # ENERGY
    if energy is None:
        notes.append("Energy value not available")
    elif energy > 350:
        score -= 2.0
        notes.append("High energy density (>350 kcal/100g): −2.0")

    # FAT
    if fat is None:
        score -= 1.5
        notes.append("Fat value missing: −1.5")
    elif fat > 30:
        score -= 5
        notes.append("Very high fat (>30 g/100g): −5.0")
    elif fat > 20:
        score -= 3
        notes.append("High fat (>20 g/100g): −3.0")
    elif fat > 15:
        score -= 2
        notes.append("Moderately high fat (>15 g/100g): −2.0")

    # SUGAR
    if sugar is None:
        score -= 3
        notes.append("Sugar value missing: −3.0")
    elif sugar > 20:
        score -= 5
        notes.append("Extremely high sugar (>20 g/100g): −5.0")
    elif sugar > 15:
        score -= 3
        notes.append("Very high sugar (>15 g/100g): −3.0")
    elif sugar > 10:
        score -= 2.5
        notes.append("High sugar (>10 g/100g): −2.5")

    # SALT
    if salt is None:
        score -= 2
        notes.append("Salt value missing: −2.0")
    elif salt > 3:
        score -= 3
        notes.append("Extremely high salt (>3 g/100g): −3.0")
    elif salt > 1.5:
        score -= 1.5
        notes.append("High salt (>1.5 g/100g): −1.5")

    # POSITIVE NUTRITION BONUS

    # Fiber bonus
    if fiber is not None:
        if fiber >= 8:
            score += 2
            notes.append("High fiber bonus (≥8 g/100g): +2.0")
        elif fiber >= 5:
            score += 1
            notes.append("Moderate fiber bonus (≥5 g/100g): +1.0")

    # Protein bonus
    if protein is not None:
        if protein >= 15:
            score += 2
            notes.append("High protein bonus (≥15 g/100g): +2.0")
        elif protein >= 8:
            score += 1
            notes.append("Moderate protein bonus (≥8 g/100g): +1.0")

    # BEVERAGE SUGAR RULE
    if is_beverage(product):

        penalty = beverage_sugar_penalty(sugar)

        if penalty > 0:
            score -= penalty
            notes.append(
                f"Beverage sugar penalty applied ({sugar} g/100g): −{penalty}"
            )

        if sugar is not None and sugar >= 10:
            score = min(score, 4)
            notes.append("Sugary beverage cap applied: score limited to 4")

    # FINAL CLAMP
    score = round(score, 1)

    score = min(score, 10.0)
    score = max(score, 0.0)

    notes.append(f"Final engine FiSPEC score: {score}")

    return {
        "engine_fispec_score": score,
        "engine_notes": notes
    }