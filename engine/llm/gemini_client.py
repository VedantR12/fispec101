from google import genai
import os

client = genai.Client(
    api_key=os.environ.get("GOOGLE_API_KEY")
)

def run_gemini(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text
