from __future__ import annotations

import re
import threading
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from business_ui_components import RoundedButton, RoundedPanel, enable_dpi_awareness
from generation_project import DEFAULT_PROJECT_ROOT, AssetGenerationRequest, generate_asset, preflight_asset
from sequence_package_builder import (
    MultiSequencePackageRequest,
    SequenceInjectionRequest,
    build_multi_sequence_package,
)


APP_DIR = Path(__file__).resolve().parent
DEFAULT_CARRIER = APP_DIR / "assets" / "sequence_carrier_native_test1.cmbx"


def _safe_name(value: str, fallback: str = "item") -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._ -]+", "_", Path(value).name).strip(" ._")
    return (cleaned or fallback)[:80]


class SequenceGenerationWindow:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.colors = {
            "window": "#FFFFFF", "panel": "#F5F5F6", "border": "#E3E4E7",
            "text": "#222326", "muted": "#7C8087", "primary": "#3598F5",
            "primary_hover": "#2389EB", "warning": "#A85D00", "success": "#198754",
            "error": "#C4322B", "error_soft": "#FEE2E2",
        }
        self.injections: list[dict[str, object]] = []
        self.busy = False
        self.result_path: Path | None = None
        self.report_md = tk.StringVar()
        self.sequence_name = tk.StringVar()
        self.cm_version = tk.StringVar(value="7.3")
        self.output_root = tk.StringVar(value=str(DEFAULT_PROJECT_ROOT))
        self._setup_window()
        self._build_shell()

    def _setup_window(self) -> None:
        self.root.title("Sequence Generation")
        self.root.geometry("1180x760")
        self.root.minsize(980, 640)
        self.root.configure(bg=self.colors["window"])
        try:
            self.root.state("zoomed")
        except tk.TclError:
            pass

    def _font(self, size: int, weight: str = "normal") -> tuple[str, int, str]:
        return ("Segoe UI", size, weight)

    def _button(self, parent: tk.Misc, text: str, command, *, neutral: bool = False, width: int = 130) -> RoundedButton:
        return RoundedButton(
            parent, text=text, command=command,
            bg=self.colors["primary"] if not neutral else "#FFFFFF",
            hover_bg=self.colors["primary_hover"] if not neutral else "#EEF2F7",
            fg="#FFFFFF" if not neutral else self.colors["text"],
            border=self.colors["border"] if neutral else self.colors["primary"],
            font=self._font(10, "bold"), width=width, radius=10, height=36,
        )

    def _build_shell(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        header = tk.Frame(self.root, bg=self.colors["window"])
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(22, 10))
        tk.Label(header, text="Sequence Generation", font=self._font(18, "bold"), bg=self.colors["window"], fg=self.colors["text"]).pack(anchor="w")
        tk.Label(
            header,
            text="Bind one or more Method MDs and one shared Report MD into a multi-Injection Sequence CMBX.",
            font=self._font(10), bg=self.colors["window"], fg=self.colors["muted"],
        ).pack(anchor="w", pady=(3, 0))

        body = tk.Frame(self.root, bg=self.colors["window"])
        body.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 10))
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)
        body.rowconfigure(0, weight=1)

        left = RoundedPanel(body, fill=self.colors["panel"], border=self.colors["border"], radius=12, padding=12, parent_bg=self.colors["window"])
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=6)
        left.body.columnconfigure(0, weight=1)
        left.body.rowconfigure(1, weight=1)
        tk.Label(left.body, text="Injection methods", font=self._font(13, "bold"), bg=left.body["bg"], fg=self.colors["text"]).grid(row=0, column=0, sticky="w", padx=8, pady=(6, 6))
        self.method_tree = ttk.Treeview(
            left.body, columns=("injection", "md"), show="headings", selectmode="extended",
            style="Sequence.Treeview",
        )
        self.method_tree.heading("injection", text="Injection name")
        self.method_tree.heading("md", text="Method MD")
        self.method_tree.column("injection", width=180, stretch=False)
        self.method_tree.column("md", width=430, stretch=True)
        ybar = ttk.Scrollbar(left.body, orient="vertical", command=self.method_tree.yview)
        self.method_tree.configure(yscrollcommand=ybar.set)
        self.method_tree.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 6))
        ybar.grid(row=1, column=1, sticky="ns", pady=(0, 6))
        tree_actions = tk.Frame(left.body, bg=left.body["bg"])
        tree_actions.grid(row=2, column=0, columnspan=2, sticky="ew", padx=8, pady=(0, 8))
        self._button(tree_actions, "Add Method MD(s)", self._add_methods, width=150).pack(side="left")
        self._button(tree_actions, "Rename", self._rename_injection, neutral=True, width=100).pack(side="left", padx=8)
        self._button(tree_actions, "Remove", self._remove_selected, neutral=True, width=100).pack(side="left")
        self._button(tree_actions, "Clear", self._clear_injections, neutral=True, width=90).pack(side="right")

        right = RoundedPanel(body, fill=self.colors["panel"], border=self.colors["border"], radius=12, padding=12, parent_bg=self.colors["window"])
        right.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=6)
        form = right.body
        form.columnconfigure(1, weight=1)
        tk.Label(form, text="Shared Report MD", font=self._font(13, "bold"), bg=form["bg"], fg=self.colors["text"]).grid(row=0, column=0, columnspan=2, sticky="w", padx=8, pady=(6, 8))
        tk.Entry(form, textvariable=self.report_md, font=self._font(10), relief="flat", highlightthickness=1, highlightbackground=self.colors["border"], bg="#FFFFFF").grid(row=1, column=0, columnspan=2, sticky="ew", padx=8, pady=(0, 6), ipady=6)
        self._button(form, "Choose Report MD", self._choose_report_md, neutral=True, width=160).grid(row=2, column=0, columnspan=2, sticky="w", padx=8, pady=(0, 12))

        tk.Label(form, text="Sequence name", font=self._font(10, "bold"), bg=form["bg"], fg=self.colors["text"]).grid(row=3, column=0, sticky="w", padx=8, pady=6)
        tk.Entry(form, textvariable=self.sequence_name, font=self._font(10), relief="flat", highlightthickness=1, highlightbackground=self.colors["border"], bg="#FFFFFF").grid(row=3, column=1, sticky="ew", padx=(0, 8), pady=6, ipady=6)
        tk.Label(form, text="CM target", font=self._font(10, "bold"), bg=form["bg"], fg=self.colors["text"]).grid(row=4, column=0, sticky="w", padx=8, pady=6)
        ttk.Combobox(form, textvariable=self.cm_version, values=("7.3", "7.2 compatible"), state="readonly", font=self._font(10)).grid(row=4, column=1, sticky="w", padx=(0, 8), pady=6)
        tk.Label(form, text="Output folder", font=self._font(10, "bold"), bg=form["bg"], fg=self.colors["text"]).grid(row=5, column=0, sticky="w", padx=8, pady=6)
        tk.Entry(form, textvariable=self.output_root, font=self._font(10), relief="flat", highlightthickness=1, highlightbackground=self.colors["border"], bg="#FFFFFF").grid(row=5, column=1, sticky="ew", padx=(0, 8), pady=6, ipady=6)
        self._button(form, "Choose", self._choose_output, neutral=True, width=100).grid(row=6, column=1, sticky="e", padx=(0, 8), pady=(2, 10))

        carrier_ok = DEFAULT_CARRIER.is_file()
        tk.Label(
            form,
            text=f"Carrier: {DEFAULT_CARRIER.name} ({'ready' if carrier_ok else 'MISSING'})",
            font=self._font(9), bg=form["bg"],
            fg=self.colors["success"] if carrier_ok else self.colors["error"],
        ).grid(row=7, column=0, columnspan=2, sticky="w", padx=8, pady=(2, 10))

        self.generate_button = self._button(form, "Generate Sequence CMBX", self._start_generate, width=210)
        self.generate_button.grid(row=8, column=0, columnspan=2, sticky="ew", padx=8, pady=(6, 4))
        self.status_label = tk.Label(form, text="Add methods and a shared Report MD, then generate.", font=self._font(9), bg=form["bg"], fg=self.colors["muted"], anchor="w", justify="left", wraplength=360)
        self.status_label.grid(row=9, column=0, columnspan=2, sticky="w", padx=8, pady=(2, 0))

        log_panel = RoundedPanel(body, fill="#FBFBFC", border=self.colors["border"], radius=12, padding=10, parent_bg=self.colors["window"])
        log_panel.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(4, 0))
        log_panel.body.columnconfigure(0, weight=1)
        self.log_text = tk.Text(log_panel.body, height=7, font=self._font(9), wrap="word", relief="flat", bg="#FBFBFC", fg=self.colors["text"], state="disabled")
        self.log_text.grid(row=0, column=0, sticky="ew")

    def _log(self, message: str) -> None:
        stamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"[{stamp}] {message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _set_busy(self, busy: bool, text: str) -> None:
        self.busy = busy
        self.status_label.configure(text=text)
        self.generate_button.configure(state="disabled" if busy else "normal", cursor="watch" if busy else "hand2")

    def _add_methods(self) -> None:
        if self.busy:
            return
        values = filedialog.askopenfilenames(
            parent=self.root, title="Select Method MD files",
            filetypes=(("Markdown", "*.md *.MD"), ("All files", "*.*")),
        )
        for value in values:
            path = Path(value)
            name = _safe_name(path.stem, f"Injection {len(self.injections) + 1}")
            self.injections.append({"name": name, "md": path})
            self.method_tree.insert("", "end", iid=str(len(self.injections) - 1), values=(name, str(path)))
            self._log(f"Added Method MD: {path.name}")
        if values and not self.sequence_name.get().strip():
            first = Path(values[0]).stem
            self.sequence_name.set(f"{_safe_name(first, 'Sequence')}_Sequence_{datetime.now():%Y%m%d_%H%M%S}")

    def _rename_injection(self) -> None:
        selection = self.method_tree.selection()
        if not selection:
            return
        index = int(selection[0])
        current = str(self.injections[index]["name"])
        dialog = tk.Toplevel(self.root)
        dialog.title("Rename injection")
        dialog.geometry("440x140")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.colors["window"])
        tk.Label(dialog, text="Injection name", font=self._font(10, "bold"), bg=self.colors["window"], fg=self.colors["text"]).pack(anchor="w", padx=20, pady=(18, 6))
        variable = tk.StringVar(value=current)
        tk.Entry(dialog, textvariable=variable, font=self._font(10), relief="solid", bd=1).pack(fill="x", padx=20, pady=(0, 12), ipady=5)

        def save() -> None:
            value = variable.get().strip() or current
            self.injections[index]["name"] = value
            self.method_tree.item(str(index), values=(value, str(self.injections[index]["md"])))
            self._log(f"Renamed injection to: {value}")
            dialog.destroy()

        self._button(dialog, "Save", save, width=100).pack(anchor="e", padx=20, pady=(0, 14))

    def _remove_selected(self) -> None:
        if self.busy:
            return
        selection = self.method_tree.selection()
        for item in sorted(selection, key=int, reverse=True):
            index = int(item)
            self.method_tree.delete(item)
            self.injections.pop(index)
            self._reindex_tree()

    def _clear_injections(self) -> None:
        if self.busy:
            return
        self.method_tree.delete(*self.method_tree.get_children())
        self.injections.clear()
        self._log("Injection list cleared.")

    def _reindex_tree(self) -> None:
        for index, row in enumerate(self.injections):
            self.method_tree.item(str(index), values=(row["name"], str(row["md"])))

    def _choose_report_md(self) -> None:
        value = filedialog.askopenfilename(
            parent=self.root, title="Select shared Report MD",
            filetypes=(("Markdown", "*.md *.MD"), ("All files", "*.*")),
        )
        if value:
            self.report_md.set(value)
            self._log(f"Shared Report MD selected: {Path(value).name}")

    def _choose_output(self) -> None:
        value = filedialog.askdirectory(parent=self.root, title="Select generation history folder", initialdir=self.output_root.get())
        if value:
            self.output_root.set(value)

    def _start_generate(self) -> None:
        if self.busy:
            return
        rows = [dict(row) for row in self.injections]
        if not rows:
            messagebox.showwarning("Sequence Generation", "Add at least one Method MD.", parent=self.root)
            return
        report_value = self.report_md.get().strip()
        if not report_value:
            messagebox.showwarning("Sequence Generation", "Choose the shared Report MD.", parent=self.root)
            return
        if not self.sequence_name.get().strip():
            messagebox.showwarning("Sequence Generation", "Enter a sequence name.", parent=self.root)
            return
        if not DEFAULT_CARRIER.is_file():
            messagebox.showerror("Sequence Generation", f"Sequence carrier is missing:\n{DEFAULT_CARRIER}", parent=self.root)
            return
        for row in rows:
            md = Path(str(row["md"]))
            if not md.is_file():
                messagebox.showerror("Sequence Generation", f"Method MD not found:\n{md}", parent=self.root)
                return
        report_md = Path(report_value)
        if not report_md.is_file():
            messagebox.showerror("Sequence Generation", f"Report MD not found:\n{report_md}", parent=self.root)
            return
        self._set_busy(True, "Compiling methods and report, then binding the Sequence...")
        self._log("Sequence generation started.")
        threading.Thread(
            target=self._generation_worker,
            args=(rows, report_md, self.sequence_name.get().strip(), self.cm_version.get(), Path(self.output_root.get().strip() or DEFAULT_PROJECT_ROOT)),
            daemon=True,
        ).start()

    def _generation_worker(
        self,
        rows: list[dict[str, object]],
        report_md: Path,
        sequence_name: str,
        target_version: str,
        output_root: Path,
    ) -> None:
        try:
            work = output_root / "sequence_components"
            work.mkdir(parents=True, exist_ok=True)
            generated_methods: list[Path] = []
            method_names: list[str] = []
            injection_names: list[str] = []
            for index, row in enumerate(rows, 1):
                md = Path(str(row["md"]))
                injection_name = str(row["name"] or f"Injection {index}")
                method_name = _safe_name(Path(str(row["md"])).stem, f"METHOD_{index}")
                self._log(f"Compiling Method {index}/{len(rows)}: {md.name}")
                checked = preflight_asset("method", md)
                if not checked.ready:
                    raise ValueError(
                        f"Method MD preflight failed for {md.name}: " + "; ".join(checked.errors[:3])
                    )
                generated = generate_asset(AssetGenerationRequest(
                    asset_type="method",
                    asset_name=method_name,
                    family="TCC",
                    intent=f"Sequence {sequence_name} / {injection_name}",
                    target_cm_version=target_version,
                    source_md=md,
                    output_root=work,
                ), checked)
                generated_methods.append(generated.output_cmbx)
                method_names.append(method_name)
                injection_names.append(injection_name)
            self._log("Compiling shared Report Template...")
            report_check = preflight_asset("report", report_md)
            if not report_check.ready:
                raise ValueError(
                    f"Report MD preflight failed: " + "; ".join(report_check.errors[:3])
                )
            report_name = str(report_check.report_spec.template_name or _safe_name(report_md.stem, "SHARED_REPORT"))
            generated_report = generate_asset(AssetGenerationRequest(
                asset_type="report",
                asset_name=report_name,
                family="TCC",
                intent=f"Shared report for Sequence {sequence_name}",
                target_cm_version=target_version,
                source_md=report_md,
                output_root=work,
            ), report_check)
            output_cmbx = output_root / f"{_safe_name(sequence_name, 'Generated_Sequence')}.cmbx"
            self._log("Writing multi-Injection Sequence DataContract...")
            validation = build_multi_sequence_package(MultiSequencePackageRequest(
                carrier_cmbx=DEFAULT_CARRIER,
                report_cmbx=generated_report.output_cmbx,
                output_cmbx=output_cmbx,
                sequence_name=sequence_name,
                report_name=report_name,
                injections=tuple(
                    SequenceInjectionRequest(
                        injection_name=name,
                        method_cmbx=method_path,
                        method_name=method_name,
                    )
                    for name, method_path, method_name in zip(injection_names, generated_methods, method_names)
                ),
                include_processing_methods=False,
            ))
            if not validation.passed:
                raise ValueError("Sequence validation failed: " + "; ".join(validation.errors))
            self.root.after(0, lambda v=validation, p=output_cmbx: self._finish_generation(v, p))
        except Exception as exc:
            self.root.after(0, lambda error=exc: self._task_failed(error))

    def _finish_generation(self, validation, output_cmbx: Path) -> None:
        self.result_path = output_cmbx
        self._set_busy(False, f"Generated: {output_cmbx}")
        self._log(f"Sequence CMBX generated: {output_cmbx}")
        self._log(f"Injections: {', '.join(validation.injection_names)}")
        self._log(f"Instrument methods: {', '.join(validation.instrument_methods)}")
        self._log(f"Report template: {validation.report_template}")
        for warning in validation.warnings:
            self._log(f"WARNING: {warning}")
        messagebox.showinfo(
            "Sequence Generation",
            f"Sequence CMBX generated successfully:\n\n{output_cmbx}\n\n"
            f"Injections: {len(validation.injection_names)}\n"
            f"Methods: {', '.join(validation.instrument_methods)}\n"
            f"Report: {validation.report_template}",
            parent=self.root,
        )

    def _task_failed(self, error: Exception) -> None:
        self._set_busy(False, f"Sequence generation failed: {error}")
        self._log(f"ERROR - {error}")
        messagebox.showerror("Sequence Generation", str(error), parent=self.root)


def main() -> None:
    enable_dpi_awareness()
    root = tk.Tk()
    window = SequenceGenerationWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
