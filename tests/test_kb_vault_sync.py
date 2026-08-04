from __future__ import annotations

from pathlib import Path

from tools import sync_kb_vault as sync


def test_collect_verify_and_long_path_alias(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "repo"
    managed = repo / "knowledge_vault"
    kb_root = tmp_path / "kb"
    engineering = repo / "docs" / "PLAN.md"
    skill_root = tmp_path / "skills" / "example-skill"
    # Keep the source valid on Windows; the deliberately small managed-path
    # threshold below is what exercises the stable alias behavior.
    long_source = kb_root / "Method Script Generator" / "nested" / "method_script.md"
    for path, content in (
        (engineering, "# Engineering\n"),
        (skill_root / "SKILL.md", "# Skill\n"),
        (long_source, "# Long operational note\n"),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    monkeypatch.setattr(sync, "REPO_ROOT", repo)
    monkeypatch.setattr(sync, "MANAGED_ROOT", managed)
    monkeypatch.setattr(sync, "SKILL_ROOTS", (skill_root,))
    monkeypatch.setattr(sync, "SAFE_PATH_LENGTH", 120)
    monkeypatch.setattr(sync, "tracked_markdown", lambda: [engineering])

    entries = sync.collect(kb_root)

    assert len(entries) == 3
    operational = next(item for item in entries if item.layer == "operational")
    assert "_long_paths" in operational.managed_path
    assert sync.verify(kb_root) == []
    assert (managed / "manifest.json").is_file()
    assert (managed / "manifest.csv").is_file()
