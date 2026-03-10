from datetime import datetime
from engine.db.supabase_client import supabase


def save_user_history(uid: str, product_name: str, barcode: str | None, score: float):

    try:
        insert_response = supabase.table("user_history").insert({
            "user_uid": uid,
            "product_name": product_name,
            "barcode": barcode,
            "final_fispec_score": score,
            "searched_at": datetime.utcnow().isoformat()
        }).execute()
    except Exception as e:
        print("Supabase history error:", e)

    # 2️⃣ Fetch all user history ordered latest first
    response = (
        supabase
        .table("user_history")
        .select("id")
        .eq("user_uid", uid)
        .order("searched_at", desc=True)
        .execute()
    )

    history = response.data or []

    # 3️⃣ If more than 50 rows → delete older ones
    if len(history) > 50:
        # Keep first 50 (latest)
        ids_to_delete = [row["id"] for row in history[50:]]

        for row_id in ids_to_delete:
            supabase.table("user_history") \
                .delete() \
                .eq("id", row_id) \
                .execute()