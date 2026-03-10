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
        "one_line": "2-3 sentence explanation describing what the additive is, why it is used in food, and any health context"
    },

    "nutrition_breakdown": {
        "energy": {
            "value": "number | null",
            "unit": "kcal per 100g",
            "impact": "1-2 sentence explanation of the nutritional impact on health"
        },
        "fats": {
            "value": "number | null",
            "unit": "g per 100g",
            "impact": "1-2 sentence explanation of the nutritional impact on health"
        },
        "sugar": {
            "value": "number | null",
            "unit": "g per 100g",
            "impact": "1-2 sentence explanation of the nutritional impact on health"
        },
        "salt": {
            "value": "number | null",
            "unit": "g per 100g",
            "impact": "1-2 sentence explanation of the nutritional impact on health"
        },
        "protein": {
            "value": "number | null",
            "unit": "g per 100g",
            "impact": "1-2 sentence explanation of the nutritional impact on health"
        },
        "fiber": {
            "value": "number | null",
            "unit": "g per 100g",
            "impact": "1-2 sentence explanation of the nutritional impact on health"
        }
    },

    "additives_analysis": [
        {
            "name": "string",
            "code": "string | null",
            "why_used": "string",
            "disclosure": "Disclosed | Not disclosed | Inferred",
            "confidence": "High | Medium | Low",
            "general_note": "2-3 sentence explanation describing what the additive is, why it is used in food, and any health context"
        }
    ]
}
