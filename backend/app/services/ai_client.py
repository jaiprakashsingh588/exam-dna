import os

from dotenv import load_dotenv
from google import genai
from openai import OpenAI

load_dotenv()


def get_ai_provider() -> str:
    return os.getenv("AI_PROVIDER", "gemini").lower()


def generate_text(prompt: str) -> str:
    provider = get_ai_provider()

    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set")

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
            contents=prompt,
        )

        return response.text or ""

    if provider == "nvidia":
        api_key = os.getenv("NVIDIA_API_KEY")

        if not api_key:
            raise RuntimeError("NVIDIA_API_KEY is not set")

        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key,
        )

        response = client.chat.completions.create(
            model=os.getenv(
                "NVIDIA_MODEL",
                "nvidia/nemotron-3-super-120b-a12b",
            ),
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096,
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError("NVIDIA returned no text content")

        return content

    raise ValueError(f"Unsupported AI_PROVIDER: {provider}")
