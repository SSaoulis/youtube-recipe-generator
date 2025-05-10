import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file in the project root
env_path = Path(__file__).resolve().parent.parent / ".env"

# Check if the .env file exists
if not env_path.is_file():
    raise FileNotFoundError(
        f".env file not found at {env_path}. Generate one and add your API key."
    )

load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError("GEMINI_API_KEY not found in .env file")
