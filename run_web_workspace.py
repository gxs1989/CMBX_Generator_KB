from __future__ import annotations

import os
import sys
from pathlib import Path

import uvicorn


def main() -> None:
    log_path = os.environ.get("CMBX_WEB_LOG_FILE", "").strip()
    if log_path:
        target = Path(log_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        stream = target.open("a", encoding="utf-8", buffering=1)
        sys.stdout = stream
        sys.stderr = stream
    host = os.environ.get("CMBX_WEB_HOST", "0.0.0.0")
    port = int(os.environ.get("CMBX_WEB_PORT", "8765"))
    uvicorn.run("web_workspace.app:create_app", host=host, port=port, factory=True, log_level="info")


if __name__ == "__main__":
    main()
