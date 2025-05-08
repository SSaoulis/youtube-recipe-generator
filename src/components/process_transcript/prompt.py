import os
from pathlib import Path
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

base_prompt_path = os.path.join(os.path.dirname(__file__), "base_prompt.txt")

with open(base_prompt_path, "r") as f:
    BASE_PROMPT = f.read()


def get_gemini_response(transcript: str):

    gemini_input = BASE_PROMPT + "\n" + transcript

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=gemini_input,
    )
    return response.text
