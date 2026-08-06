from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
import urllib.error
import urllib.request
import zipfile

from generation_project import DEFAULT_WORKSPACE


AI_CONFIG_FILE = DEFAULT_WORKSPACE / "ai_config.json"
SMALL_FILE_LIMIT = 200 * 1024

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


@dataclass(frozen=True)
class PromptOptimization:
    prompt: str
    used_ai: bool
    detail: str


def load_ai_config() -> dict[str, str]:
    provider = "gpt"
    payload: dict[str, object] = {}
    if AI_CONFIG_FILE.is_file():
        try:
            loaded = json.loads(AI_CONFIG_FILE.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                payload = loaded
        except Exception:
            payload = {}
    configured = str(payload.get("provider") or "gpt").strip().lower()
    if configured in PROVIDER_DEFAULTS:
        provider = configured
    defaults = {
        "provider": provider,
        "base_url": PROVIDER_DEFAULTS[provider]["base_url"],
        "model": PROVIDER_DEFAULTS[provider]["model"],
        "api_key": "",
    }
    for key in defaults:
        if payload.get(key) is not None:
            defaults[key] = str(payload[key])
    return defaults


def _chat_endpoint(base_url: str) -> str:
    base = (base_url or "https://api.openai.com/v1").strip().rstrip("/")
    if base.endswith("/chat/completions"):
        return base
    if base in {"https://api.openai.com", "http://api.openai.com"}:
        return base + "/v1/chat/completions"
    return base + "/chat/completions"


def base_prompt(
    asset_type: str,
    modules: tuple[str, ...],
    user_request: str = "",
    *,
    has_method_basis: bool = False,
) -> str:
    kind = "Chromeleon Instrument Method MD" if asset_type == "method" else "Chromeleon Report Template MD"
    request = user_request.strip() or "[Paste the natural-language test/report requirement here before sending.]"
    basis = ""
    if asset_type == "report" and has_method_basis:
        basis = (
            "\nThe attached generated Method MD is the execution contract for this report. "
            "Derive channels, variables, audit events, RetTimes, timing windows and configuration "
            "from that Method MD; do not substitute unrelated template assumptions.\n"
        )
    return (
        f"Use the attached SPEC and knowledge-base files to generate one {kind}.\n"
        f"Modules: {', '.join(modules)}\n\n"
        "Requirement:\n"
        f"{request}\n"
        f"{basis}\n"
        "Follow the SPEC exactly. Return the complete generated Markdown only. "
        "Do not invent unsupported CM commands, formulas, channels, variables, or configuration."
    )


def optimize_prompt(
    asset_type: str,
    modules: tuple[str, ...],
    user_request: str,
    *,
    prepared_prompt: bool = False,
    has_method_basis: bool = False,
) -> PromptOptimization:
    original = user_request.strip() if prepared_prompt else base_prompt(
        asset_type, modules, user_request, has_method_basis=has_method_basis,
    )
    if not user_request.strip():
        return PromptOptimization(original, False, "No local request was entered; a web-model prompt template was packaged.")
    config = load_ai_config()
    if not config.get("api_key", "").strip():
        return PromptOptimization(original, False, "AI key is not configured; the original request was packaged unchanged.")
    kind = "Instrument Method MD" if asset_type == "method" else "Report Template MD"
    basis_rule = (
        "The package includes a generated Method MD. Tell the web AI to use it as the report execution "
        "contract and bind channels, variables, RetTimes, audit events and timing windows to it. "
        if asset_type == "report" and has_method_basis else ""
    )
    system = (
        "Rewrite fragmented user notes into one coherent, ordered generation request for a separate web AI. "
        "That web AI receives local Chromeleon SPEC and KB files. Preserve every temperature, duration, "
        "sequence order, device constraint, measurement scope, uncertainty and requested output. Resolve only "
        "language ambiguity; do not design the test, answer the request, add unsupported facts, or merely prepend "
        "headings and annotations. Make the selected modules and asset type explicit. "
        f"{basis_rule}"
        f"End with an explicit instruction to generate the complete {kind} according to the attached SPEC/KB "
        "and return Markdown only. Return only the final standalone prompt."
    )
    body = {
        "model": config.get("model") or "gpt-5.5",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": original},
        ],
    }
    request = urllib.request.Request(
        _chat_endpoint(config.get("base_url", "")),
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {config['api_key'].strip()}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            payload = json.loads(response.read().decode("utf-8"))
        content = str(payload["choices"][0]["message"]["content"]).strip()
        if not content:
            raise ValueError("AI returned an empty prompt.")
        return PromptOptimization(content, True, f"Prompt optimized with {body['model']}.")
    except (urllib.error.URLError, urllib.error.HTTPError, KeyError, ValueError, json.JSONDecodeError) as exc:
        return PromptOptimization(original, False, f"AI optimization failed; original request packaged: {exc}")


def create_web_ai_zip(
    destination: Path,
    *,
    asset_type: str,
    modules: tuple[str, ...],
    files: list[Path],
    prompt: PromptOptimization,
    small_context: bool,
) -> Path:
    missing = [path for path in files if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing KB file(s): " + "; ".join(str(path) for path in missing))
    if not files:
        raise ValueError("No matching SPEC/KB files were found for the selected modules.")
    if small_context:
        oversized = [path for path in files if path.stat().st_size >= SMALL_FILE_LIMIT]
        if oversized:
            raise ValueError("Small-file package contains a file >= 200 KB: " + "; ".join(path.name for path in oversized))
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("00_PROMPT.md", prompt.prompt)
        note = [
            "# Web AI package",
            "",
            f"Asset: {asset_type}",
            f"Modules: {', '.join(modules)}",
            f"Prompt mode: {'AI optimized' if prompt.used_ai else 'original/template'}",
        ]
        if small_context:
            note.extend(("", "This is the <200 KB-per-Markdown package.", "Extract the ZIP, then upload the individual files to a model with a 200 KB file limit."))
        else:
            note.extend(("", "Upload the ZIP directly if your web model accepts ZIP files, or extract and upload its files."))
        archive.writestr("README.md", "\n".join(note) + "\n")
        used_names: set[str] = set()
        for index, path in enumerate(files, start=1):
            name = path.name
            if name.lower() in used_names:
                name = f"{index:02d}_{name}"
            used_names.add(name.lower())
            archive.write(path, f"KB/{name}")
    return destination
