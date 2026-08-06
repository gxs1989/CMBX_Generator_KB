from __future__ import annotations

from web_ai_package import (
    AIProviderSettings,
    MAX_CONTEXT_CHARS,
    PROVIDER_DEFAULTS,
    build_method_generation_prompt,
    build_report_generation_prompt,
    chat_endpoint,
    generate_method_markdown,
    generate_report_markdown,
)

__all__ = [
    "AIProviderSettings",
    "MAX_CONTEXT_CHARS",
    "PROVIDER_DEFAULTS",
    "build_method_generation_prompt",
    "build_report_generation_prompt",
    "chat_endpoint",
    "generate_method_markdown",
    "generate_report_markdown",
    "public_provider_defaults",
]


def public_provider_defaults() -> list[dict[str, str]]:
    return [dict(id=provider, **values) for provider, values in PROVIDER_DEFAULTS.items()]
