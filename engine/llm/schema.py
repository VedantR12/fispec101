LLM_OUTPUT_SCHEMA = {
    "ratings": {
        "fispec_score": {
            "value": "number (0–10)",
            "basis": "string"
        },
        "indian_lifestyle_score": {
            "value": "number (0–10)",
            "basis": "string"
        }
    },

    "summary": {
        "one_line": "string"
    },

    "nutrition_breakdown": {
        "energy": {
            "value": "number | null",
            "unit": "kcal per 100g",
            "impact": "string"
        },
        "fats": {
            "value": "number | null",
            "unit": "g per 100g",
            "impact": "string"
        },
        "sugar": {
            "value": "number | null",
            "unit": "g per 100g",
            "impact": "string"
        },
        "salt": {
            "value": "number | null",
            "unit": "g per 100g",
            "impact": "string"
        },
        "protein": {
            "value": "number | null",
            "unit": "g per 100g",
            "impact": "string"
        },
        "fiber": {
            "value": "number | null",
            "unit": "g per 100g",
            "impact": "string"
        }
    },

    "additives_analysis": [
        {
            "name": "string",
            "code": "string | null",
            "why_used": "string",
            "disclosure": "Disclosed | Not disclosed | Inferred",
            "confidence": "High | Medium | Low",
            "general_note": "string"
        }
    ]
}
