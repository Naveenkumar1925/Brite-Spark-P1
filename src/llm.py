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
    Retries on temporary errors (server busy or rate limit)."""
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
        except errors.ClientError as e:
            # 429 = rate limit. Wait longer and retry.
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                last_error = e
                wait = 15 * (attempt + 1)   # 15s, 30s, 45s
                print(f"Rate limit hit, waiting {wait}s...")
                time.sleep(wait)
            else:
                raise
        except errors.ServerError as e:
            last_error = e
            wait = 2 * (attempt + 1)        # 2s, 4s, 6s
            print(f"Model busy, retrying in {wait}s...")
            time.sleep(wait)

    raise RuntimeError(
        f"The model is unavailable after {retries} tries "
        f"(busy or rate-limited). Please try again shortly.\n"
        f"Details: {last_error}"
    )