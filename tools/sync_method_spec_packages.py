from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys
import zipfile


MODULE_ROOT = Path(__file__).resolve().parents[1]
if str(MODULE_ROOT) not in sys.path:
    sys.path.insert(0, str(MODULE_ROOT))

from tools.build_online_gpt_method_kb import build_spec


DEFAULT_KB_ROOT = Path(r"C:\ProgramData\CMBX Data Explorer Workspace\KB")
MODULES = ("TCC", "VAS", "RID")
DELIVERY_FILES = (
    "01_METHOD_SPEC.md",
    "02_METHOD_ORIGINAL_SCRIPTS.md",
    "03_METHOD_SUMMARIES.md",
)


def _refresh_small_zip(kb_root: Path, module: str) -> None:
    profile = kb_root / "KB_Online_GPT" / "03_Small_Context" / module / "Method"
    if not profile.is_dir():
        return
    archive_path = profile.parent / "Method_3Files_Under200K.zip"
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in DELIVERY_FILES:
            source = profile / name
            if source.is_file():
                archive.write(source, arcname=name)


def sync(repo_root: Path, kb_root: Path) -> list[Path]:
    spec_source = repo_root / "docs" / "CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md"
    rules_source = repo_root / "docs" / "CM Compiler Rules.MD"
    if not spec_source.is_file() or not rules_source.is_file():
        raise FileNotFoundError("Canonical Method SPEC or compiler rules are missing.")

    destinations = (
        kb_root / "FOQ Template",
        kb_root / "Method Script Generator" / "Generator Spec",
    )
    written: list[Path] = []
    for destination in destinations:
        destination.mkdir(parents=True, exist_ok=True)
        for source in (spec_source, rules_source):
            target = destination / source.name
            shutil.copy2(source, target)
            written.append(target)

    generated_spec = build_spec(kb_root)
    online_root = kb_root / "KB_Online_GPT"
    for profile_name in ("02_Full_Context", "03_Small_Context"):
        for module in MODULES:
            target = online_root / profile_name / module / "Method" / "01_METHOD_SPEC.md"
            if target.parent.is_dir():
                target.write_text(generated_spec, encoding="utf-8")
                written.append(target)
    for module in MODULES:
        _refresh_small_zip(kb_root, module)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize the canonical Method SPEC and rebuild online SPEC packages.")
    parser.add_argument("--repo-root", type=Path, default=MODULE_ROOT)
    parser.add_argument("--kb-root", type=Path, default=DEFAULT_KB_ROOT)
    args = parser.parse_args()
    written = sync(args.repo_root.resolve(), args.kb_root.resolve())
    for path in written:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
