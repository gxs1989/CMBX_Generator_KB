from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from cmbx_container import CmbxElement, load_cmbx_package, summarize_package


ProgressCallback = Callable[[int, int, str, str], None]


def _element_payload(element: CmbxElement) -> dict[str, Any]:
    return {
        "id": element.id,
        "name": element.name,
        "kind": element.kind,
        "item_type": element.item_type,
        "size": element.size,
        "children": [_element_payload(child) for child in element.children],
    }


def build_inventory(cmbx_path: Path, output_path: Path, progress: ProgressCallback) -> dict[str, Any]:
    progress(0, 4, "preparing", "Reading CMBX package header")
    package = load_cmbx_package(cmbx_path)
    progress(1, 4, "running", "Classifying package elements")
    summary = summarize_package(package)
    progress(2, 4, "running", "Building sequence and injection tree")
    payload = {
        "file_name": cmbx_path.name,
        "summary": summary,
        "header": {
            key: value
            for key, value in package.header_attributes.items()
            if key in {"ArchiveVersion", "ChromeleonVersion", "DateCreated", "CreatedBy", "Comment"}
        },
        "tree": [_element_payload(element) for element in package.root_elements],
    }
    progress(3, 4, "validating", "Writing inventory cache")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_suffix(".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(output_path)
    progress(4, 4, "completed", "Inventory ready")
    return payload


def read_inventory(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
