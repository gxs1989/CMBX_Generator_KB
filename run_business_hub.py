from __future__ import annotations

import os
import traceback
from pathlib import Path


os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
LOG_PATH = Path(__file__).resolve().parent / "logs" / "business_hub_launcher.log"


def _log(message: str) -> None:
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as handle:
            handle.write(message.rstrip() + "\n")
    except Exception:
        pass


def main() -> None:
    _log("business hub starting")
    try:
        from business_hub import main as run_hub

        _log("business hub module imported")
        run_hub()
        _log("business hub exited")
    except BaseException:
        _log("fatal exception:\n" + traceback.format_exc())
        raise


if __name__ == "__main__":
    main()
