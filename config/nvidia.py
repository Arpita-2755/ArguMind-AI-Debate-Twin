import os

from dotenv import load_dotenv

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

NVIDIA_MODEL = "openai/gpt-oss-20b"

NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"

# The free NIM endpoint can hang for minutes; fail fast so the router falls back.
NVIDIA_TIMEOUT_SECONDS = 60