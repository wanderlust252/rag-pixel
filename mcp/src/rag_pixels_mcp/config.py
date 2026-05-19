import os

from dotenv import load_dotenv


DEFAULT_API_BASE_URL = "http://127.0.0.1:8000"

load_dotenv()


def api_base_url() -> str:
    return os.getenv("RAG_PIXELS_API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")


def auth_headers() -> dict[str, str]:
    api_key = os.getenv("RAG_PIXELS_API_KEY")
    if not api_key:
        return {}
    return {"Authorization": f"Bearer {api_key}"}
