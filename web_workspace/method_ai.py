from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
import urllib.error
import urllib.request


PROVIDER_DEFAULTS = {
    "gpt": {"label": "GPT", "base_url": "https://api.openai.com/v1", "model": "gpt-5.5"},
    "deepseek": {"label": "DeepSeek", "base_url": "https://api.deepseek.com/v1", "model": "deepseek-chat"},
}
MAX_CONTEXT_CHARS = 1_500_000


@dataclass(frozen=True)
class AIProviderSettings:
    provider: str
    base_url: str
    model: str
    api_key: str


def public_provider_defaults() -> list[dict[str, str]]:
    return [dict(id=provider, **values) for provider, values in PROVIDER_DEFAULTS.items()]


def chat_endpoint(base_url: str) -> str:
    base = base_url.strip().rstrip("/")
    if base.endswith("/chat/completions"):
        return base
    if base in {"https://api.openai.com", "http://api.openai.com"}:
        return base + "/v1/chat/completions"
    return base + "/chat/completions"


def build_method_generation_prompt(requirement: str, modules: tuple[str, ...], kb_files: list[Path]) -> str:
    sections: list[str] = []
    used = 0
    for path in kb_files:
        content = path.read_text(encoding="utf-8", errors="replace")
        section = f"\n\n===== KB FILE: {path.name} =====\n{content}"
        if used + len(section) > MAX_CONTEXT_CHARS:
            raise ValueError(
                "Selected Method KB exceeds the automatic API context limit. Choose fewer modules or use manual Web AI mode."
            )
        sections.append(section)
        used += len(section)
    return (
        "Generate one complete Chromeleon Instrument Method Markdown document from the requirement and the attached local KB.\n"
        f"Modules: {', '.join(modules)}\n"
        f"Requirement: {requirement.strip()}\n\n"
        "The Method SPEC is binding. Reuse verified command grammar, stage timing, Trigger serialization, variables, "
        "device symbols and configuration assumptions from the KB. Do not invent unsupported commands. Return only "
        "the complete Markdown document accepted by the MD-to-CMBX compiler; no explanation and no outer code fence."
        + "".join(sections)
    )


def generate_method_markdown(
    requirement: str,
    modules: tuple[str, ...],
    kb_files: list[Path],
    settings: AIProviderSettings,
) -> str:
    if not requirement.strip():
        raise ValueError("Enter a natural-language test requirement before API generation.")
    if not settings.api_key.strip():
        raise ValueError(f"Configure your {settings.provider} API key first.")
    prompt = build_method_generation_prompt(requirement, modules, kb_files)
    body = {
        "model": settings.model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a Chromeleon instrument-method author. Follow the supplied local Method SPEC and evidence "
                    "exactly. Your response is compiled automatically, so output only the complete Method Markdown."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    }
    request = urllib.request.Request(
        chat_endpoint(settings.base_url),
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {settings.api_key.strip()}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            payload = json.loads(response.read().decode("utf-8"))
        content = str(payload["choices"][0]["message"]["content"]).strip()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"{settings.provider} API returned HTTP {exc.code}: {detail}") from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"{settings.provider} API connection failed: {exc}") from exc
    except (KeyError, ValueError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"{settings.provider} API returned an invalid response") from exc
    if not content:
        raise RuntimeError(f"{settings.provider} API returned empty Method Markdown")
    return _strip_outer_fence(content)


def build_report_generation_prompt(
    requirement: str,
    modules: tuple[str, ...],
    kb_files: list[Path],
    method_markdowns: str | list[tuple[str, str]] | tuple[tuple[str, str], ...],
) -> str:
    if isinstance(method_markdowns, str):
        method_sources = [("Method 1", method_markdowns)]
    else:
        method_sources = [(str(name or f"Method {index}"), content) for index, (name, content) in enumerate(method_markdowns, 1)]
    method_context = "".join(
        f"\n\n===== BINDING METHOD MD {index}: {name} =====\n{content.strip()}"
        for index, (name, content) in enumerate(method_sources, 1)
    )
    sections: list[str] = []
    used = len(method_context)
    for path in kb_files:
        content = path.read_text(encoding="utf-8", errors="replace")
        section = f"\n\n===== KB FILE: {path.name} =====\n{content}"
        if used + len(section) > MAX_CONTEXT_CHARS:
            raise ValueError(
                "Selected Report KB and Method MD exceed the automatic API context limit. "
                "Choose fewer modules or use the small-context option."
            )
        sections.append(section)
        used += len(section)
    return (
        "Generate one complete Chromeleon Report Template Markdown document. The report must be derived from the "
        "supplied Method MD collection and must use only channels, audit properties, RetTimes, variables, and runtime "
        "evidence that those methods actually create. Keep the Method/Injection source explicit whenever names overlap.\n"
        f"Modules: {', '.join(modules)}\n"
        f"Report requirement: {requirement.strip()}\n\n"
        "The Report SPEC is binding. Return only the complete Report Markdown accepted by the MD-to-CMBX compiler; "
        "do not add an explanation or an outer code fence.\n\n"
        "The output is one shared Report Template for the complete Sequence represented by all binding methods. "
        "Treat each binding Method MD as an independent Injection-local runtime contract. RetTime numbers, channels, "
        "audit properties, and variables must not be merged across methods merely because their names match. "
        "A Method MD is a reusable method contract, not an Injection count: the same Method MD may later be assigned "
        "to multiple Injection rows, and it must be included only once in this authoring context. Unless exact "
        "Injection instances are explicitly supplied, make its result sheets reusable per Injection rather than "
        "assuming one Method MD means one Injection. Apply the SPEC's Multiple Method MD / Shared Sequence Report "
        "Contract and keep method coverage explicit."
        + method_context
        + "".join(sections)
    )


def generate_report_markdown(
    requirement: str,
    modules: tuple[str, ...],
    kb_files: list[Path],
    method_markdowns: str | list[tuple[str, str]] | tuple[tuple[str, str], ...],
    settings: AIProviderSettings,
) -> str:
    if not requirement.strip():
        raise ValueError("Enter the report requirement before automatic generation.")
    if isinstance(method_markdowns, str):
        has_method = bool(method_markdowns.strip())
    else:
        has_method = any(content.strip() for _, content in method_markdowns)
    if not has_method:
        raise ValueError("Choose at least one Method MD basis before automatic Report generation.")
    if not settings.api_key.strip():
        raise ValueError(f"Configure your {settings.provider} API key first.")
    prompt = build_report_generation_prompt(requirement, modules, kb_files, method_markdowns)
    body = {
        "model": settings.model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a Chromeleon report-template author. Follow the supplied Report SPEC and all binding "
                    "Method MD files exactly. Never invent runtime evidence. Output only the complete Report Markdown."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    }
    request = urllib.request.Request(
        chat_endpoint(settings.base_url),
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {settings.api_key.strip()}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            payload = json.loads(response.read().decode("utf-8"))
        content = str(payload["choices"][0]["message"]["content"]).strip()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"{settings.provider} API returned HTTP {exc.code}: {detail}") from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"{settings.provider} API connection failed: {exc}") from exc
    except (KeyError, ValueError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"{settings.provider} API returned an invalid response") from exc
    if not content:
        raise RuntimeError(f"{settings.provider} API returned empty Report Markdown")
    return _strip_outer_fence(content)


def _strip_outer_fence(content: str) -> str:
    match = re.fullmatch(r"\s*```(?:markdown|md)?\s*\n(.*)\n```\s*", content, re.I | re.S)
    return match.group(1).strip() + "\n" if match else content.rstrip() + "\n"
