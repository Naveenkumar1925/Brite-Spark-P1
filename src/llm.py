"""The one place the model is called. Swap here to change model."""
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


def generate(prompt):
    """Send prompt to Gemini, return the text response.
    Fails with a clear message if the key is missing."""
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Add it to a .env file:\n"
            "  GEMINI_API_KEY=your_key"
        )

    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )
    return response.text