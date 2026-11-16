from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

_DEFAULT_DEEPSEEK_URL = "https://api.deepseek.com"
_DEFAULT_DEEPSEEK_MODEL = "deepseek-chat"
_OPENROUTER_URL = "https://openrouter.ai/api/v1"


@dataclass(frozen=True)
class LLMSettings:
    api_key: str
    base_url: str
    model: str
    timeout_seconds: float = 120.0


def _load_environment() -> None:
    configured = os.getenv("LLM_ENV_FILE")
    if configured:
        path = Path(configured).expanduser().resolve()
        if not path.is_file():
            raise ValueError(f"LLM_ENV_FILE does not exist: {path}")
        load_dotenv(path, override=False)
        return

    repository = Path(__file__).resolve().parents[2]
    candidates = (
        Path.cwd() / "deploy" / ".env",
        repository / "deploy" / ".env",
        Path.cwd() / ".env",
        repository / ".env",
    )
    for path in candidates:
        if path.is_file():
            load_dotenv(path, override=False)
            return


def get_llm_settings() -> LLMSettings:
    """Load one OpenAI-compatible provider from environment variables.

    LLM_API_KEY selects the provider-neutral path. OPENROUTER_API_KEY remains a
    compatibility fallback for existing installations.
    """

    _load_environment()
    api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("Set LLM_API_KEY in deploy/.env or the shell")

    using_legacy_openrouter = not os.getenv("LLM_API_KEY") and bool(
        os.getenv("OPENROUTER_API_KEY")
    )
    base_url = os.getenv("LLM_BASE_URL") or (
        _OPENROUTER_URL if using_legacy_openrouter else _DEFAULT_DEEPSEEK_URL
    )
    model = os.getenv("LLM_MODEL") or _DEFAULT_DEEPSEEK_MODEL
    try:
        timeout = float(os.getenv("LLM_TIMEOUT_SECONDS", "120"))
    except ValueError as exc:
        raise ValueError("LLM_TIMEOUT_SECONDS must be numeric") from exc
    if timeout <= 0:
        raise ValueError("LLM_TIMEOUT_SECONDS must be positive")
    return LLMSettings(api_key=api_key, base_url=base_url, model=model, timeout_seconds=timeout)
