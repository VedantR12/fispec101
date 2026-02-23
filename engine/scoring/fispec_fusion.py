def fuse_fispec_scores(engine_score: float, llm_score: float) -> float:
    final = (0.7 * engine_score) + (0.3 * llm_score)
    return round(final, 2)
