from fastapi import FastAPI, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from engine.auth.dependencies import get_current_user
from engine.history.history_writer import save_user_history
from engine.history.history_reader import get_user_history
from engine.retrieval import find_product
from engine.llm.runner import run_llm_analysis
from engine.scoring.fispec_score import calculate_fispec_score
from engine.scoring.nutrition_mapper import map_nutrition_for_engine

app = FastAPI()


# CORS (tighten later in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "FiSpec backend is running"}


@app.get("/search")
def search_product(
    q: str = Query(...),
    user: dict = Depends(get_current_user)
):
    product = find_product(q)

    if product is None:
        return {"error": "Product not found"}

    # LLM analysis
    llm_result = run_llm_analysis(product)
    llm_score = llm_result["llm_fispec_score"]

    # Engine scoring
    mapped_nutrition = map_nutrition_for_engine(
        product.get("nutrition_100g", {})
    )

    engine_result = calculate_fispec_score(mapped_nutrition)
    engine_score = engine_result["engine_fispec_score"]
    engine_notes = engine_result.get("engine_notes") or []

    # Final score (your logic here)
    final_score = engine_score
   

    # Save history
    save_user_history(
        uid=user["uid"],
        product_name=product.get("product_name"),
        barcode=product.get("code"),
        score=final_score
    )

    # Response
    return {
        "final_fispec_score": final_score,
        "engine_fispec_score": engine_score,
        "llm_fispec_score": llm_score,
        "engine_notes": engine_notes,
        "product_details": {
            "product_name": product.get("product_name"),
            "brand": product.get("brands"),
            "barcode": product.get("code"),
            "categories": product.get("categories")
        },
        "analysis": llm_result["analysis"]
    }


@app.get("/history")
def read_history(user: dict = Depends(get_current_user)):
    history = get_user_history(user["uid"])
    return {"history": history}