from engine.db.supabase_client import supabase


def get_user_history(uid: str):
    response = (
        supabase
        .table("user_history")
        .select("*")
        .eq("user_uid", uid)
        .order("searched_at", desc=True)
        .limit(10)
        .execute()
    )

    return response.data or []