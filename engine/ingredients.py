import re
import csv
from pathlib import Path

# ---------- LOAD ADDITIVE NAMES FROM DATASET ----------

ADD_FILE = Path("data/additives_master.csv")

ADDITIVE_NAMES = set()
ADDITIVE_NAME_TO_CODE = {}

if ADD_FILE.exists():
    with open(ADD_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"].strip().lower()
            code = row["code"].strip().upper()

            if name:
                ADDITIVE_NAMES.add(name)
                ADDITIVE_NAME_TO_CODE[name] = code


# ---------- MAIN PARSER ----------

def parse_ingredients(ingredients_text):
    """
    Parses ingredient text and detects additive signals using DATASET ONLY.
    """

    if not ingredients_text or not isinstance(ingredients_text, str):
        return {"ingredients": [], "additives": []}

    text = ingredients_text.lower()

    # ---------- INGREDIENT LIST ----------
    clean_text = re.sub(r"\([^)]*\)", "", text)

    ingredients = [
        i.strip()
        for i in re.split(r"[,\.;]", clean_text)
        if i.strip()
    ]

    additives = []
    seen = set()

    # ---------- 1️⃣ CODE-BASED DETECTION ----------
    code_matches = re.findall(r"\b(e\d{3,4}|ins\s?\d{3,4})\b", text)

    numeric_matches = re.findall(
        r"(?:raising agents?|emulsifiers?|stabilizers?|antioxidants?|colou?rs?)\s*\[?\s*(\d{3,4}[a-z]?)",
        text
    )

    for raw in code_matches + numeric_matches:
        code = raw.upper().replace(" ", "")
        code = code.replace("INS", "").replace("E", "").strip()

        if not code or code in seen:
            continue

        seen.add(code)

        additives.append({
            "code": code,
            "raw_text": raw,
            "detected_as": "code",
            "confidence": "High"
        })

    # ---------- 2️⃣ NAME-BASED DETECTION (DATASET-ONLY) ----------
    for ingredient in ingredients:
        for name in ADDITIVE_NAMES:
           tokens = re.findall(r"[a-z]+", ingredient)
           ingredient_text = " ".join(tokens)
           
           if f" {name} " in f" {ingredient_text} ":

                code = ADDITIVE_NAME_TO_CODE.get(name)

                key = f"NAME::{code or name}"
                if key in seen:
                    continue
                seen.add(key)

                additives.append({
                    "code": code,
                    "raw_text": name,
                    "detected_as": "name",
                    "confidence": "Medium"
                })
                def normalize_word(word):
                    return word.replace("nn", "n")


    # ---------- CATEGORY-ONLY DISCLOSURE (LOW CONFIDENCE) ----------
        CATEGORY_KEYWORDS = [
    "raising agent",
    "raising agents",
    "emulsifier",
    "emulsifiers",
    "stabilizing agent",
    "stabilizing agents",
    "antioxidant",
    "antioxidants",
    "food colour",
    "food colours",
    "flavouring substance",
    "flavouring substances"
]

    for ingredient in ingredients:
            for category in CATEGORY_KEYWORDS:
                if category not in ingredient:
                    continue   # ✅ ensures k is only used when defined

                key = f"CATEGORY::{category}"

                if key in seen:
                    continue

                seen.add(key)

                additives.append({
                "code": None,
                "raw_text": category,
                "detected_as": "category",
                "confidence": "Low"
                })


    return {
        "ingredients": ingredients,
        "additives": additives
    }
