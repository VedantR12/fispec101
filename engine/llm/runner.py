import json
from engine.llm.groq_client import run_groq
from engine.llm.prompt_builder import build_llm_prompt
from engine.llm.models import LLMOutput


def run_llm_analysis(product_data: dict) -> dict:

    prompt = build_llm_prompt(product_data)

    raw = run_groq(prompt)

    try:
        parsed = json.loads(raw)

        validated = LLMOutput(**parsed)

        llm_fispec_score = (
            validated.ratings.fispec_score.value
            if validated.ratings and validated.ratings.fispec_score
            else None
        )

        result = {
            "analysis": validated.dict(),
            "llm_fispec_score": llm_fispec_score
        }

        return result

    except Exception as e:
        raise RuntimeError(
            f"LLM output validation failed: {e}\n\nRAW OUTPUT:\n{raw}"
        )