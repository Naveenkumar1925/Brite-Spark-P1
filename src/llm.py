"""The one place the model is called. Swap here to change model."""
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

MODEL = "gemini-3.6-flash"


def generate(prompt, retries=3):
    """Send prompt to Gemini, return the text.
    Retries a few times if the server is briefly busy (503)."""
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Add it to a .env file:\n"
            "  GEMINI_API_KEY=your_key"
        )

    client = genai.Client(api_key=key)

    last_error = None
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
            )
            return response.text
        except errors.ServerError as e:
            last_error = e
            wait = 2 * (attempt + 1)   # 2s, 4s, 6s
            print(f"Model busy, retrying in {wait}s...")
            time.sleep(wait)

    raise RuntimeError(
        f"The model is busy right now (after {retries} tries). "
        f"Please try again in a moment.\nDetails: {last_error}"
    )