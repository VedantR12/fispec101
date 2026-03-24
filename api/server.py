from fastapi import FastAPI, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from engine.auth.dependencies import get_current_user
from engine.history.history_writer import save_user_history
from engine.history.history_reader import get_user_history
from engine.retrieval import find_product
from engine.llm.runner import run_llm_analysis
from engine.scoring.fispec_score import calculate_fispec_score
from engine.scoring.nutrition_mapper import map_nutrition_for_engine
from engine.db.supabase_client import supabase
from engine.db.analysis_store import get_analysis, save_analysis
from fastapi.responses import JSONResponse


app = FastAPI()

#health
@app.api_route("/health", methods=["GET", "HEAD"])
def health():
    return JSONResponse({"status": "ok"})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

#home
@app.get("/")
def root():
    return {"status": "FiSpec backend is running \n visit: https://fispec.vercel.app"}

#search
@app.get("/search")
def search_product(
    q: str = Query(...),
    user: dict = Depends(get_current_user)
):
    product = find_product(q)

    if product is None:
        return {"error": "Product not found"}

    
    barcode = product.get("code")

    cached = get_analysis(barcode)

    if cached:

        llm_result = {
            "analysis": cached["analysis_json"],
            "llm_fispec_score": cached["llm_fispec_score"]
        }

    else:

        llm_result = run_llm_analysis(product)

        save_analysis(
            barcode,
            llm_result["analysis"],
            llm_result["llm_fispec_score"]
        )
         
    llm_score = llm_result["llm_fispec_score"]

    mapped_nutrition = map_nutrition_for_engine(
        product.get("nutrition_100g", {})
    )

    engine_result = calculate_fispec_score(product, mapped_nutrition)
    engine_score = engine_result["engine_fispec_score"]
    engine_notes = engine_result.get("engine_notes") or []

  
    final_score = engine_score
   

    #save_history
    try:
        save_user_history(
            uid=user["uid"],
            product_name=product.get("product_name"),
            barcode=product.get("code"),
            score=final_score
        )
    except Exception as e:
        print("History write failed:", e)

    #response
    return {
        "final_fispec_score": final_score,
        "engine_fispec_score": engine_score,
        "llm_fispec_score": llm_score,
        "engine_notes": engine_notes,
        "product_details": {
            "product_name": product.get("product_name"),
            "brand": product.get("brands"),
            "barcode": product.get("code"),
            "categories": product.get("categories"),
            "image_url": product.get("image_url"),
            "image_small_url": product.get("image_small_url")
        },
        "analysis": llm_result["analysis"]
    }

#suggestions
@app.get("/suggest")
def suggest_products(q: str = Query(...)):

    response = (
        supabase
        .table("products")
        .select("code, product_name, brands, image_small_url")
        .ilike("product_name", f"%{q}%")
        .limit(8)
        .execute()
    )

    suggestions = []

    if response.data:
        for row in response.data:
            suggestions.append({
                "barcode": row["code"],
                "product_name": row["product_name"],
                "brand": row["brands"],
                "image": row["image_small_url"]
            })

    return {"suggestions": suggestions}

#search results page
@app.get("/search-products")
def search_products(q: str = Query(...)):

    # Detect if query is barcode
    if q.isdigit():

        response = (
            supabase
            .table("products")
            .select("code, product_name, brands, categories, image_small_url")
            .eq("code", q)
            .limit(1)
            .execute()
        )

    else:

        response = (
            supabase
            .table("products")
            .select("code, product_name, brands, categories, image_small_url")
            .ilike("product_name", f"%{q}%")
            .limit(20)
            .execute()
        )

    results = []

    if response.data:
        for row in response.data:
            results.append({
                "barcode": row["code"],
                "product_name": row["product_name"],
                "brand": row["brands"],
                "categories": row["categories"],
                "image": row.get("image_small_url")
            })

    return {"results": results}

#get_hisotry
@app.get("/history")
def read_history(user: dict = Depends(get_current_user)):
    history = get_user_history(user["uid"])
    return {"history": history}