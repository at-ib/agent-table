import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DOWNLOAD_PATH = "./downloads/"

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required")

os.makedirs(DOWNLOAD_PATH, exist_ok=True)
