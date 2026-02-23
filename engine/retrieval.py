from engine.db.supabase_client import supabase
from engine.ingredients import parse_ingredients
from engine.additives_resolver import resolve_additives


def find_product(query: str):
    if not query:
        return None

    query = str(query).strip()
    is_numeric = query.isdigit()

    # 1️⃣ Barcode search (priority)
    if is_numeric:
        response = (
            supabase
            .table("products")
            .select("*")
            .eq("code", query)
            .limit(1)
            .execute()
        )

        if response.data:
            return build_product_result(response.data[0])

    # 2️⃣ Name search
    response = (
        supabase
        .table("products")
        .select("*")
        .ilike("product_name", f"%{query}%")
        .limit(1)
        .execute()
    )

    if response.data:
        return build_product_result(response.data[0])

    return None


def build_product_result(product: dict):
    parsed = parse_ingredients(product.get("ingredients_text"))

    return {
        "product_name": product.get("product_name"),
        "brands": product.get("brands"),
        "categories": product.get("categories"),
        "code": product.get("code"),
        "ingredients": parsed["ingredients"],
        "additives": resolve_additives(parsed["additives"]),
        "nutrition_100g": {
            "energy_100g": product.get("energy_kcal_100g"),
            "energy-kcal_100g": product.get("energy_kcal_100g"),
            "fat_100g": product.get("fat_100g"),
            "saturated-fat_100g": product.get("saturated_fat_100g"),
            "trans-fat_100g": product.get("trans_fat_100g"),
            "carbohydrates_100g": product.get("carbohydrates_100g"),
            "sugars_100g": product.get("sugars_100g"),
            "added-sugars_100g": product.get("added_sugars_100g"),
            "proteins_100g": product.get("proteins_100g"),
            "fiber_100g": product.get("fiber_100g"),
            "salt_100g": product.get("salt_100g"),
            "sodium_100g": product.get("sodium_100g"),
        }
    }