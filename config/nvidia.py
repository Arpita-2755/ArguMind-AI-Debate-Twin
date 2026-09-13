import os

from dotenv import load_dotenv

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

NVIDIA_MODEL = "deepseek-ai/deepseek-v4-flash-0731"

NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"