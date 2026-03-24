import json
from engine.llm.schema import LLM_OUTPUT_SCHEMA


def build_llm_prompt(product_data: dict) -> str:
    """
    Builds a strict prompt for the LLM.
    The LLM must return JSON ONLY, matching LLM_OUTPUT_SCHEMA.
    """

    system_role = """
You are a food-label analysis expert.
You explain ingredients, additives, and nutrition factually.
Explanations should be informative, balanced, and easy to understand.
You never guess missing data.
You never invent values.
You follow schema rules strictly.
"""

    rules = """
RULES (MANDATORY):

- Output ONLY raw JSON
- DO NOT wrap output in ``` or ```json
- DO NOT use markdown
- DO NOT add explanations
- The first character MUST be {
- The last character MUST be }

If you violate these rules, the response will be rejected.

1. Use ONLY the data provided below.
2. Do NOT invent nutrition values or additive codes.
3. If an additive appears in ingredients but not in the additives list:
   - include it in additives_analysis
   - set code = null
   - set disclosure = "Not disclosed"
4. If a nutrition value is null:
   - explain its absence in the impact text
5. Ratings must be reasoned and conservative.
6. Output must be VALID JSON ONLY.
7. Output must match the schema EXACTLY.
"""

    explanation_rules = """
EXPLANATION STYLE:

The explanations must be clear, educational, and informative.

For nutrition impacts:
- Write 3-4 sentences explaining how the nutrient level affects health.
- Clearly tell if the element is in low/moderate/high quantity as per the general norms by WHO(World health organization) or any authorized organization.
- Mention typical dietary considerations where relevant.
- analyze all the nutritional elements and give a context if the product with a certain quantity of a particuualr nutritional element is good or not.
- Tell the user clearly if the particular nutritional element is low or moderate or high quantity
- If the quantity is low then tell them the health impacts of that particular nutritional elements if the quantity is low and same for moderate and higher values

For additives:
- Write 2–3 sentences explaining:
  • what the additive is
  • why it is used in foods
  • any relevant health or regulatory context
  * if the given additives is hazardous or not for the consumer's health
  * if the given additive is suitable from the indian consumer's perspective

Avoid one-line explanations.

Do not exaggerate risks. maintain a balanced information with risks/benefits or if the element is neutral.
"""



    provided_data = f"""
PRODUCT DATA (SOURCE OF TRUTH):

Product name:
{product_data.get("product_name")}

Brand:
{product_data.get("brands")}

Ingredients list:
{json.dumps(product_data.get("ingredients", []), indent=2)}

Detected additives (from engine):
{json.dumps(product_data.get("additives", []), indent=2)}

Nutrition per 100g:
{json.dumps(product_data.get("nutrition_100g", {}), indent=2)}
"""

    schema_definition = f"""
EXPECTED OUTPUT JSON SCHEMA:
{json.dumps(LLM_OUTPUT_SCHEMA, indent=2)}
"""

    final_instruction = """
Generate the final analysis strictly according to the schema.
Do not include explanations outside JSON.
"""

    prompt = (
        system_role
        + rules
        + explanation_rules
        + provided_data
        + schema_definition
        + final_instruction
    )

    return prompt
