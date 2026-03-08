from engine.db.supabase_client import supabase


def get_user_history(uid: str):

    response = (
        supabase
        .table("user_history")
        .select("*")
        .eq("user_uid", uid)
        .order("searched_at", desc=True)
        .limit(50)
        .execute()
    )

    results = []

    if response.data:

        for row in response.data:

            barcode = row.get("barcode")

            product_response = (
                supabase
                .table("products")
                .select("product_name, brands, image_small_url")
                .eq("code", barcode)
                .limit(1)
                .execute()
            )

            product = {}

            if product_response.data:
                product = product_response.data[0]

            results.append({
                "barcode": barcode,
                "score": row.get("final_fispec_score"),
                "product_name": product.get("product_name"),
                "brand": product.get("brands"),
                "image": product.get("image_small_url")
            })

    return results