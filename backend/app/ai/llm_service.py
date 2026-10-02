"""Provider-agnostic LLM gateway.

All AI traffic goes through this module so the provider (Gemini / OpenAI) can be
swapped by changing `AI_PROVIDER` in .env. Route files never call an SDK.

The gateway never raises: if the key is missing or the provider fails, it
returns a `LLMResult` with `ok=False` and the caller falls back to demo content.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Any

from app.core.config import settings

logger = logging.getLogger(__name__)

# How long we are willing to wait on the provider before falling back.
LLM_TIMEOUT_SECONDS = 45.0


@dataclass
class LLMResult:
    """Outcome of a single LLM call."""

    ok: bool
    text: str
    error: str = ""

    @property
    def failed(self) -> bool:
        return not self.ok


def _clean(text: str | None) -> str:
    return (text or "").strip()


async def _call_gemini(system_prompt: str, user_prompt: str) -> str:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=settings.resolved_api_key)
    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0.7,
        response_mime_type="application/json",
    )
    response = await asyncio.to_thread(
        client.models.generate_content,
        model=settings.resolved_model,
        contents=user_prompt,
        config=config,
    )
    return _clean(response.text)


async def _call_openai(system_prompt: str, user_prompt: str) -> str:
    import httpx

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.resolved_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.resolved_model if settings.resolved_model.startswith("gpt") else "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.7,
        "response_format": {"type": "json_object"},
    }
    async with httpx.AsyncClient(timeout=LLM_TIMEOUT_SECONDS) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
    return _clean(data["choices"][0]["message"]["content"])


async def generate_json(
    system_prompt: str,
    user_prompt: str,
    *,
    temperature: float | None = None,
) -> LLMResult:
    """Ask the configured LLM for a JSON string.

    Returns an LLMResult; `ok` is False when demo mode is active or the
    provider errored. Callers must handle the fallback path.
    """
    if not settings.ai_enabled:
        return LLMResult(
            ok=False,
            text="",
            error="No AI API key configured - running in demo mode.",
        )

    provider = settings.ai_provider.strip().lower()
    try:
        if provider == "gemini":
            text = await asyncio.wait_for(
                _call_gemini(system_prompt, user_prompt), timeout=LLM_TIMEOUT_SECONDS
            )
        elif provider == "openai":
            text = await asyncio.wait_for(
                _call_openai(system_prompt, user_prompt), timeout=LLM_TIMEOUT_SECONDS
            )
        else:
            return LLMResult(
                ok=False,
                text="",
                error=f"Unsupported AI_PROVIDER '{settings.ai_provider}'.",
            )
    except asyncio.TimeoutError:
        logger.warning("LLM call timed out after %ss", LLM_TIMEOUT_SECONDS)
        return LLMResult(ok=False, text="", error="AI provider timed out.")
    except Exception as exc:  # noqa: BLE001 - any provider failure must be survivable
        logger.warning("LLM call failed: %s", exc)
        # Never leak the key or full request in the error surface.
        return LLMResult(ok=False, text="", error=f"AI provider error: {type(exc).__name__}")

    if not text:
        return LLMResult(ok=False, text="", error="AI provider returned an empty response.")

    return LLMResult(ok=True, text=text)


async def generate_json_or_none(
    system_prompt: str, user_prompt: str, **kwargs: Any
) -> dict | None:
    """Convenience wrapper: returns a parsed dict or None to trigger fallback."""
    from app.utils.helpers import safe_json_loads, strip_code_fence

    result = await generate_json(system_prompt, user_prompt, **kwargs)
    if result.failed:
        return None

    parsed = safe_json_loads(strip_code_fence(result.text))
    if isinstance(parsed, dict):
        return parsed
    if isinstance(parsed, list):
        return {"items": parsed}
    return None
