from engine.db.supabase_client import supabase


def get_analysis(barcode: str):

    response = (
        supabase
        .table("product_analysis")
        .select("*")
        .eq("barcode", barcode)
        .limit(1)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None


def save_analysis(barcode: str, analysis: dict, llm_score: float):

    supabase.table("product_analysis").insert({
        "barcode": barcode,
        "analysis_json": analysis,
        "llm_fispec_score": llm_score
    }).execute()