from fastapi import FastAPI, Query, Depends
from engine.auth.dependencies import get_current_user
from fastapi.middleware.cors import CORSMiddleware
from engine.history.history_writer import save_user_history
from engine.history.history_reader import get_user_history
from engine.retrieval import find_product
from engine.llm.runner import run_llm_analysis
from engine.scoring.fispec_score import calculate_fispec_score
from engine.scoring.fispec_fusion import fuse_fispec_scores
from engine.scoring.nutrition_mapper import map_nutrition_for_engine
from engine.scoring.category_guard import apply_category_guard

app = FastAPI()

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

    # 1️⃣ LLM
    llm_result = run_llm_analysis(product)
    llm_score = llm_result["llm_fispec_score"]

    # 2️⃣ Engine
    mapped_nutrition = map_nutrition_for_engine(
        product.get("nutrition_100g", {})
    )

    engine_result = calculate_fispec_score(mapped_nutrition)
    engine_score = engine_result["engine_fispec_score"]
    engine_notes = engine_result.get("engine_notes") or []

    # 3️⃣ Fusion (FIXED)
    final_score = fuse_fispec_scores(engine_score)

    # 4️⃣ Category guard
    guarded_score, guard_notes = apply_category_guard(
        final_score,
        product
    )

    engine_notes.extend(guard_notes)

    # 5️⃣ Save history
    save_user_history(
        uid=user["uid"],
        product_name=product.get("product_name"),
        barcode=product.get("code"),
        score=guarded_score
    )

    # 6️⃣ Product details
    product_details = {
        "product_name": product.get("product_name"),
        "brand": product.get("brands"),
        "barcode": product.get("code"),
        "ingredients_raw": product.get("ingredients_text"),
        "categories": product.get("categories"),
        "quantity": product.get("quantity")
    }

    return {
        "final_fispec_score": guarded_score,
        "engine_fispec_score": engine_score,
        "llm_fispec_score": llm_score,
        "engine_notes": engine_notes,
        "product_details": product_details,
        "analysis": llm_result["analysis"]
    }


@app.get("/history")
def read_history(user: dict = Depends(get_current_user)):
    history = get_user_history(user["uid"])
    return {"history": history}