import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

DEFAULT_MODEL = "gemini-3.6-flash"

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)