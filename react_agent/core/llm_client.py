from __future__ import annotations

from openai import OpenAI

from .llm_config import LLMSettings, get_llm_settings


class LLMClient:
    """Thin OpenAI-compatible client; provider details live in environment settings."""

    def __init__(
        self,
        model: str | None = None,
        *,
        settings: LLMSettings | None = None,
        client: OpenAI | None = None,
    ):
        self.settings = settings or get_llm_settings()
        self.model = model or self.settings.model
        self.client = client or OpenAI(
            base_url=self.settings.base_url,
            api_key=self.settings.api_key,
            timeout=self.settings.timeout_seconds,
        )

    def chat(self, messages) -> str:
        print("\n\nWaiting for model")
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        content = response.choices[0].message.content
        if not isinstance(content, str) or not content:
            raise RuntimeError("LLM returned no text content")
        return content
    