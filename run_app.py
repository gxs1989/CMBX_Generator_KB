from __future__ import annotations

import os
from pathlib import Path
import traceback

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

LOG_PATH = Path(__file__).resolve().parent / "logs" / "launcher_last.log"


def _log(message: str) -> None:
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as handle:
            handle.write(message.rstrip() + "\n")
    except Exception:
        pass


def main() -> None:
    _log("run_app.py starting")
    try:
        import app

        _log("app module imported")
        app.main()
        _log("app main exited")
    except BaseException:
        _log("fatal exception in run_app.py:")
        _log(traceback.format_exc())
        raise


if __name__ == "__main__":
    main()
