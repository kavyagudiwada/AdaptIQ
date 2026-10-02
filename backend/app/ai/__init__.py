"""AI module package: LLM gateway, prompts and the four agents."""

from app.ai.llm_service import LLMResult, generate_json, generate_json_or_none

__all__ = ["LLMResult", "generate_json", "generate_json_or_none"]
