import json
from engine.llm.gemini_client import run_gemini
from engine.llm.prompt_builder import build_llm_prompt
from engine.llm.models import LLMOutput


def run_llm_analysis(product_data: dict) -> dict:
    prompt = build_llm_prompt(product_data)
    raw = run_gemini(prompt)

    try:
        parsed = json.loads(raw)

        # Validate full structure
        validated = LLMOutput(**parsed)

        # Extract FiSPEC score ONLY for internal use
        llm_fispec_score = (
            validated.ratings.fispec_score.value
            if validated.ratings and validated.ratings.fispec_score
            else None
        )
        
        return {
            "analysis": validated.dict(),
            "llm_fispec_score": llm_fispec_score
        }

    except Exception as e:
        raise RuntimeError(
        f"LLM output validation failed: {e}\n\nRAW OUTPUT:\n{raw}"
    )