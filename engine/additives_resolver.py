import csv
from pathlib import Path


# ---------- LOAD MASTER DATASET ----------

ADD_FILE = Path("data/additives_master.csv")

_ADDITIVES_BY_CODE = {}
_ADDITIVES_BY_CLASS = {}


def _load_additives():
    if not ADD_FILE.exists():
        return

    with open(ADD_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            code = row["code"].strip().upper()

            # normalize: remove leading E if present
            if code.startswith("E"):
                code = code[1:]

            cls = row["class"].strip()

            _ADDITIVES_BY_CODE[code] = {
                "code": code,
                "name": row["name"].strip(),
                "class": cls,
                "purpose": row["purpose"].strip()
            }

            # store generic fallback by class (first wins)
            if cls not in _ADDITIVES_BY_CLASS:
                _ADDITIVES_BY_CLASS[cls] = {
                    "name": cls,
                    "class": cls,
                    "purpose": f"Used as a {cls.lower()} in food products."
                }


_load_additives()


# ---------- PUBLIC RESOLVER ----------

def resolve_additives(detected_additives):
    """
    Input: output from parse_ingredients()
    Output: clean additive list for API response
    """

    resolved = []
    seen = set()

    for item in detected_additives:
        detected_as = item["detected_as"]
        raw = item["raw_text"]
        code = item.get("code")

        # ---------- CASE 1: CODE FOUND ----------
        if detected_as == "code" and code:
            data = _ADDITIVES_BY_CODE.get(code)

            if data:
                key = (data["code"], data["class"])
                if key in seen:
                    continue
                seen.add(key)

                resolved.append({
                    "code": data["code"],
                    "name": data["name"],
                    "class": data["class"],
                    "purpose": data["purpose"]
                })
            else:
                resolved.append({
                    "code": code,
                    "name": "Unknown additive",
                    "class": "Unknown",
                    "purpose": "Additive code declared but not found in reference dataset."
                })

        # ---------- CASE 2: CATEGORY ONLY ----------
        elif detected_as == "category":
            cls = raw.title()
            data = _ADDITIVES_BY_CLASS.get(cls)

            key = (None, cls)
            if key in seen:
                continue
            seen.add(key)

            if data:
                resolved.append({
                    "code": None,
                    "name": data["name"],
                    "class": data["class"],
                    "purpose": data["purpose"]
                })
            else:
                resolved.append({
                    "code": None,
                    "name": cls,
                    "class": cls,
                    "purpose": "Additive category declared without specific compound disclosure."
                })

        # ---------- CASE 3: NAME-BASED ONLY ----------
        elif detected_as == "name":
            resolved.append({
                "code": None,
                "name": raw.title(),
                "class": "Unspecified additive",
                "purpose": "Ingredient name suggests additive usage, but no official code disclosed."
            })

    return resolved
