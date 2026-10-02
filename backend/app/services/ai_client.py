import os


def get_ai_provider() -> str:
    return os.getenv("AI_PROVIDER", "gemini").lower()
