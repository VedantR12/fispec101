import pandas as pd

# Columns we care about (names EXACTLY as in OpenFoodFacts)
NUTRITION_COLUMNS = [
    "energy_100g",
    "energy-kcal_100g",
    "fat_100g",
    "saturated-fat_100g",
    "trans-fat_100g",
    "carbohydrates_100g",
    "sugars_100g",
    "added-sugars_100g",
    "proteins_100g",
    "fiber_100g",
    "salt_100g",
    "sodium_100g"
]


def extract_nutrition(product_row: pd.Series) -> dict:
    """
    Extract nutrition values EXACTLY as present in OpenFoodFacts.
    - Keeps column names unchanged
    - Converts NaN → None
    - Never guesses or derives values
    """

    nutrition = {}

    for col in NUTRITION_COLUMNS:
        if col in product_row:
            value = product_row.get(col)

            if value is None or (isinstance(value, float) and pd.isna(value)):
                nutrition[col] = None
            else:
                nutrition[col] = value

    return nutrition
