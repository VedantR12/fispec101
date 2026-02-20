def map_nutrition_for_engine(nutrition_100g: dict) -> dict:
    """
    Normalize nutrition keys so the deterministic engine
    ALWAYS receives values if they exist.
    """

    if not nutrition_100g:
        return {}

    def first_available(*keys):
        for k in keys:
            if k in nutrition_100g and nutrition_100g[k] is not None:
                return nutrition_100g[k]
        return None

    return {
        "energy_kcal": first_available(
            "energy-kcal_100g",
            "energy_kcal_100g",
            "energy_100g"
        ),

        "fat": first_available(
            "fat_100g",
            "total_fat_100g"
        ),

        "sugars": first_available(
            "sugars_100g",
            "sugar_100g"
        ),

        "salt": first_available(
            "salt_100g",
            "sodium_100g"
        ),

        "protein": first_available(
            "proteins_100g",
            "protein_100g"
        ),

        "fiber": first_available(
            "fiber_100g",
            "fibres_100g"
        ),
    }
