from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


WORD_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
DC_NS = "{http://purl.org/dc/elements/1.1/}"
CP_NS = "{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}"


def _clean_text(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_docm(path: Path) -> tuple[dict[str, str], str]:
    metadata: dict[str, str] = {}
    paragraphs: list[str] = []
    with zipfile.ZipFile(path) as zf:
        if "docProps/core.xml" in zf.namelist():
            root = ET.fromstring(zf.read("docProps/core.xml"))
            fields = {
                "title": f"{DC_NS}title",
                "subject": f"{DC_NS}subject",
                "creator": f"{DC_NS}creator",
                "keywords": f"{CP_NS}keywords",
                "description": f"{DC_NS}description",
                "category": f"{CP_NS}category",
            }
            for key, tag in fields.items():
                node = root.find(tag)
                if node is not None and node.text:
                    metadata[key] = node.text.strip()
        doc = ET.fromstring(zf.read("word/document.xml"))
        for para in doc.iter(f"{WORD_NS}p"):
            chunks: list[str] = []
            for text_node in para.iter(f"{WORD_NS}t"):
                if text_node.text:
                    chunks.append(text_node.text)
            line = _clean_text("".join(chunks))
            if line:
                paragraphs.append(line)
    return metadata, "\n".join(f"{i}\t{line}" for i, line in enumerate(paragraphs))


def extract_pdf(path: Path) -> tuple[dict[str, str], str]:
    try:
        from pypdf import PdfReader
    except ImportError:
        PdfReader = None  # type: ignore

    if PdfReader is not None:
        reader = PdfReader(str(path))
        metadata = {str(k).lstrip("/"): str(v) for k, v in (reader.metadata or {}).items() if v}
        pages: list[str] = []
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            pages.append(f"[Page {i + 1}]\n{_clean_text(page_text)}")
        return metadata, "\n\n".join(pages)

    import fitz  # type: ignore

    doc = fitz.open(str(path))
    metadata = {str(k): str(v) for k, v in (doc.metadata or {}).items() if v}
    pages = []
    for i, page in enumerate(doc):
        pages.append(f"[Page {i + 1}]\n{_clean_text(page.get_text())}")
    return metadata, "\n\n".join(pages)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: extract_foq_td_text.py <source-folder> <output-folder>", file=sys.stderr)
        return 2
    source = Path(argv[1])
    output = Path(argv[2])
    output.mkdir(parents=True, exist_ok=True)
    for path in sorted(source.iterdir()):
        if path.name.startswith("~$") or not path.is_file():
            continue
        if path.suffix.lower() not in {".docm", ".docx", ".pdf"}:
            continue
        try:
            if path.suffix.lower() == ".pdf":
                metadata, text = extract_pdf(path)
            else:
                metadata, text = extract_docm(path)
        except Exception as exc:
            print(f"skipped {path.name}: {exc}")
            continue
        stem = re.sub(r"[^A-Za-z0-9_.-]+", "_", path.stem)
        metadata_lines = [f"{key}: {value}" for key, value in sorted(metadata.items())]
        (output / f"{stem}.metadata.txt").write_text("\n".join(metadata_lines), encoding="utf-8")
        (output / f"{stem}.text.txt").write_text(text, encoding="utf-8")
        print(f"extracted {path.name} -> {stem}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
