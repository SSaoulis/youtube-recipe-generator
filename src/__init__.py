import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file in the project root
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise EnvironmentError("GEMINI_API_KEY not found in .env file")