import pandas as pd
from engine.ingredients import parse_ingredients
from engine.additives_resolver import resolve_additives
from engine.nutrition import extract_nutrition

# 🔹 Global dataframe cache
df = None


def load_data():
    global df
    if df is None:
        print("Loading CSV data into memory...")
        df = pd.read_csv(
            "data/foodfacts.csv",
            sep="\t",
            engine="python",
            on_bad_lines="skip"
        )
        df["code"] = df["code"].astype(str)
        print("CSV loaded successfully.")


def find_product(query: str):
    if not query:
        return None

    # 🔹 Ensure CSV is loaded
    if df is None:
        load_data()

    query = str(query).strip()
    query_lower = query.lower()
    is_numeric = query.isdigit()

    # 🔹 1️⃣ BARCODE MATCH (PRIORITY)
    if is_numeric:
        barcode_matches = df[
            (df["code"] == query) |
            (df["code"].str.lstrip("0") == query.lstrip("0"))
        ]
        if not barcode_matches.empty:
            product = barcode_matches.iloc[0]
            return build_product_result(product)

    # 🔹 2️⃣ NAME MATCH
    product_series = df["product_name"].astype(str).str.lower()
    alt = query_lower[:-1] if query_lower.endswith("s") else query_lower + "s"

    name_matches = df[
        product_series.str.contains(query_lower, na=False) |
        product_series.str.contains(alt, na=False)
    ]

    if name_matches.empty:
        return None

    product = name_matches.iloc[0]
    return build_product_result(product)


def build_product_result(product):
    parsed = parse_ingredients(product.get("ingredients_text"))

    result = {
        "product_name": product.get("product_name"),
        "brands": product.get("brands"),
        "categories": product.get("categories"),
        "code": product.get("code"),
        "ingredients": parsed["ingredients"],
        "additives": resolve_additives(parsed["additives"]),
        "nutrition_100g": {
            "energy_100g": product.get("energy_100g"),
            "energy-kcal_100g": product.get("energy-kcal_100g"),
            "fat_100g": product.get("fat_100g"),
            "saturated-fat_100g": product.get("saturated-fat_100g"),
            "trans-fat_100g": product.get("trans-fat_100g"),
            "carbohydrates_100g": product.get("carbohydrates_100g"),
            "sugars_100g": product.get("sugars_100g"),
            "added-sugars_100g": product.get("added-sugars_100g"),
            "proteins_100g": product.get("proteins_100g"),
            "fiber_100g": product.get("fiber_100g"),
            "salt_100g": product.get("salt_100g"),
            "sodium_100g": product.get("sodium_100g"),
        }
    }

    # 🔹 Clean NaN values
    for section, values in result.items():
        if isinstance(values, dict):
            for k, v in values.items():
                if isinstance(v, float) and pd.isna(v):
                    values[k] = None

    return result