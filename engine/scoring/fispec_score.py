def calculate_fispec_score(product: dict, nutrition_100g: dict) -> dict:

    notes = []
    score = 10.0

    energy = nutrition_100g.get("energy_kcal")
    fat = nutrition_100g.get("fat")
    sugar = nutrition_100g.get("sugars")
    salt = nutrition_100g.get("salt")
    protein = nutrition_100g.get("protein")
    fiber = nutrition_100g.get("fiber")

    values = {
        "energy": energy,
        "fat": fat,
        "sugar": sugar,
        "salt": salt,
        "protein": protein,
        "fiber": fiber
    }

    # -------------------------
    # DATA AVAILABILITY CHECK
    # -------------------------

    missing = [k for k, v in values.items() if v is None]

    if len(missing) > 2:

        notes.append(
            f"Insufficient nutritional data. Missing values: {', '.join(missing)}"
        )

        notes.append(
            "More than two essential nutritional values are unavailable."
        )

        notes.append(
            "FiSpec score cannot be calculated reliably."
        )

        return {
            "engine_fispec_score": "NA",
            "engine_notes": notes
        }

    if len(missing) > 0:

        notes.append(
            f"Score calculated using available data. Missing values: {', '.join(missing)}"
        )

    notes.append("Base score initialized at 10.0")

    risk = 0
    benefit = 0

    # -------------------------
    # SUGAR RISK
    # -------------------------

    if sugar is not None:
        sugar_risk = sugar / 25
        risk += sugar_risk
        notes.append(f"Sugar influence: +{round(sugar_risk,2)} risk units")

    # -------------------------
    # FAT RISK
    # -------------------------

    if fat is not None:
        fat_risk = fat / 30
        risk += fat_risk
        notes.append(f"Fat influence: +{round(fat_risk,2)} risk units")

    # -------------------------
    # SALT RISK
    # -------------------------

    if salt is not None:
        salt_risk = salt / 2
        risk += salt_risk
        notes.append(f"Salt influence: +{round(salt_risk,2)} risk units")

    # -------------------------
    # ENERGY RISK
    # -------------------------

    if energy is not None:
        energy_risk = energy / 500
        risk += energy_risk
        notes.append(f"Energy density influence: +{round(energy_risk,2)} risk units")

    # -------------------------
    # FIBER BENEFIT
    # -------------------------

    if fiber is not None:

        if fiber == 0:
            fiber_bonus = -1 / 8
            notes.append("No fiber present: small penalty applied")
        else:
            fiber_bonus = fiber / 8

        benefit += fiber_bonus
        notes.append(f"Fiber contribution: {round(fiber_bonus,2)} benefit units")

    # -------------------------
    # PROTEIN BENEFIT
    # -------------------------

    if protein is not None:

        if protein == 0:
            protein_bonus = -1 / 15
            notes.append("No protein present: small penalty applied")
        else:
            protein_bonus = protein / 15

        benefit += protein_bonus
        notes.append(f"Protein contribution: {round(protein_bonus,2)} benefit units")

    # -------------------------
    # FINAL SCORE
    # -------------------------

    score = 10 - (risk * 2) + benefit

    score = round(score, 1)

    score = min(score, 10.0)
    score = max(score, 1.0)

    notes.append(f"Total risk influence: {round(risk,2)}")
    notes.append(f"Total benefit influence: {round(benefit,2)}")
    notes.append(f"Final engine FiSPEC score: {score}")

    return {
        "engine_fispec_score": score,
        "engine_notes": notes
    }