from datetime import datetime, timedelta
from engine.db.supabase_client import supabase


def save_user_history(uid: str, product_name: str, barcode: str | None, score: float):

    # 1️⃣ Delete entries older than 10 days
    ten_days_ago = (datetime.utcnow() - timedelta(days=10)).isoformat()

    supabase.table("user_history") \
        .delete() \
        .eq("user_uid", uid) \
        .lt("searched_at", ten_days_ago) \
        .execute()

    # 2️⃣ Fetch existing history (latest first)
    response = supabase.table("user_history") \
        .select("*") \
        .eq("user_uid", uid) \
        .order("searched_at", desc=True) \
        .execute()

    history = response.data or []

    # 3️⃣ Keep only last 10 entries
    if len(history) >= 10:
        oldest = history[-1]
        supabase.table("user_history") \
            .delete() \
            .eq("id", oldest["id"]) \
            .execute()

    # 4️⃣ Insert new entry
    supabase.table("user_history").insert({
        "user_uid": uid,
        "product_name": product_name,
        "barcode": barcode,
        "final_fispec_score": score,
        "searched_at": datetime.utcnow().isoformat()
    }).execute()
