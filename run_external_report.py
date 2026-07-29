from __future__ import annotations

import tkinter as tk
from pathlib import Path

from external_report_window import ExternalReportWindow


def main() -> None:
    root = tk.Tk()
    root.withdraw()
    window = ExternalReportWindow(root, output_folder=Path(r"C:\ProgramData\CMBX Data Explorer Workspace\exports"))

    def close() -> None:
        try:
            window.top.destroy()
        finally:
            root.destroy()

    window.top.protocol("WM_DELETE_WINDOW", close)
    root.mainloop()


if __name__ == "__main__":
    main()
