from __future__ import annotations

import sys
from pathlib import Path
import zipfile

import pytest


MODULE_ROOT = Path(__file__).resolve().parents[1]
if str(MODULE_ROOT) not in sys.path:
    sys.path.insert(0, str(MODULE_ROOT))

import web_ai_package
from web_ai_package import PromptOptimization, SMALL_FILE_LIMIT, base_prompt, create_web_ai_zip, optimize_prompt


def test_base_prompt_keeps_web_entry_placeholder_when_local_intent_is_empty() -> None:
    prompt = base_prompt("method", ("TCC", "VAS"), "")
    assert "Chromeleon Instrument Method MD" in prompt
    assert "TCC, VAS" in prompt
    assert "Paste the natural-language" in prompt
    assert "complete generated Markdown only" in prompt


def test_report_prompt_uses_generated_method_as_execution_contract() -> None:
    prompt = base_prompt("report", ("TCC",), "Show valve positions.", has_method_basis=True)
    assert "Method MD is the execution contract" in prompt
    assert "channels, variables, audit events, RetTimes" in prompt


def test_prepared_prompt_is_not_wrapped_again_when_ai_is_unavailable(monkeypatch) -> None:
    monkeypatch.setattr(web_ai_package, "load_ai_config", lambda: {"base_url": "", "model": "gpt", "api_key": ""})
    visible_prompt = "Use these files.\nRequirement: keep this exact reviewed prompt."
    result = optimize_prompt("method", ("TCC",), visible_prompt, prepared_prompt=True)
    assert result.prompt == visible_prompt
    assert not result.used_ai


def test_optimizer_requests_a_coherent_standalone_generation_prompt(monkeypatch) -> None:
    captured = {}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def read(self):
            return b'{"choices":[{"message":{"content":"coherent prompt"}}]}'

    monkeypatch.setattr(web_ai_package, "load_ai_config", lambda: {"base_url": "https://example.test/v1", "model": "gpt-test", "api_key": "key"})

    def fake_open(request, timeout):
        captured["body"] = request.data.decode("utf-8")
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr(web_ai_package.urllib.request, "urlopen", fake_open)
    result = optimize_prompt("report", ("TCC",), "valve time; position; calculate speed", has_method_basis=True)

    assert result.prompt == "coherent prompt"
    assert result.used_ai
    body = captured["body"]
    assert "Rewrite fragmented user notes" in body
    assert "Method MD" in body
    assert "complete Report Template MD" in body


def test_create_small_web_ai_zip_contains_prompt_readme_and_kb(tmp_path: Path) -> None:
    kb = tmp_path / "01_METHOD_SPEC.md"
    kb.write_text("spec", encoding="utf-8")
    output = tmp_path / "package.zip"

    create_web_ai_zip(
        output,
        asset_type="method",
        modules=("TCC",),
        files=[kb],
        prompt=PromptOptimization("do the test", False, "original"),
        small_context=True,
    )

    with zipfile.ZipFile(output) as archive:
        assert set(archive.namelist()) == {"00_PROMPT.md", "README.md", "KB/01_METHOD_SPEC.md"}
        assert archive.read("00_PROMPT.md").decode("utf-8") == "do the test"
        assert "200 KB" in archive.read("README.md").decode("utf-8")


def test_small_package_rejects_oversized_markdown(tmp_path: Path) -> None:
    kb = tmp_path / "large.md"
    kb.write_bytes(b"x" * SMALL_FILE_LIMIT)
    with pytest.raises(ValueError, match="200 KB"):
        create_web_ai_zip(
            tmp_path / "package.zip",
            asset_type="method",
            modules=("TCC",),
            files=[kb],
            prompt=PromptOptimization("prompt", False, "original"),
            small_context=True,
        )
