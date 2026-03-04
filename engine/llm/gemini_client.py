import os
import google.generativeai as genai

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create model instance once
model = genai.GenerativeModel("gemini-2.5-flash")

def run_gemini(prompt: str) -> str:
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0,
            "top_p": 1,
        }
    )
    return response.text