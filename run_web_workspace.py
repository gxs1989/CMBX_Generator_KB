from __future__ import annotations

import os

import uvicorn


def main() -> None:
    host = os.environ.get("CMBX_WEB_HOST", "0.0.0.0")
    port = int(os.environ.get("CMBX_WEB_PORT", "8765"))
    uvicorn.run("web_workspace.app:create_app", host=host, port=port, factory=True, log_level="info")


if __name__ == "__main__":
    main()
