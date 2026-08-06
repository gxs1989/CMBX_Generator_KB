from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
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
