import json
from typing import Any, Optional

from .prompts import (
    HOME_PROMPT,
    JEWELRY_PROMPT,
    PARTY_PROMPT,
)


def _get_client():
    from ..config import settings

    if not settings.gemini_api_key:
        return None

    try:
        from google import genai

        return genai.Client(
            api_key=settings.gemini_api_key
        )
    except Exception:
        return None


def generate_with_gemini(
    planner_type: str,
    user_data: dict[str, Any],
    fallback: dict[str, Any],
) -> dict[str, Any]:

    client = _get_client()

    if client is None:
        fallback["source"] = "fallback"
        return fallback

    prompts = {
        "home": HOME_PROMPT,
        "party": PARTY_PROMPT,
        "jewelry": JEWELRY_PROMPT,
    }

    system_prompt = prompts.get(
        planner_type,
        "Create a useful budget recommendation.",
    )

    request = f"""
{system_prompt}

User data:
{json.dumps(user_data, indent=2)}

Return ONLY valid JSON with this structure:

{{
  "summary": "string",
  "estimated_total": 0,
  "items": [
    {{
      "name": "string",
      "category": "string",
      "price": 0,
      "reason": "string",
      "platform": "string",
      "url": "string"
    }}
  ],
  "tips": ["string"]
}}
"""

    try:
        response = client.models.generate_content(
            model=__import__(
                "app.config",
                fromlist=["settings"],
            ).settings.gemini_model,
            contents=request,
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace(
                "```json",
                "",
            ).replace(
                "```",
                "",
            ).strip()

        parsed = json.loads(text)

        parsed["source"] = "gemini"

        return parsed

    except Exception:
        fallback["source"] = "fallback"
        return fallback