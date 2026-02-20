from pydantic import BaseModel, Field
from typing import List, Optional


class Rating(BaseModel):
    value: float = Field(ge=0, le=10)
    basis: str


class Ratings(BaseModel):
    fispec_score: Rating
    indian_lifestyle_score: Rating


class NutritionItem(BaseModel):
    value: Optional[float] = None
    unit: Optional[str] = None
    impact: str


class NutritionBreakdown(BaseModel):
    energy: NutritionItem
    fats: NutritionItem
    sugar: NutritionItem
    salt: NutritionItem
    protein: NutritionItem
    fiber: NutritionItem


class AdditiveAnalysis(BaseModel):
    name: str
    code: Optional[str]
    why_used: str
    disclosure: str
    confidence: Optional[str] = None
    general_note: str


class Summary(BaseModel):
    one_line: str


class LLMOutput(BaseModel):
    ratings: Ratings
    summary: Summary
    nutrition_breakdown: NutritionBreakdown
    additives_analysis: List[AdditiveAnalysis]
