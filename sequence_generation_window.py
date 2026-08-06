from __future__ import annotations

import os
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
STEPS = ("Add method & report inputs", "Generate sequence")


def _safe_name(value: str, fallback: str = "item") -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._ -]+", "_", Path(value).name).strip(" ._")
    return (cleaned or fallback)[:80]


class SequenceGenerationWindow:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.colors = {
            "bg": "#FFFFFF", "surface": "#FFFFFF", "alt": "#F6F6F7", "border": "#E3E4E7",
            "text": "#222326", "muted": "#7C8087", "primary": "#3598F5", "hover": "#2389EB",
            "soft": "#EAF4FE", "success": "#198754", "warning": "#A85D00", "danger": "#C23934",
        }
        self.injections: list[dict[str, object]] = []
        self.busy = False
        self.result_path: Path | None = None
        self.report_md = tk.StringVar()
        self.sequence_name = tk.StringVar()
        self.cm_version = tk.StringVar(value="7.3")
        self.output_root = tk.StringVar(value=str(DEFAULT_PROJECT_ROOT))
        self.status_var = tk.StringVar(value="Add at least one Method MD and the shared Report MD to begin.")
        self.page: tk.Frame | None = None
        self.workflow_step_bar: tk.Frame | None = None
        self.workflow_hint_label: tk.Label | None = None
        self.workflow_active_step = 0
        self.workflow_targets: dict[int, tuple[tk.Misc, str, int, str]] = {}
        self._setup()
        self._build_shell()
        self.show_inputs()

    def _font(self, size: int, weight: str = "normal") -> tuple[str, int, str]:
        return ("Segoe UI", size, weight)

    def _setup(self) -> None:
        self.root.title("Sequence Generation")
        self.root.geometry("1440x900")
        self.root.minsize(1120, 720)
        self.root.configure(bg=self.colors["bg"])
        try:
            self.root.state("zoomed")
        except tk.TclError:
            pass
        style = ttk.Style(self.root)
        style.configure("Sequence.Treeview", font=self._font(9), rowheight=27, background="#FFFFFF", fieldbackground="#FFFFFF")
        style.configure("Sequence.Treeview.Heading", font=self._font(9, "bold"), background="#F0F1F3")
        style.configure("Sequence.TCombobox", font=self._font(9), padding=5)

    def _button(self, parent: tk.Misc, text: str, command, *, neutral: bool = False, width: int = 145) -> RoundedButton:
        return RoundedButton(
            parent, text, command, width=width, height=42, radius=9,
            bg=self.colors["surface"] if neutral else self.colors["primary"],
            hover_bg=self.colors["alt"] if neutral else self.colors["hover"],
            fg=self.colors["text"] if neutral else "#FFFFFF",
            border=self.colors["border"] if neutral else self.colors["primary"],
            parent_bg=str(parent.cget("bg")), font=self._font(9, "bold"),
        )

    def _build_shell(self) -> None:
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        top = tk.Frame(self.root, bg=self.colors["surface"], height=76, highlightthickness=1, highlightbackground=self.colors["border"])
        top.grid(row=0, column=0, sticky="ew")
        top.grid_propagate(False)
        top.columnconfigure(1, weight=1)
        tk.Label(top, text="Sequence Generation", font=self._font(19, "bold"), bg=self.colors["surface"], fg=self.colors["text"]).grid(row=0, column=0, sticky="w", padx=(28, 14), pady=(14, 2))
        self.scope_label = tk.Label(
            top,
            text=f"Carrier: {DEFAULT_CARRIER.name} ({'ready' if DEFAULT_CARRIER.is_file() else 'MISSING'})",
            font=self._font(9), bg=self.colors["surface"], fg=self.colors["success"] if DEFAULT_CARRIER.is_file() else self.colors["danger"],
        )
        self.scope_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=28, pady=(0, 12))
        self._button(top, "Open output folder", self._open_output_folder, neutral=True, width=150).grid(row=0, column=2, rowspan=2, padx=(8, 28), pady=16)

        self.content = tk.Frame(self.root, bg=self.colors["bg"])
        self.content.grid(row=1, column=0, sticky="nsew")
        self.content.rowconfigure(0, weight=1)
        self.content.columnconfigure(0, weight=1)

        log_shell = tk.Frame(self.root, bg=self.colors["surface"], height=86, highlightthickness=1, highlightbackground=self.colors["border"])
        log_shell.grid(row=2, column=0, sticky="ew")
        log_shell.grid_propagate(False)
        log_shell.columnconfigure(0, weight=1)
        tk.Label(log_shell, text="Progress", font=self._font(8, "bold"), bg=self.colors["surface"], fg=self.colors["muted"]).grid(row=0, column=0, sticky="w", padx=28, pady=(9, 2))
        self.log_text = tk.Text(log_shell, height=2, relief="flat", bd=0, bg=self.colors["surface"], fg=self.colors["muted"], font=self._font(8), wrap="word")
        self.log_text.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 8))
        self._log(self.status_var.get())

    def _new_page(self) -> tk.Frame:
        for child in self.content.winfo_children():
            child.destroy()
        page = tk.Frame(self.content, bg=self.colors["bg"])
        page.grid(row=0, column=0, sticky="nsew", padx=32, pady=24)
        page.rowconfigure(3, weight=1)
        page.columnconfigure(0, weight=1)
        self.page = page
        self.workflow_targets = {}
        return page

    def _heading(self, page: tk.Frame, title: str, description: str, steps: tuple[str, ...], active: int) -> None:
        tk.Label(page, text=title, font=self._font(20, "bold"), bg=self.colors["bg"], fg=self.colors["text"]).grid(row=0, column=0, sticky="w")
        tk.Label(page, text=description, font=self._font(10), bg=self.colors["bg"], fg=self.colors["muted"], wraplength=1050, justify="left").grid(row=1, column=0, sticky="w", pady=(5, 14))
        guide = tk.Frame(page, bg=self.colors["bg"])
        guide.grid(row=2, column=0, sticky="ew", pady=(0, 16))
        guide.columnconfigure(0, weight=1)
        self.workflow_step_bar = tk.Frame(guide, bg=self.colors["bg"])
        self.workflow_step_bar.grid(row=0, column=0, sticky="w")
        self.workflow_hint_label = tk.Label(
            guide, text="", font=self._font(9, "bold"), bg=self.colors["soft"],
            fg=self.colors["primary"], anchor="w", justify="left", padx=12, pady=8,
        )
        self.workflow_hint_label.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        self.workflow_active_step = max(0, min(active, len(steps) - 1))
        self._render_workflow_stepper()

    def _render_workflow_stepper(self) -> None:
        bar = self.workflow_step_bar
        if bar is None or not bar.winfo_exists():
            return
        for child in bar.winfo_children():
            child.destroy()
        for index, label in enumerate(STEPS):
            active = self.workflow_active_step
            done = index < active
            current = index == active
            color = self.colors["success"] if done else self.colors["primary"] if current else self.colors["muted"]
            tk.Label(bar, text=str(index + 1), width=3, font=self._font(9, "bold"), bg=color if done or current else self.colors["alt"], fg="#FFFFFF" if done or current else color).pack(side="left")
            tk.Label(bar, text=label, font=self._font(9, "bold" if current else "normal"), bg=self.colors["bg"], fg=color).pack(side="left", padx=(7, 14))
            if index < len(STEPS) - 1:
                tk.Frame(bar, width=32, height=1, bg=self.colors["border"]).pack(side="left", padx=(0, 14))

    def _register_workflow_target(self, step: int, widget: tk.Misc, instruction: str) -> None:
        try:
            original_thickness = int(widget.cget("highlightthickness"))
            original_color = str(widget.cget("highlightbackground"))
        except (tk.TclError, ValueError):
            original_thickness, original_color = 0, self.colors["border"]
        self.workflow_targets[step] = (widget, instruction, original_thickness, original_color)
        self._apply_workflow_guidance()

    def _set_workflow_step(self, step: int) -> None:
        self.workflow_active_step = max(0, min(step, len(STEPS) - 1))
        self._render_workflow_stepper()
        self._apply_workflow_guidance()

    def _apply_workflow_guidance(self) -> None:
        active_target = None
        for index, target in self.workflow_targets.items():
            widget, _instruction, thickness, color = target
            if not widget.winfo_exists():
                continue
            try:
                if index == self.workflow_active_step:
                    widget.configure(highlightthickness=2, highlightbackground=self.colors["primary"], highlightcolor=self.colors["primary"])
                    active_target = target
                else:
                    widget.configure(highlightthickness=thickness, highlightbackground=color)
            except tk.TclError:
                continue
        hint = self.workflow_hint_label
        if hint is not None and hint.winfo_exists():
            label = STEPS[self.workflow_active_step]
            instruction = active_target[1] if active_target is not None else "Complete the highlighted operation below."
            hint.configure(text=f"Step {self.workflow_active_step + 1}: {label}  |  {instruction}")

    def show_inputs(self) -> None:
        page = self._new_page()
        self._heading(page, "Assemble sequence inputs", "Add one or more Method MDs and one shared Report MD. Each Method MD is a reusable injection contract.", STEPS, 0)
        page.rowconfigure(3, weight=1)
        page.columnconfigure(0, weight=3)
        page.columnconfigure(1, weight=2)

        left = RoundedPanel(page, fill=self.colors["alt"], border=self.colors["border"], radius=12, padding=12, parent_bg=self.colors["bg"])
        left.grid(row=3, column=0, sticky="nsew", padx=(0, 10), pady=6)
        left.body.columnconfigure(0, weight=1)
        left.body.rowconfigure(1, weight=1)
        tk.Label(left.body, text="1. Injection methods", font=self._font(13, "bold"), bg=left.body["bg"], fg=self.colors["text"]).grid(row=0, column=0, sticky="w", padx=10, pady=(8, 6))
        tree_frame = tk.Frame(left.body, bg=self.colors["surface"])
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 6))
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        self.method_tree = ttk.Treeview(
            tree_frame, columns=("injection", "md"), show="headings", selectmode="extended",
            style="Sequence.Treeview",
        )
        self.method_tree.heading("injection", text="Injection name")
        self.method_tree.heading("md", text="Method MD")
        self.method_tree.column("injection", width=170, minwidth=120, stretch=False)
        self.method_tree.column("md", width=430, minwidth=220, stretch=True)
        ybar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.method_tree.yview)
        xbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.method_tree.xview)
        self.method_tree.configure(yscrollcommand=ybar.set, xscrollcommand=xbar.set)
        self.method_tree.grid(row=0, column=0, sticky="nsew")
        ybar.grid(row=0, column=1, sticky="ns")
        xbar.grid(row=1, column=0, sticky="ew")
        tree_actions = tk.Frame(left.body, bg=left.body["bg"])
        tree_actions.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        self._button(tree_actions, "Add Method MD(s)", self._add_methods, width=150).pack(side="left")
        self._button(tree_actions, "Rename", self._rename_injection, neutral=True, width=100).pack(side="left", padx=8)
        self._button(tree_actions, "Remove", self._remove_selected, neutral=True, width=100).pack(side="left")
        self._button(tree_actions, "Clear", self._clear_injections, neutral=True, width=90).pack(side="right")
        self._register_workflow_target(0, self.method_tree, "Add at least one Method MD, then choose the shared Report MD.")

        right = RoundedPanel(page, fill=self.colors["alt"], border=self.colors["border"], radius=12, padding=12, parent_bg=self.colors["bg"])
        right.grid(row=3, column=1, sticky="nsew", padx=(10, 0), pady=6)
        form = right.body
        form.columnconfigure(1, weight=1)
        tk.Label(form, text="2. Shared Report MD", font=self._font(13, "bold"), bg=form["bg"], fg=self.colors["text"]).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(8, 8))
        tk.Entry(form, textvariable=self.report_md, font=self._font(9), relief="flat", highlightthickness=1, highlightbackground=self.colors["border"], bg=self.colors["surface"]).grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 6), ipady=7)
        self._button(form, "Choose Report MD", self._choose_report_md, neutral=True, width=170).grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 14))

        tk.Label(form, text="3. Sequence settings", font=self._font(13, "bold"), bg=form["bg"], fg=self.colors["text"]).grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=(4, 8))
        tk.Label(form, text="Sequence name", font=self._font(9, "bold"), bg=form["bg"], fg=self.colors["muted"]).grid(row=4, column=0, sticky="w", padx=10, pady=6)
        tk.Entry(form, textvariable=self.sequence_name, font=self._font(9), relief="flat", highlightthickness=1, highlightbackground=self.colors["border"], bg=self.colors["surface"]).grid(row=4, column=1, sticky="ew", padx=(0, 10), pady=6, ipady=7)
        tk.Label(form, text="CM target", font=self._font(9, "bold"), bg=form["bg"], fg=self.colors["muted"]).grid(row=5, column=0, sticky="w", padx=10, pady=6)
        ttk.Combobox(form, textvariable=self.cm_version, values=("7.3", "7.2 compatible"), state="readonly", style="Sequence.TCombobox").grid(row=5, column=1, sticky="w", padx=(0, 10), pady=6)
        tk.Label(form, text="Output folder", font=self._font(9, "bold"), bg=form["bg"], fg=self.colors["muted"]).grid(row=6, column=0, sticky="w", padx=10, pady=6)
        tk.Entry(form, textvariable=self.output_root, font=self._font(9), relief="flat", highlightthickness=1, highlightbackground=self.colors["border"], bg=self.colors["surface"]).grid(row=6, column=1, sticky="ew", padx=(0, 10), pady=6, ipady=7)
        self._button(form, "Choose", self._choose_output, neutral=True, width=100).grid(row=7, column=1, sticky="e", padx=(0, 10), pady=(2, 6))

        footer = tk.Frame(page, bg=self.colors["bg"])
        footer.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(14, 0))
        self._button(footer, "Continue", self._go_to_generate, width=150).pack(side="right")
        self._log("Sequence workflow opened. Add Method MDs and a shared Report MD.")

    def show_generate(self) -> None:
        page = self._new_page()
        self._heading(page, "Generate the sequence", "Review the assembled inputs, then build the multi-Injection Sequence CMBX.", STEPS, 1)
        panel = RoundedPanel(page, fill=self.colors["alt"], border=self.colors["border"], radius=12, padding=14, parent_bg=self.colors["bg"])
        panel.grid(row=3, column=0, sticky="nsew", pady=6)
        body = panel.body
        body.columnconfigure(1, weight=1)
        rows = [
            ("Asset type", "Sequence CMBX"),
            ("Sequence name", self.sequence_name.get().strip() or "(not set)"),
            ("Injections", f"{len(self.injections)} method(s): {', '.join(str(row['name']) for row in self.injections[:3])}{' ...' if len(self.injections) > 3 else ''}"),
            ("Shared Report MD", self.report_md.get().strip() or "(not set)"),
            ("CM target", self.cm_version.get()),
            ("Output folder", self.output_root.get().strip() or str(DEFAULT_PROJECT_ROOT)),
        ]
        for row, (label, value) in enumerate(rows, start=1):
            tk.Label(body, text=label, font=self._font(9, "bold"), bg=body["bg"], fg=self.colors["text"], width=16, anchor="w").grid(row=row, column=0, sticky="w", padx=(14, 8), pady=8)
            tk.Label(body, text=value, font=self._font(10), bg=body["bg"], fg=self.colors["muted"], anchor="w", wraplength=820, justify="left").grid(row=row, column=1, sticky="w", padx=8, pady=8)
        result_text = f"A candidate Sequence CMBX will be written here after generation.{chr(10) + str(self.result_path) if self.result_path else ''}"
        self.generation_result = tk.Label(body, text=result_text, font=self._font(10), wraplength=850, justify="left", bg=body["bg"], fg=self.colors["primary"] if self.result_path else self.colors["muted"])
        self.generation_result.grid(row=len(rows) + 2, column=0, columnspan=2, sticky="w", padx=14, pady=(20, 16))
        footer = tk.Frame(page, bg=self.colors["bg"])
        footer.grid(row=4, column=0, sticky="ew", pady=(14, 0))
        self._button(footer, "Back to inputs", self.show_inputs, neutral=True, width=140).pack(side="left")
        self.generate_button = self._button(footer, "Generate Sequence CMBX", self._start_generate, width=210)
        self.generate_button.pack(side="right")
        self._register_workflow_target(1, self.generate_button, "Review the summary, then generate the Sequence CMBX.")

    def _go_to_generate(self) -> None:
        if self.busy:
            return
        if not self.injections:
            messagebox.showwarning("Sequence Generation", "Add at least one Method MD.", parent=self.root)
            return
        if not self.report_md.get().strip():
            messagebox.showwarning("Sequence Generation", "Choose the shared Report MD.", parent=self.root)
            return
        if not self.sequence_name.get().strip():
            messagebox.showwarning("Sequence Generation", "Enter a sequence name.", parent=self.root)
            return
        self.show_generate()

    def _log(self, message: str) -> None:
        self.status_var.set(message)
        if not hasattr(self, "log_text"):
            return
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message.rstrip() + "\n")
        lines = int(self.log_text.index("end-1c").split(".")[0])
        if lines > 120:
            self.log_text.delete("1.0", f"{lines - 100}.0")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _set_busy(self, busy: bool, text: str) -> None:
        self.busy = busy
        self.status_var.set(text)
        if hasattr(self, "generate_button") and self.generate_button.winfo_exists():
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
        self.scope_label.configure(text=f"Carrier: {DEFAULT_CARRIER.name} · {len(self.injections)} injection method(s) ready")

    def _rename_injection(self) -> None:
        selection = self.method_tree.selection()
        if not selection:
            return
        index = int(selection[0])
        current = str(self.injections[index]["name"])
        dialog = tk.Toplevel(self.root)
        dialog.title("Rename injection")
        dialog.geometry("440x150")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.colors["bg"])
        tk.Label(dialog, text="Injection name", font=self._font(10, "bold"), bg=self.colors["bg"], fg=self.colors["text"]).pack(anchor="w", padx=22, pady=(20, 6))
        variable = tk.StringVar(value=current)
        tk.Entry(dialog, textvariable=variable, font=self._font(10), relief="solid", bd=1, highlightthickness=1, highlightbackground=self.colors["border"]).pack(fill="x", padx=22, pady=(0, 14), ipady=6)
        actions = tk.Frame(dialog, bg=self.colors["bg"])
        actions.pack(fill="x", padx=22, pady=(0, 16))

        def save() -> None:
            value = variable.get().strip() or current
            self.injections[index]["name"] = value
            self.method_tree.item(str(index), values=(value, str(self.injections[index]["md"])))
            self._log(f"Renamed injection to: {value}")
            dialog.destroy()

        self._button(actions, "Cancel", dialog.destroy, neutral=True, width=100).pack(side="right", padx=(8, 0))
        self._button(actions, "Save", save, width=100).pack(side="right")

    def _remove_selected(self) -> None:
        if self.busy:
            return
        selection = self.method_tree.selection()
        for item in sorted(selection, key=int, reverse=True):
            index = int(item)
            self.method_tree.delete(item)
            self.injections.pop(index)
            self._reindex_tree()
        self.scope_label.configure(text=f"Carrier: {DEFAULT_CARRIER.name} · {len(self.injections)} injection method(s) ready")

    def _clear_injections(self) -> None:
        if self.busy:
            return
        self.method_tree.delete(*self.method_tree.get_children())
        self.injections.clear()
        self.scope_label.configure(text=f"Carrier: {DEFAULT_CARRIER.name} · 0 injection methods")
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

    def _open_output_folder(self) -> None:
        target = Path(self.output_root.get().strip() or DEFAULT_PROJECT_ROOT)
        if self.result_path is not None:
            target = self.result_path
        target.mkdir(parents=True, exist_ok=True)
        if os.name == "nt":
            os.startfile(target)  # type: ignore[attr-defined]

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
        if self.page is not None and self.current_step_is_generate():
            self.show_generate()
        messagebox.showinfo(
            "Sequence Generation",
            f"Sequence CMBX generated successfully:\n\n{output_cmbx}\n\n"
            f"Injections: {len(validation.injection_names)}\n"
            f"Methods: {', '.join(validation.instrument_methods)}\n"
            f"Report: {validation.report_template}",
            parent=self.root,
        )

    def current_step_is_generate(self) -> bool:
        return self.workflow_active_step == 1

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
