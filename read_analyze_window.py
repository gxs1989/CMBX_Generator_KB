from __future__ import annotations

import argparse
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from business_ui_components import RoundedButton, RoundedPanel, enable_dpi_awareness
from formula_catalog import FormulaCatalogEntry, build_formula_catalog, useful_direct_formula_catalog
from read_analyze_service import (
    ChannelRecord,
    FormulaRecord,
    FormulaScanProgress,
    InjectionRecord,
    IntegrationSettings,
    WorksetPackage,
    adapt_integration_settings,
    channel_records,
    decode_channel_points,
    discover_cmbx_paths,
    evaluate_formula_batch,
    export_channel_records,
    filter_channel_records,
    formula_records,
    integrate_signal,
    injection_records,
    load_workset,
    unique_channel_names,
)


DEFAULT_OUTPUT = Path(r"C:\ProgramData\CMBX Data Explorer Workspace\exports\read_analyze")


class ReadAnalyzeWindow:
    TASKS = {
        "raw": ("Batch Raw Data Export", "Select and export matching raw channels across a multi-CMBX workspace."),
        "plot": ("Chromatograms & Integration", "Compare, zoom and integrate selected channel traces."),
        "formula": ("Direct CM Formula Results", "Batch-evaluate useful or embedded Direct CM formulas."),
    }

    def __init__(self, root: tk.Tk, initial_task: str | None = None):
        self.root = root
        self.colors = {
            "bg": "#FFFFFF", "surface": "#FFFFFF", "alt": "#F6F6F7", "border": "#E3E4E7",
            "text": "#222326", "muted": "#7C8087", "primary": "#3598F5", "hover": "#2389EB",
            "soft": "#EAF4FE", "success": "#198754", "warning": "#A85D00", "danger": "#C23934",
        }
        self.workset: list[WorksetPackage] = []
        self.channels: list[ChannelRecord] = []
        self.injections: list[InjectionRecord] = []
        self.source_paths: list[Path] = []
        self.channel_by_iid: dict[str, ChannelRecord] = {}
        self.injection_by_iid: dict[str, InjectionRecord] = {}
        self.formula_by_iid: dict[str, FormulaRecord] = {}
        self.formulas: list[FormulaRecord] = []
        self.formula_scan_errors: list[tuple[str, str]] = []
        self.formula_scan_progress: FormulaScanProgress | None = None
        self.formula_scan_active = False
        self.formula_scan_complete = False
        self.formula_scan_failure = ""
        self.formula_scan_generation = 0
        self.formula_scan_logged_percent = -10
        self.formula_scan_started_at: float | None = None
        self.formula_library_entries: tuple[FormulaCatalogEntry, ...] = ()
        self.formula_library_active = False
        self.formula_library_failure = ""
        self.plot_series: list[tuple[ChannelRecord, list]] = []
        self.peak_results = []
        self.plot_bounds: tuple[float, float, float, float] | None = None
        self.plot_view: tuple[float, float, float, float] | None = None
        self._pan_start: tuple[int, int, tuple[float, float, float, float]] | None = None
        self.plot_view_history: list[tuple[float, float, float, float]] = []
        self.plot_space_down = False
        self._plot_drag_mode: str | None = None
        self._plot_drag_origin: tuple[int, int, tuple[float, float, float, float]] | None = None
        self._plot_zoom_rect: int | None = None
        self._plot_redraw_job: str | None = None
        self.page: tk.Frame | None = None
        self.workflow_steps: tuple[str, ...] = ()
        self.workflow_active_step = 0
        self.workflow_step_bar: tk.Frame | None = None
        self.workflow_hint_label: tk.Label | None = None
        self.workflow_targets: dict[int, tuple[tk.Misc, str, int, str]] = {}
        self.selected_task = initial_task if initial_task in self.TASKS else None
        self.status_var = tk.StringVar(value="Start by adding one or more CMBX files or folders.")
        self._setup()
        self._build_shell()
        self._start_formula_library_load()
        if self.selected_task:
            self.show_workset()
        else:
            self.show_task_selection()

    def _font(self, size: int, weight: str = "normal"):
        return ("Segoe UI", size, weight)

    def _setup(self) -> None:
        self.root.title("Read & Analyze CMBX")
        self.root.geometry("1500x920")
        self.root.minsize(1120, 720)
        self.root.configure(bg=self.colors["bg"])
        try:
            self.root.state("zoomed")
        except tk.TclError:
            pass
        style = ttk.Style(self.root)
        style.configure("Analyze.Treeview", font=self._font(9), rowheight=27, background="#FFFFFF", fieldbackground="#FFFFFF")
        style.configure("Analyze.Treeview.Heading", font=self._font(9, "bold"), background="#F0F1F3")
        style.configure("Analyze.TCombobox", font=self._font(9), padding=5)

    def _build_shell(self) -> None:
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        top = tk.Frame(self.root, bg=self.colors["surface"], height=76, highlightthickness=1, highlightbackground=self.colors["border"])
        top.grid(row=0, column=0, sticky="ew")
        top.grid_propagate(False)
        top.columnconfigure(1, weight=1)
        tk.Label(top, text="Chromatograms & Results", font=self._font(19, "bold"), bg=self.colors["surface"], fg=self.colors["text"]).grid(row=0, column=0, sticky="w", padx=(28, 14), pady=(14, 2))
        self.scope_label = tk.Label(top, text="No workset loaded", font=self._font(9), bg=self.colors["surface"], fg=self.colors["muted"])
        self.scope_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=28, pady=(0, 12))
        self._button(top, "Change task", self.show_task_selection, neutral=True, width=118).grid(row=0, column=2, rowspan=2, padx=(8, 0), pady=16)
        self._button(top, "CMBX workspace", self.show_workset, neutral=True, width=145).grid(row=0, column=3, rowspan=2, padx=(8, 28), pady=16)
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

    def _button(self, parent, text, command, *, neutral=False, width=145):
        return RoundedButton(
            parent, text, command, width=width, height=42, radius=9,
            bg=self.colors["surface"] if neutral else self.colors["primary"],
            hover_bg=self.colors["alt"] if neutral else self.colors["hover"],
            fg=self.colors["text"] if neutral else "#FFFFFF",
            border=self.colors["border"] if neutral else self.colors["primary"],
            parent_bg=str(parent.cget("bg")), font=self._font(9, "bold"),
        )

    def _new_page(self) -> tk.Frame:
        if self._plot_redraw_job is not None:
            try:
                self.root.after_cancel(self._plot_redraw_job)
            except tk.TclError:
                pass
            self._plot_redraw_job = None
        for child in self.content.winfo_children():
            child.destroy()
        page = tk.Frame(self.content, bg=self.colors["bg"])
        page.grid(row=0, column=0, sticky="nsew", padx=32, pady=24)
        page.rowconfigure(3, weight=1)
        page.columnconfigure(0, weight=1)
        self.page = page
        self.workflow_steps = ()
        self.workflow_active_step = 0
        self.workflow_step_bar = None
        self.workflow_hint_label = None
        self.workflow_targets = {}
        return page

    def _heading(self, page, title: str, description: str, steps: tuple[str, ...], active: int) -> None:
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
        self.workflow_steps = steps
        self.workflow_active_step = max(0, min(active, len(steps) - 1))
        self._render_workflow_stepper()

    def _render_workflow_stepper(self) -> None:
        bar = self.workflow_step_bar
        if bar is None or not bar.winfo_exists():
            return
        for child in bar.winfo_children():
            child.destroy()
        for index, label in enumerate(self.workflow_steps):
            active = self.workflow_active_step
            done = index < active
            current = index == active
            color = self.colors["success"] if done else self.colors["primary"] if current else self.colors["muted"]
            tk.Label(bar, text=str(index + 1), width=3, font=self._font(9, "bold"), bg=color if done or current else self.colors["alt"], fg="#FFFFFF" if done or current else color).pack(side="left")
            tk.Label(bar, text=label, font=self._font(9, "bold" if current else "normal"), bg=self.colors["bg"], fg=color).pack(side="left", padx=(7, 14))
            if index < len(self.workflow_steps) - 1:
                tk.Frame(bar, width=32, height=1, bg=self.colors["border"]).pack(side="left", padx=(0, 14))

    def _register_workflow_target(self, step: int, widget: tk.Misc, instruction: str) -> None:
        try:
            original_thickness = int(widget.cget("highlightthickness"))
            original_color = str(widget.cget("highlightbackground"))
        except (tk.TclError, ValueError):
            original_thickness, original_color = 0, self.colors["border"]
        self.workflow_targets[step] = (widget, instruction, original_thickness, original_color)
        self._apply_workflow_guidance(move_focus=False)

    def _set_workflow_step(self, step: int, *, move_focus: bool = True) -> None:
        if not self.workflow_steps:
            return
        self.workflow_active_step = max(0, min(step, len(self.workflow_steps) - 1))
        self._render_workflow_stepper()
        self._apply_workflow_guidance(move_focus=move_focus)

    def _apply_workflow_guidance(self, *, move_focus: bool) -> None:
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
            label = self.workflow_steps[self.workflow_active_step] if self.workflow_steps else ""
            instruction = active_target[1] if active_target is not None else "Complete the highlighted operation below."
            hint.configure(text=f"Step {self.workflow_active_step + 1}: {label}  |  {instruction}")
        if move_focus and active_target is not None:
            widget = active_target[0]
            self.root.after_idle(lambda item=widget: item.focus_set() if item.winfo_exists() else None)

    def _table(self, parent, columns, headings, *, selectmode="extended", tree=False):
        frame = tk.Frame(parent, bg=self.colors["surface"])
        frame.rowconfigure(0, weight=1); frame.columnconfigure(0, weight=1)
        table = ttk.Treeview(frame, columns=columns, show="tree headings" if tree else "headings", style="Analyze.Treeview", selectmode=selectmode)
        table.grid(row=0, column=0, sticky="nsew")
        for column in columns:
            table.heading(column, text=headings.get(column, column))
            table.column(column, width=headings.get(f"{column}_width", 150), minwidth=70, stretch=True)
        if tree:
            table.heading("#0", text=headings.get("#0", "Name")); table.column("#0", width=300, minwidth=180)
        ybar = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
        xbar = ttk.Scrollbar(frame, orient="horizontal", command=table.xview)
        table.configure(yscrollcommand=ybar.set, xscrollcommand=xbar.set)
        ybar.grid(row=0, column=1, sticky="ns"); xbar.grid(row=1, column=0, sticky="ew")
        return frame, table

    def _log(self, message: str) -> None:
        self.status_var.set(message)
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message.rstrip() + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _background(self, label: str, worker, done) -> None:
        self._log(label)
        def run():
            try:
                result = worker()
                self.root.after(0, lambda: done(result, None))
            except Exception as exc:
                self.root.after(0, lambda: done(None, exc))
        threading.Thread(target=run, daemon=True).start()

    def _reset_formula_scan(self) -> None:
        self.formula_scan_generation += 1
        self.formulas = []
        self.formula_by_iid.clear()
        self.formula_scan_errors = []
        self.formula_scan_progress = None
        self.formula_scan_active = False
        self.formula_scan_complete = False
        self.formula_scan_failure = ""
        self.formula_scan_logged_percent = -10
        self.formula_scan_started_at = None

    def _start_formula_library_load(self) -> None:
        if self.formula_library_active or self.formula_library_entries:
            return
        self.formula_library_active = True
        try:
            catalog = build_formula_catalog(Path(__file__).resolve().parent / "docs")
            result, error = useful_direct_formula_catalog(catalog), None
        except Exception as exc:
            result, error = (), exc
        self._formula_library_done(result, error)

    def _formula_library_done(self, result, error) -> None:
        self.formula_library_active = False
        if error is not None:
            self.formula_library_failure = str(error)
            self._log(f"Useful Direct CM formula library failed: {error}")
        else:
            self.formula_library_entries = tuple(result)
            self._log(f"Useful Direct CM formula library ready: {len(self.formula_library_entries)} formula(s).")
            if hasattr(self, "formula_inventory_table") and self.formula_inventory_table.winfo_exists():
                self._fill_formula_inventory()

    def _start_formula_prefetch(self, expected_generation: int | None = None) -> None:
        if expected_generation is not None and expected_generation != self.formula_scan_generation:
            return
        if not self.workset or self.formula_scan_active or self.formula_scan_complete:
            self._refresh_formula_scan_widgets()
            return
        generation = self.formula_scan_generation
        self.formula_scan_active = True
        self.formula_scan_started_at = time.monotonic()
        self.formula_scan_failure = ""
        self._log("Direct CM inventory prefetch started in the background.")
        self._refresh_formula_scan_widgets()
        self.root.after(1000, lambda: self._formula_scan_heartbeat(generation))

        def report_progress(progress: FormulaScanProgress) -> None:
            try:
                self.root.after(0, lambda item=progress: self._formula_scan_progressed(generation, item))
            except (tk.TclError, RuntimeError):
                pass

        def run() -> None:
            try:
                result = formula_records(self.workset, include_formulaone=False, progress=report_progress)
                error = None
            except Exception as exc:
                result, error = None, exc
            try:
                self.root.after(0, lambda value=result, exc=error: self._formula_prefetch_done(generation, value, exc))
            except (tk.TclError, RuntimeError):
                pass

        threading.Thread(target=run, daemon=True).start()

    def _formula_scan_heartbeat(self, generation: int) -> None:
        if generation != self.formula_scan_generation or not self.formula_scan_active:
            return
        self._refresh_formula_scan_widgets()
        self.root.after(1000, lambda: self._formula_scan_heartbeat(generation))

    def _formula_scan_progressed(self, generation: int, progress: FormulaScanProgress) -> None:
        if generation != self.formula_scan_generation:
            return
        self.formula_scan_progress = progress
        percent = int(progress.completed * 100 / max(progress.total, 1))
        if percent >= self.formula_scan_logged_percent + 10 or progress.completed == progress.total:
            self.formula_scan_logged_percent = percent
            self._log(self._formula_scan_status())
        self._refresh_formula_scan_widgets()

    def _formula_prefetch_done(self, generation: int, result, error) -> None:
        if generation != self.formula_scan_generation:
            return
        self.formula_scan_active = False
        self.formula_scan_complete = True
        if error is not None:
            self.formula_scan_failure = str(error)
            self._log(f"Direct CM inventory prefetch failed: {error}")
        else:
            self.formulas, self.formula_scan_errors = result
            self._log(f"Direct CM inventory cached: {len(self.formulas)} formula(s), {len(self.formula_scan_errors)} source warning(s).")
            if hasattr(self, "formula_inventory_table") and self.formula_inventory_table.winfo_exists():
                self._fill_formula_inventory()
        self._refresh_formula_scan_widgets()

    @staticmethod
    def _formula_eta(seconds: float | None) -> str:
        if seconds is None:
            return "estimating..."
        if seconds < 1:
            return "<1 s"
        if seconds < 60:
            return f"~{int(round(seconds))} s"
        minutes, remainder = divmod(int(round(seconds)), 60)
        return f"~{minutes} min {remainder:02d} s"

    def _formula_scan_status(self) -> str:
        if self.formula_scan_failure:
            return f"Direct CM scan failed: {self.formula_scan_failure}"
        progress = self.formula_scan_progress
        if self.formula_scan_complete:
            return f"Ready in cache: {len(self.formulas)} Direct CM formula(s)"
        if progress is not None:
            percent = int(progress.completed * 100 / max(progress.total, 1))
            elapsed = time.monotonic() - self.formula_scan_started_at if self.formula_scan_started_at is not None else progress.elapsed_s
            return (
                f"Scanning {progress.completed}/{progress.total} reports ({percent}%) | "
                f"{progress.formulas_found} formulas | elapsed {self._formula_eta(elapsed)} | "
                f"ETA {self._formula_eta(progress.eta_s)} | {progress.report}"
            )
        if self.formula_scan_active:
            return "Discovering Direct CM report sources..."
        return "Direct CM inventory will be prepared automatically"

    def _refresh_formula_scan_widgets(self) -> None:
        status = self._formula_scan_status()
        label = getattr(self, "formula_task_status_label", None)
        if label is not None and label.winfo_exists():
            label.configure(text=status)
        scan_label = getattr(self, "formula_scan_label", None)
        if scan_label is not None and scan_label.winfo_exists():
            scan_label.configure(text=status)
        bar = getattr(self, "formula_progress_bar", None)
        if bar is not None and bar.winfo_exists():
            progress = self.formula_scan_progress
            total = max(progress.total if progress is not None else 1, 1)
            completed = progress.completed if progress is not None else (total if self.formula_scan_complete else 0)
            bar.configure(maximum=total, value=completed)

    # Workset
    def show_workset(self) -> None:
        if not self.selected_task:
            self.show_task_selection()
            return
        page = self._new_page()
        task_title = self.TASKS[self.selected_task][0]
        self._heading(page, f"Choose the CMBX workspace for {task_title}", "Add one or many packages. Header structure is indexed first; raw signal data is decoded only when the selected workflow needs it.", ("Task selected", "Add sources", "Index and open"), 1)
        body = tk.Frame(page, bg=self.colors["bg"]); body.grid(row=3, column=0, sticky="nsew"); body.rowconfigure(1, weight=1); body.columnconfigure(0, weight=1)
        actions = tk.Frame(body, bg=self.colors["bg"]); actions.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        self._button(actions, "Add CMBX", self._add_files).pack(side="left")
        self._button(actions, "Add folder", self._add_folder, neutral=True).pack(side="left", padx=8)
        self._button(actions, "Clear", self._clear_sources, neutral=True, width=100).pack(side="left")
        self._button(actions, "Index CMBX", self._load_sources, width=132).pack(side="right")
        frame, self.workset_table = self._table(body, ("path", "type", "sequences", "injections", "channels"), {
            "path": "CMBX source", "path_width": 560, "type": "Package type", "type_width": 150,
            "sequences": "Sequences", "injections": "Injections", "channels": "Channels",
        })
        frame.grid(row=1, column=0, sticky="nsew")
        self._register_workflow_target(1, actions, "Add one or more CMBX files or folders.")
        self._register_workflow_target(2, frame, "Review the source list, then choose Index CMBX.")
        self._render_sources()

    def _add_files(self) -> None:
        values = filedialog.askopenfilenames(parent=self.root, title="Add CMBX files", filetypes=[("CMBX packages", "*.cmbx")])
        self.source_paths = list(dict.fromkeys([*self.source_paths, *[Path(item) for item in values]]))
        self._render_sources()

    def _add_folder(self) -> None:
        value = filedialog.askdirectory(parent=self.root, title="Add a CMBX folder")
        if value:
            self.source_paths = list(dict.fromkeys([*self.source_paths, *discover_cmbx_paths([value])]))
            self._render_sources()

    def _clear_sources(self) -> None:
        self.source_paths.clear(); self.workset.clear(); self.channels.clear(); self.injections.clear()
        self._reset_formula_scan()
        self._render_sources(); self.scope_label.configure(text="No workset loaded")
        self._set_workflow_step(1 if self.selected_task else 0)

    def _render_sources(self) -> None:
        if not hasattr(self, "workset_table"):
            return
        self.workset_table.delete(*self.workset_table.get_children())
        loaded_by_path = {item.package.path.resolve(): item for item in self.workset}
        for path in self.source_paths:
            item = loaded_by_path.get(path.resolve()) if path.exists() else None
            self.workset_table.insert("", "end", values=(str(path), item.package_type if item else "Waiting", len(item.package.sequences) if item else "", len(item.package.injections) if item else "", len(item.package.channels) if item else ""))
        if self.source_paths and self.workflow_steps and "Add sources" in self.workflow_steps:
            self._set_workflow_step(2)

    def _load_sources(self) -> None:
        paths = discover_cmbx_paths(self.source_paths)
        if not paths:
            messagebox.showwarning("Read & Analyze", "Add at least one CMBX package.", parent=self.root); return
        self._set_workflow_step(2)
        self._background(f"Indexing {len(paths)} CMBX package(s)...", lambda: load_workset(paths), self._loaded)

    def _loaded(self, result, error) -> None:
        if error:
            messagebox.showerror("Read & Analyze", str(error), parent=self.root); self._log(f"Index failed: {error}"); return
        self.workset, errors = result
        self.source_paths = [item.package.path for item in self.workset]
        self.channels = channel_records(self.workset)
        self.injections = injection_records(self.workset)
        self._reset_formula_scan()
        self.scope_label.configure(text=f"{len(self.workset)} package(s) | {len(self.injections)} injection(s) | {len(self.channels)} channel(s)")
        self._log(f"Index ready: {len(self.workset)} package(s), {len(self.injections)} injection(s), {len(self.channels)} channel(s).")
        for path, detail in errors:
            self._log(f"Skipped {path.name}: {detail}")
        self._open_selected_task()
        generation = self.formula_scan_generation
        self.root.after(250, lambda: self._start_formula_prefetch(generation))

    # Task selection
    def show_task_selection(self) -> None:
        page = self._new_page()
        self._heading(page, "Choose a task", "Select the result you need first. The next step asks for the CMBX workspace used by that workflow.", ("Choose task", "Choose CMBX workspace", "Review result"), 0)
        cards = tk.Frame(page, bg=self.colors["bg"]); cards.grid(row=3, column=0, sticky="new")
        tasks = (
            ("raw", "Select package -> sequence -> injection -> channel, or reverse-match every compatible injection."),
            ("plot", "Filter channels from any package, compare traces and integrate with one shared parameter set."),
            ("formula", "Discover useful or embedded Direct CM formulas and batch-preview filtered injection contexts."),
        )
        for index, (task_id, text) in enumerate(tasks):
            title = self.TASKS[task_id][0]
            cards.columnconfigure(index, weight=1, uniform="task")
            shell = RoundedPanel(cards, fill=self.colors["surface"], border=self.colors["border"], radius=12, padding=10, parent_bg=self.colors["bg"], height=240)
            shell.grid(row=0, column=index, sticky="nsew", padx=(0 if index == 0 else 7, 0 if index == 2 else 7))
            shell.body.columnconfigure(0, weight=1)
            shell.body.rowconfigure(1, weight=1)
            tk.Label(shell.body, text=title, font=self._font(13, "bold"), bg=self.colors["surface"], fg=self.colors["text"]).grid(row=0, column=0, sticky="nw", padx=10, pady=(12, 7))
            tk.Label(shell.body, text=text, font=self._font(9), bg=self.colors["surface"], fg=self.colors["muted"], wraplength=310, justify="left").grid(row=1, column=0, sticky="nw", padx=10)
            if index == 2:
                self.formula_task_status_label = tk.Label(shell.body, text=self._formula_scan_status(), font=self._font(8), bg=self.colors["surface"], fg=self.colors["muted"], wraplength=310, justify="left")
                self.formula_task_status_label.grid(row=2, column=0, sticky="sw", padx=10, pady=(8, 0))
            self._button(shell.body, "Choose", lambda value=task_id: self._select_task(value), width=112).grid(row=3, column=0, sticky="sw", padx=10, pady=(10, 10))
        self._register_workflow_target(0, cards, "Choose the result you want before selecting any CMBX files.")

    # Compatibility alias used by workflow back buttons.
    def show_tasks(self) -> None:
        self.show_task_selection()

    def _select_task(self, task_id: str) -> None:
        if task_id not in self.TASKS:
            raise ValueError(f"Unknown analysis task: {task_id}")
        self.selected_task = task_id
        self._log(f"Task selected: {self.TASKS[task_id][0]}.")
        self.show_workset()

    def _open_selected_task(self) -> None:
        if self.selected_task == "raw":
            self.show_raw_export()
        elif self.selected_task == "plot":
            self.show_plot()
        elif self.selected_task == "formula":
            self.show_formula()
        else:
            self.show_task_selection()

    # Raw export
    def _channel_filter_panel(self, parent, callback, prefix: str):
        panel = tk.Frame(parent, bg=self.colors["bg"])
        variables = {}
        definitions = (
            ("package", sorted({row.package.path.name for row in self.channels}, key=str.lower)),
            ("sequence", sorted({row.sequence.name for row in self.channels}, key=str.lower)),
            ("injection", sorted({row.injection.name for row in self.channels}, key=str.lower)),
            ("channel", unique_channel_names(self.channels)),
        )
        for index, (name, values) in enumerate(definitions):
            panel.columnconfigure(index, weight=1)
            cell = tk.Frame(panel, bg=self.colors["bg"]); cell.grid(row=0, column=index, sticky="ew", padx=(0 if index == 0 else 5, 0 if index == 3 else 5))
            tk.Label(cell, text=name.title(), font=self._font(8, "bold"), bg=self.colors["bg"], fg=self.colors["muted"]).pack(anchor="w")
            variable = tk.StringVar(value="All")
            combo = ttk.Combobox(cell, textvariable=variable, values=["All", *values], style="Analyze.TCombobox")
            combo.pack(fill="x", pady=(3, 0))
            combo.bind("<<ComboboxSelected>>", lambda _event: callback())
            combo.bind("<KeyRelease>", lambda event: callback() if event.keysym not in {"Up", "Down", "Left", "Right"} else None)
            variables[name] = variable
        setattr(self, f"{prefix}_filter_vars", variables)
        return panel

    def _filtered_channels(self, prefix: str) -> list[ChannelRecord]:
        variables = getattr(self, f"{prefix}_filter_vars", {})
        def value(name):
            current = variables[name].get().strip() if name in variables else ""
            return "" if current.casefold() == "all" else current
        return filter_channel_records(
            self.channels, package=value("package"), sequence=value("sequence"),
            injection=value("injection"), channel=value("channel"),
        )

    def show_raw_export(self) -> None:
        page = self._new_page()
        self._heading(page, "Batch raw data export", "Choose down the hierarchy or reverse-match a channel across all packages. Parent rows select all channel descendants.", ("Select scope", "Review matches", "Export TSV"), 0)
        body = tk.Frame(page, bg=self.colors["bg"]); body.grid(row=3, column=0, sticky="nsew"); body.rowconfigure(3, weight=1); body.columnconfigure(0, weight=1)
        filterbar = self._channel_filter_panel(body, self._raw_scope_changed, "raw"); filterbar.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        actions = tk.Frame(body, bg=self.colors["bg"]); actions.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        self.raw_match_label = tk.Label(actions, text="", font=self._font(8), bg=self.colors["bg"], fg=self.colors["muted"]); self.raw_match_label.pack(side="left")
        self._button(actions, "Workspace", self.show_workset, neutral=True, width=108).pack(side="right", padx=(8, 0))
        self._button(actions, "Export selected", self._export_selected_raw, width=165).pack(side="right")
        frame, self.raw_tree = self._table(body, ("kind", "detail"), {"#0": "Package / Sequence / Injection / Channel", "kind": "Type", "kind_width": 110, "detail": "Source", "detail_width": 520}, tree=True)
        frame.grid(row=2, column=0, sticky="nsew")
        self.raw_tree.bind("<<TreeviewSelect>>", lambda _event: self._set_workflow_step(2))
        self._register_workflow_target(0, filterbar, "Filter by package, sequence, injection, or channel.")
        self._register_workflow_target(1, frame, "Review the matching hierarchy and select the rows to export.")
        self._register_workflow_target(2, actions, "Choose Export selected and select the destination folder.")
        self._fill_raw_tree()

    def _raw_scope_changed(self) -> None:
        self._fill_raw_tree()
        self._set_workflow_step(1)

    def _fill_raw_tree(self) -> None:
        self.raw_tree.delete(*self.raw_tree.get_children()); self.channel_by_iid.clear()
        records = self._filtered_channels("raw")
        self.raw_match_label.configure(text=f"{len(records)} matching channel context(s)")
        grouped: dict[Path, dict[str, dict[str, list[ChannelRecord]]]] = {}
        for record in records:
            grouped.setdefault(record.package.path, {}).setdefault(record.sequence.id, {}).setdefault(record.injection.id, []).append(record)
        for p_index, (path, sequences) in enumerate(grouped.items()):
            p_iid = f"p{p_index}"; self.raw_tree.insert("", "end", iid=p_iid, text=path.name, values=("Package", str(path)), open=True)
            for s_index, injections in enumerate(sequences.values()):
                first = next(iter(next(iter(injections.values())))); s_iid = f"{p_iid}s{s_index}"
                self.raw_tree.insert(p_iid, "end", iid=s_iid, text=first.sequence.name, values=("Sequence", ""), open=True)
                for i_index, channels in enumerate(injections.values()):
                    i_iid = f"{s_iid}i{i_index}"; self.raw_tree.insert(s_iid, "end", iid=i_iid, text=channels[0].injection.name, values=("Injection", ""), open=True)
                    for c_index, record in enumerate(channels):
                        c_iid = f"{i_iid}c{c_index}"; self.raw_tree.insert(i_iid, "end", iid=c_iid, text=record.channel.name, values=("Channel", record.channel.raw_filename))
                        self.channel_by_iid[c_iid] = record

    def _selected_channel_records(self, table: ttk.Treeview, mapping: dict[str, ChannelRecord]) -> list[ChannelRecord]:
        found: dict[str, ChannelRecord] = {}
        def walk(iid: str):
            if iid in mapping:
                found[mapping[iid].key] = mapping[iid]
            for child in table.get_children(iid):
                walk(child)
        for iid in table.selection():
            walk(iid)
        return list(found.values())

    def _export_selected_raw(self) -> None:
        records = self._selected_channel_records(self.raw_tree, self.channel_by_iid)
        if not records:
            messagebox.showwarning("Raw export", "Select one or more hierarchy rows.", parent=self.root); return
        self._set_workflow_step(2)
        DEFAULT_OUTPUT.mkdir(parents=True, exist_ok=True)
        destination = filedialog.askdirectory(parent=self.root, title="Choose raw-data output folder", initialdir=str(DEFAULT_OUTPUT))
        if not destination:
            return
        self._background(f"Exporting {len(records)} channel(s)...", lambda: export_channel_records(records, destination), self._raw_exported)

    def _raw_exported(self, result, error) -> None:
        if error:
            self._log(f"Raw export failed: {error}"); messagebox.showerror("Raw export", str(error), parent=self.root); return
        paths, errors = result
        self._log(f"Raw export complete: {len(paths)} file(s), {len(errors)} error(s).")
        messagebox.showinfo("Raw export", f"Exported {len(paths)} channel file(s).\nErrors: {len(errors)}", parent=self.root)

    # Plot
    def show_plot(self) -> None:
        page = self._new_page()
        self._heading(page, "Chromatograms & Integration", "Filter at package, sequence, injection and channel levels; display chromatograms overlaid or separately, then apply one shared external Cobra-inspired integration parameter set.", ("Find channels", "Load traces", "View and integrate"), 0)
        body = tk.PanedWindow(page, orient="horizontal", sashwidth=6, bg=self.colors["border"], bd=0)
        body.grid(row=3, column=0, sticky="nsew")
        left = tk.Frame(body, bg=self.colors["bg"], width=520); right = tk.Frame(body, bg=self.colors["surface"])
        body.add(left, minsize=360); body.add(right, minsize=520, stretch="always")
        left.rowconfigure(2, weight=1); left.columnconfigure(0, weight=1)
        filters = self._channel_filter_panel(left, self._fill_plot_matches, "plot"); filters.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        bar = tk.Frame(left, bg=self.colors["bg"]); bar.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        self.plot_match_label = tk.Label(bar, text="", font=self._font(8), bg=self.colors["bg"], fg=self.colors["muted"]); self.plot_match_label.pack(side="left")
        self._button(bar, "Load selected", self._load_plot, width=145).pack(side="right")
        frame, self.plot_match_table = self._table(left, ("package", "sequence", "injection", "channel"), {"package": "Package", "sequence": "Sequence", "injection": "Injection", "channel": "Channel"})
        frame.grid(row=2, column=0, sticky="nsew")
        self.plot_match_table.bind("<<TreeviewSelect>>", lambda _event: self._set_workflow_step(1))
        self._fill_plot_matches()
        right.rowconfigure(2, weight=1); right.columnconfigure(0, weight=1)
        controls = tk.Frame(right, bg=self.colors["surface"]); controls.grid(row=0, column=0, sticky="ew", padx=12, pady=10)
        self._button(controls, "Workspace", self.show_workset, neutral=True, width=108).pack(side="left")
        self._button(controls, "Zoom in", lambda: self._zoom_plot(0.7), neutral=True, width=95).pack(side="left", padx=5)
        self._button(controls, "Zoom out", lambda: self._zoom_plot(1.4), neutral=True, width=100).pack(side="left")
        self._button(controls, "Reset", self._reset_plot, neutral=True, width=80).pack(side="left", padx=5)
        self.plot_mode_var = tk.StringVar(value="Overlay")
        ttk.Combobox(controls, textvariable=self.plot_mode_var, values=("Overlay", "Separate"), state="readonly", width=11, style="Analyze.TCombobox").pack(side="left", padx=(8, 0))
        self.plot_mode_var.trace_add("write", lambda *_args: self._draw_plot())
        tk.Label(controls, text="Drag: box zoom | Space + drag: pan | Right-click: previous view", font=self._font(8), bg=self.colors["surface"], fg=self.colors["muted"], wraplength=390, justify="right").pack(side="right")
        parameters = tk.Frame(right, bg=self.colors["alt"], highlightthickness=1, highlightbackground=self.colors["border"])
        parameters.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 8))
        self.integration_vars = {}
        for index, (key, label, default) in enumerate((
            ("noise_start", "Noise range start (min)", ""), ("noise_end", "Noise range end (min)", ""),
            ("smoothing", "Smoothing width (s)", "1.0"), ("noise", "Noise multiplier", "5.0"),
            ("height", "Minimum height", "0"), ("area", "Minimum area", "0"),
            ("width", "Minimum width (s)", "0"),
        )):
            row, column = divmod(index, 4)
            cell = tk.Frame(parameters, bg=self.colors["alt"]); cell.grid(row=row, column=column, sticky="ew", padx=7, pady=5); parameters.columnconfigure(column, weight=1)
            tk.Label(cell, text=label, font=self._font(7, "bold"), bg=self.colors["alt"], fg=self.colors["muted"]).pack(anchor="w")
            variable = tk.StringVar(value=default); ttk.Entry(cell, textvariable=variable, width=12).pack(fill="x", pady=(2, 0)); self.integration_vars[key] = variable
        self.integration_negative_var = tk.BooleanVar(value=False)
        self.integration_auto_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(parameters, text="Negative peaks", variable=self.integration_negative_var).grid(row=0, column=4, padx=8)
        ttk.Checkbutton(parameters, text="Auto adapt sampling", variable=self.integration_auto_var).grid(row=1, column=4, padx=8)
        self._button(parameters, "Integrate traces", self._integrate_plot, width=145).grid(row=0, column=5, rowspan=2, padx=8, pady=7)
        plot_panes = tk.PanedWindow(right, orient="vertical", sashwidth=6, bg=self.colors["border"], bd=0); plot_panes.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 12))
        plot_frame = tk.Frame(plot_panes, bg=self.colors["surface"]); plot_frame.rowconfigure(0, weight=1); plot_frame.columnconfigure(0, weight=1)
        self.plot_canvas = tk.Canvas(plot_frame, bg="#FFFFFF", highlightthickness=1, highlightbackground=self.colors["border"], takefocus=1)
        self.plot_canvas.grid(row=0, column=0, sticky="nsew")
        self.plot_canvas.configure(cursor="crosshair")
        peak_frame, self.peak_table = self._table(plot_panes, ("trace", "peak", "start", "apex", "end", "baseline_start", "baseline_end", "height", "area", "width", "polarity"), {
            "trace": "Trace", "trace_width": 300, "peak": "Peak", "start": "Start min", "apex": "Apex min", "end": "End min",
            "baseline_start": "Baseline start", "baseline_end": "Baseline end",
            "height": "Height", "area": "Area", "width": "Width s", "polarity": "Polarity",
        })
        plot_panes.add(plot_frame, minsize=260); plot_panes.add(peak_frame, minsize=120)
        self.plot_canvas.bind("<Configure>", lambda _e: self._draw_plot())
        self.plot_canvas.bind("<MouseWheel>", self._plot_wheel)
        self.plot_canvas.bind("<ButtonPress-1>", self._plot_press)
        self.plot_canvas.bind("<B1-Motion>", self._plot_drag)
        self.plot_canvas.bind("<ButtonRelease-1>", self._plot_release)
        self.plot_canvas.bind("<Button-3>", self._plot_previous_view)
        self.plot_canvas.bind("<KeyPress-space>", self._plot_space_press)
        self.plot_canvas.bind("<KeyRelease-space>", self._plot_space_release)
        self.plot_canvas.bind("<Enter>", lambda _event: self.plot_canvas.focus_set())
        self._register_workflow_target(0, left, "Filter the workset and select one or more matching channels.")
        self._register_workflow_target(1, bar, "Choose Load selected to decode the selected raw traces.")
        self._register_workflow_target(2, right, "Compare, zoom, pan, and integrate the loaded traces.")

    def _fill_plot_matches(self) -> None:
        if not hasattr(self, "plot_match_table"):
            return
        self.plot_match_table.delete(*self.plot_match_table.get_children()); self.channel_by_iid.clear()
        records = self._filtered_channels("plot")
        self.plot_match_label.configure(text=f"{len(records)} matching channel context(s)")
        for index, record in enumerate(records):
            iid = f"plot{index}"; self.channel_by_iid[iid] = record
            self.plot_match_table.insert("", "end", iid=iid, values=(record.package.path.name, record.sequence.name, record.injection.name, record.channel.name))

    def _load_plot(self) -> None:
        records = [self.channel_by_iid[iid] for iid in self.plot_match_table.selection() if iid in self.channel_by_iid]
        if not records:
            messagebox.showwarning("Channel comparison", "Select one or more matched channels.", parent=self.root); return
        self._set_workflow_step(1)
        self._background(f"Decoding {len(records)} trace(s)...", lambda: [(record, decode_channel_points(record)) for record in records], self._plot_loaded)

    def _plot_loaded(self, result, error) -> None:
        if error:
            self._log(f"Plot load failed: {error}"); messagebox.showerror("Channel comparison", str(error), parent=self.root); return
        self.plot_series = [(record, points) for record, points in result if points]
        self.peak_results = []
        if hasattr(self, "peak_table"):
            self.peak_table.delete(*self.peak_table.get_children())
        all_points = [point for _record, points in self.plot_series for point in points]
        if not all_points:
            self._log("No signal points were decoded."); return
        xs = [point.time_min for point in all_points]; ys = [point.value for point in all_points]
        ypad = (max(ys) - min(ys)) * 0.05 or 1.0
        self.plot_bounds = (min(xs), max(xs), min(ys) - ypad, max(ys) + ypad); self.plot_view = self.plot_bounds
        self.plot_view_history.clear()
        self._set_workflow_step(2)
        self._draw_plot(); self._log(f"Loaded {len(self.plot_series)} trace(s), {len(all_points)} raw point(s).")

    def _draw_plot(self) -> None:
        if not hasattr(self, "plot_canvas") or not self.plot_canvas.winfo_exists():
            return
        canvas = self.plot_canvas; canvas.delete("all")
        width = max(canvas.winfo_width(), 300); height = max(canvas.winfo_height(), 220)
        left, top, right, bottom = self._plot_geometry()
        canvas.create_rectangle(left, top, right, bottom, outline=self.colors["border"])
        if not self.plot_series or not self.plot_view:
            canvas.create_text(width / 2, height / 2, text="Select channels and load the comparison.", fill=self.colors["muted"], font=self._font(10)); return
        xmin, xmax, ymin, ymax = self.plot_view
        if xmax <= xmin or ymax <= ymin:
            return
        for tick in range(6):
            x = left + (right - left) * tick / 5; value = xmin + (xmax - xmin) * tick / 5
            canvas.create_line(x, bottom, x, bottom + 5, fill=self.colors["muted"]); canvas.create_text(x, bottom + 18, text=f"{value:.3g}", fill=self.colors["muted"], font=self._font(7))
            y = bottom - (bottom - top) * tick / 5; yvalue = ymin + (ymax - ymin) * tick / 5
            canvas.create_line(left - 5, y, left, y, fill=self.colors["muted"]); canvas.create_text(left - 9, y, text=f"{yvalue:.3g}", anchor="e", fill=self.colors["muted"], font=self._font(7))
        canvas.create_text((left + right) / 2, height - 10, text="Time (min)", fill=self.colors["muted"], font=self._font(8))
        palette = ("#2374E1", "#D64545", "#198754", "#8E5BB7", "#D97706", "#008B95", "#555B66")
        separate = hasattr(self, "plot_mode_var") and self.plot_mode_var.get() == "Separate"
        for index, (record, points) in enumerate(self.plot_series):
            visible = [point for point in points if xmin <= point.time_min <= xmax]
            if len(visible) > max(right - left, 200):
                stride = max(1, len(visible) // int(max(right - left, 200))); visible = visible[::stride]
            coords = []
            trace_top, trace_bottom = top, bottom
            trace_ymin, trace_ymax = ymin, ymax
            if separate:
                track_height = (bottom - top) / max(len(self.plot_series), 1)
                trace_top = top + index * track_height + 3; trace_bottom = top + (index + 1) * track_height - 3
                local_values = [point.value for point in visible] or [0.0, 1.0]
                trace_ymin, trace_ymax = min(local_values), max(local_values)
                if trace_ymax == trace_ymin:
                    trace_ymax += 1.0
                canvas.create_line(left, trace_bottom, right, trace_bottom, fill="#ECEDEF")
            for point in visible:
                coords.extend((left + (point.time_min - xmin) / (xmax - xmin) * (right - left), trace_bottom - (point.value - trace_ymin) / (trace_ymax - trace_ymin) * (trace_bottom - trace_top)))
            color = palette[index % len(palette)]
            if len(coords) >= 4:
                canvas.create_line(*coords, fill=color, width=2.0)
            canvas.create_line(right - 245, top + 14 + index * 18, right - 225, top + 14 + index * 18, fill=color, width=2)
            canvas.create_text(right - 218, top + 14 + index * 18, text=record.label, anchor="w", fill=color, font=self._font(7))
            for peak in (item for item in self.peak_results if item.trace_key == record.label):
                if peak.end_min < xmin or peak.start_min > xmax:
                    continue
                visible_start = max(peak.start_min, xmin); visible_end = min(peak.end_min, xmax)
                span = peak.end_min - peak.start_min
                start_ratio = (visible_start - peak.start_min) / span if span > 0 else 0.0
                end_ratio = (visible_end - peak.start_min) / span if span > 0 else 1.0
                base_start = peak.baseline_start + (peak.baseline_end - peak.baseline_start) * start_ratio
                base_end = peak.baseline_start + (peak.baseline_end - peak.baseline_start) * end_ratio
                x1 = left + (visible_start - xmin) / (xmax - xmin) * (right - left)
                x2 = left + (visible_end - xmin) / (xmax - xmin) * (right - left)
                y1 = trace_bottom - (base_start - trace_ymin) / (trace_ymax - trace_ymin) * (trace_bottom - trace_top)
                y2 = trace_bottom - (base_end - trace_ymin) / (trace_ymax - trace_ymin) * (trace_bottom - trace_top)
                y1 = min(max(y1, trace_top), trace_bottom); y2 = min(max(y2, trace_top), trace_bottom)
                canvas.create_line(x1, y1, x2, y2, fill="#D93939", width=2.4)
                if xmin <= peak.start_min <= xmax:
                    canvas.create_line(x1, y1 - 7, x1, y1 + 7, fill="#D93939", width=2.4)
                if xmin <= peak.end_min <= xmax:
                    canvas.create_line(x2, y2 - 7, x2, y2 + 7, fill="#D93939", width=2.4)

    def _integrate_plot(self) -> None:
        if not self.plot_series:
            messagebox.showwarning("Integration", "Load one or more traces first.", parent=self.root); return
        try:
            def optional_float(key: str):
                value = self.integration_vars[key].get().strip()
                return float(value) if value else None
            noise_start = optional_float("noise_start")
            noise_end = optional_float("noise_end")
            if (noise_start is None) != (noise_end is None):
                raise ValueError("Baseline noise range requires both start and end.")
            if noise_start is not None and noise_end <= noise_start:
                raise ValueError("Baseline noise range end must be greater than start.")
            settings = IntegrationSettings(
                baseline_noise_start_min=noise_start,
                baseline_noise_end_min=noise_end,
                smoothing_width_s=float(self.integration_vars["smoothing"].get()),
                noise_multiplier=float(self.integration_vars["noise"].get()),
                minimum_height=float(self.integration_vars["height"].get()),
                minimum_area=float(self.integration_vars["area"].get()),
                minimum_width_s=float(self.integration_vars["width"].get()),
                detect_negative=bool(self.integration_negative_var.get()),
            )
        except ValueError as exc:
            messagebox.showerror("Integration", f"Invalid integration parameters: {exc}", parent=self.root); return
        auto_adapt = bool(self.integration_auto_var.get())
        series = list(self.plot_series)
        def worker():
            effective = adapt_integration_settings((points for _record, points in series), settings) if auto_adapt else settings
            peaks = [peak for record, points in series for peak in integrate_signal(record.label, points, effective)]
            return effective, peaks
        self._background(f"Integrating {len(series)} trace(s) in the background...", worker, self._integration_done)

    def _integration_done(self, result, error) -> None:
        if error:
            self._log(f"Integration failed: {error}")
            messagebox.showerror("Integration", str(error), parent=self.root)
            return
        effective, self.peak_results = result
        self.peak_table.delete(*self.peak_table.get_children())
        for peak in self.peak_results:
            self.peak_table.insert("", "end", values=(
                peak.trace_key, peak.peak_index, f"{peak.start_min:.6g}", f"{peak.apex_min:.6g}", f"{peak.end_min:.6g}",
                f"{peak.baseline_start:.8g}", f"{peak.baseline_end:.8g}", f"{peak.height:.8g}", f"{peak.area:.8g}",
                f"{peak.width_s:.6g}", peak.polarity,
            ))
        self._draw_plot()
        self._log(
            f"External integration complete: {len(self.peak_results)} peak(s); shared effective smoothing "
            f"{effective.smoothing_width_s:.4g} s, minimum width {effective.minimum_width_s:.4g} s."
        )

    def _remember_plot_view(self, view: tuple[float, float, float, float] | None = None) -> None:
        value = view or self.plot_view
        if value is not None and (not self.plot_view_history or self.plot_view_history[-1] != value):
            self.plot_view_history.append(value)
            del self.plot_view_history[:-40]

    def _schedule_plot_draw(self) -> None:
        if self._plot_redraw_job is not None:
            return
        def draw() -> None:
            self._plot_redraw_job = None
            self._draw_plot()
        self._plot_redraw_job = self.root.after(16, draw)

    def _zoom_plot(self, factor: float) -> None:
        if not self.plot_view:
            return
        self._remember_plot_view()
        xmin, xmax, ymin, ymax = self.plot_view; cx = (xmin + xmax) / 2; cy = (ymin + ymax) / 2
        self.plot_view = (cx - (xmax - xmin) * factor / 2, cx + (xmax - xmin) * factor / 2, cy - (ymax - ymin) * factor / 2, cy + (ymax - ymin) * factor / 2); self._draw_plot()

    def _reset_plot(self) -> None:
        if self.plot_view and self.plot_bounds and self.plot_view != self.plot_bounds:
            self._remember_plot_view()
        self.plot_view = self.plot_bounds; self._draw_plot()

    def _plot_wheel(self, event) -> None:
        self._zoom_plot(0.82 if event.delta > 0 else 1.22)
        return "break"

    def _plot_press(self, event) -> None:
        if not self.plot_view:
            return
        self.plot_canvas.focus_set()
        self._plot_drag_mode = "pan" if self.plot_space_down else "box"
        self._plot_drag_origin = (event.x, event.y, self.plot_view)
        if self._plot_drag_mode == "pan":
            self.plot_canvas.configure(cursor="fleur")
        else:
            self.plot_canvas.delete("zoom-box")
            self._plot_zoom_rect = self.plot_canvas.create_rectangle(event.x, event.y, event.x, event.y, outline=self.colors["primary"], width=2, dash=(5, 3), tags="zoom-box")

    def _plot_drag(self, event) -> None:
        if not self._plot_drag_origin or not self.plot_view:
            return
        sx, sy, view = self._plot_drag_origin
        if self._plot_drag_mode == "box":
            if self._plot_zoom_rect is not None:
                self.plot_canvas.coords(self._plot_zoom_rect, sx, sy, event.x, event.y)
            return
        xmin, xmax, ymin, ymax = view
        width = max(self.plot_canvas.winfo_width() - 86, 100); height = max(self.plot_canvas.winfo_height() - 77, 100)
        dx = (event.x - sx) / width * (xmax - xmin); dy = (event.y - sy) / height * (ymax - ymin)
        self.plot_view = (xmin - dx, xmax - dx, ymin + dy, ymax + dy)
        self._schedule_plot_draw()

    def _plot_release(self, event) -> None:
        origin = self._plot_drag_origin
        mode = self._plot_drag_mode
        self._plot_drag_origin = None
        self._plot_drag_mode = None
        self.plot_canvas.delete("zoom-box")
        self._plot_zoom_rect = None
        self.plot_canvas.configure(cursor="hand2" if self.plot_space_down else "crosshair")
        if origin is None or self.plot_view is None:
            return
        sx, sy, original_view = origin
        if mode == "pan":
            if self.plot_view != original_view:
                self._remember_plot_view(original_view)
            self._schedule_plot_draw()
            return
        left, top, right, bottom = self._plot_geometry()
        x1, x2 = sorted((max(left, min(right, sx)), max(left, min(right, event.x))))
        y1, y2 = sorted((max(top, min(bottom, sy)), max(top, min(bottom, event.y))))
        if x2 - x1 < 8 or y2 - y1 < 8:
            return
        xmin, xmax, ymin, ymax = original_view
        new_xmin = xmin + (x1 - left) / max(right - left, 1) * (xmax - xmin)
        new_xmax = xmin + (x2 - left) / max(right - left, 1) * (xmax - xmin)
        if hasattr(self, "plot_mode_var") and self.plot_mode_var.get() == "Separate":
            new_ymin, new_ymax = ymin, ymax
        else:
            new_ymax = ymax - (y1 - top) / max(bottom - top, 1) * (ymax - ymin)
            new_ymin = ymax - (y2 - top) / max(bottom - top, 1) * (ymax - ymin)
        self._remember_plot_view(original_view)
        self.plot_view = (new_xmin, new_xmax, new_ymin, new_ymax)
        self._draw_plot()

    def _plot_previous_view(self, _event=None) -> str:
        if self.plot_view_history:
            self.plot_view = self.plot_view_history.pop()
            self._draw_plot()
        return "break"

    def _plot_space_press(self, _event=None) -> str:
        self.plot_space_down = True
        if hasattr(self, "plot_canvas"):
            self.plot_canvas.configure(cursor="hand2")
        return "break"

    def _plot_space_release(self, _event=None) -> str:
        self.plot_space_down = False
        if hasattr(self, "plot_canvas") and self._plot_drag_mode != "pan":
            self.plot_canvas.configure(cursor="crosshair")
        return "break"

    def _plot_geometry(self) -> tuple[int, int, int, int]:
        width = max(self.plot_canvas.winfo_width(), 300)
        height = max(self.plot_canvas.winfo_height(), 220)
        return 64, 25, width - 22, height - 52

    # Formula
    def show_formula(self) -> None:
        page = self._new_page()
        self._heading(page, "Batch-preview Direct CM formulas", "Decode only Direct CM formula objects from loaded report XML for fast startup, then select formulas and filtered injection contexts for batch evaluation.", ("Scan Direct CM formulas", "Choose contexts", "Batch preview"), 0)
        body = tk.Frame(page, bg=self.colors["bg"]); body.grid(row=3, column=0, sticky="nsew"); body.rowconfigure(3, weight=1); body.columnconfigure(0, weight=1)
        filters = tk.Frame(body, bg=self.colors["bg"]); filters.grid(row=0, column=0, sticky="ew", pady=(0, 7)); filters.columnconfigure(3, weight=1)
        tk.Label(filters, text="Formula source", font=self._font(8, "bold"), bg=self.colors["bg"], fg=self.colors["muted"]).grid(row=0, column=0, padx=(0, 7))
        self.formula_source_var = tk.StringVar(value="Useful formula library")
        source_combo = ttk.Combobox(filters, textvariable=self.formula_source_var, values=("Useful formula library", "Used by loaded reports"), state="readonly", width=25)
        source_combo.grid(row=0, column=1, sticky="w", padx=(0, 12)); source_combo.bind("<<ComboboxSelected>>", lambda _event: self._fill_formula_inventory())
        tk.Label(filters, text="Search", font=self._font(8, "bold"), bg=self.colors["bg"], fg=self.colors["muted"]).grid(row=0, column=2, padx=(0, 7))
        self.formula_query_var = tk.StringVar(); query = ttk.Entry(filters, textvariable=self.formula_query_var); query.grid(row=0, column=3, sticky="ew")
        query.bind("<KeyRelease>", lambda _event: self._fill_formula_inventory())
        self.formula_count_label = tk.Label(filters, text="Loading useful library...", font=self._font(8), bg=self.colors["bg"], fg=self.colors["muted"])
        self.formula_count_label.grid(row=0, column=4, padx=10)
        self._button(filters, "Batch preview", self._evaluate_formula, width=140).grid(row=0, column=5)
        self._button(filters, "Workspace", self.show_workset, neutral=True, width=108).grid(row=0, column=6, padx=(8, 0))
        progress_shell = tk.Frame(body, bg=self.colors["bg"]); progress_shell.grid(row=1, column=0, sticky="ew", pady=(0, 7)); progress_shell.columnconfigure(1, weight=1)
        self.formula_scan_label = tk.Label(progress_shell, text=self._formula_scan_status(), font=self._font(8), bg=self.colors["bg"], fg=self.colors["muted"], anchor="w")
        self.formula_scan_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 3))
        tk.Label(progress_shell, text="Inventory", font=self._font(8, "bold"), bg=self.colors["bg"], fg=self.colors["muted"]).grid(row=1, column=0, sticky="w", padx=(0, 7))
        self.formula_progress_bar = ttk.Progressbar(progress_shell, mode="determinate")
        self.formula_progress_bar.grid(row=1, column=1, sticky="ew")
        helper = tk.Label(body, text="Filter injection contexts at all four levels, then select one or more formulas and one or more matching injections.", font=self._font(8), bg=self.colors["bg"], fg=self.colors["muted"])
        helper.grid(row=2, column=0, sticky="w", pady=(0, 6))
        panes = tk.PanedWindow(body, orient="vertical", sashwidth=6, bg=self.colors["border"], bd=0); panes.grid(row=3, column=0, sticky="nsew")
        formula_frame, self.formula_inventory_table = self._table(panes, ("package", "report", "sheet", "cell", "formula", "meaning", "channel", "component", "support", "type"), {
            "package": "Source", "report": "Report / KB evidence", "sheet": "Sheet / category", "cell": "Cell",
            "formula": "Direct CM formula", "formula_width": 430,
            "meaning": "Meaning / interpretation", "meaning_width": 430,
            "channel": "Fixed channel", "component": "Fixed component", "support": "Usability", "type": "Object type",
        })
        context_shell = tk.Frame(panes, bg=self.colors["bg"]); context_shell.rowconfigure(1, weight=1); context_shell.columnconfigure(0, weight=1)
        context_filters = self._channel_filter_panel(context_shell, self._formula_context_filter_changed, "formula")
        context_filters.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        source_frame, self.formula_source_table = self._table(context_shell, ("package", "sequence", "injection", "channels"), {"package": "Package", "sequence": "Sequence", "injection": "Injection", "channels": "Matching channels", "channels_width": 420})
        source_frame.grid(row=1, column=0, sticky="nsew")
        result_frame, self.formula_result_table = self._table(panes, ("package", "sequence", "injection", "formula", "channel", "value", "status", "detail"), {
            "package": "Package", "sequence": "Sequence", "injection": "Injection", "formula": "Formula", "formula_width": 340,
            "channel": "Channel", "value": "Value", "status": "Status", "detail": "Evidence / detail", "detail_width": 460,
        })
        panes.add(formula_frame, minsize=190); panes.add(context_shell, minsize=190); panes.add(result_frame, minsize=160)
        self.formula_inventory_table.bind("<<TreeviewSelect>>", lambda _event: self._formula_selection_changed())
        self.formula_source_table.bind("<<TreeviewSelect>>", lambda _event: self._formula_selection_changed())
        self._register_workflow_target(0, formula_frame, "Search the library or loaded-report evidence, then select one or more Direct CM formulas.")
        self._register_workflow_target(1, context_shell, "Filter and select the injection contexts that provide the required data.")
        self._register_workflow_target(2, result_frame, "Choose Batch preview above; calculated values and evidence appear here.")
        self._fill_formula_contexts()
        self._fill_formula_inventory()
        if self.formula_scan_complete:
            self._log(f"Using prefetched Direct CM inventory: {len(self.formulas)} formula(s).")
        else:
            self._start_formula_prefetch()
        self._refresh_formula_scan_widgets()

    def _formula_context_filter_changed(self) -> None:
        self._fill_formula_contexts()
        self._set_workflow_step(1)

    def _formula_selection_changed(self) -> None:
        formulas_selected = bool(self.formula_inventory_table.selection()) if hasattr(self, "formula_inventory_table") else False
        contexts_selected = bool(self.formula_source_table.selection()) if hasattr(self, "formula_source_table") else False
        if formulas_selected and contexts_selected:
            self._set_workflow_step(2)
        elif formulas_selected:
            self._set_workflow_step(1)

    def _fill_formula_contexts(self) -> None:
        if not hasattr(self, "formula_source_table"):
            return
        matched_channels = self._filtered_channels("formula")
        channels_by_injection: dict[str, list[str]] = {}
        for row in matched_channels:
            key = f"{row.package.path}|{row.injection.id}"
            channels_by_injection.setdefault(key, []).append(row.channel.name)
        self.formula_source_table.delete(*self.formula_source_table.get_children())
        self.injection_by_iid.clear()
        visible = [row for row in self.injections if f"{row.package.path}|{row.injection.id}" in channels_by_injection]
        for index, record in enumerate(visible):
            iid = f"formula{index}"; self.injection_by_iid[iid] = record
            key = f"{record.package.path}|{record.injection.id}"
            names = ", ".join(sorted(set(channels_by_injection[key]), key=str.lower))
            self.formula_source_table.insert("", "end", iid=iid, values=(record.package.path.name, record.sequence.name, record.injection.name, names))
        self._log(f"Formula context filter: {len(visible)} injection(s), {len(matched_channels)} matching channel context(s).")

    def _fill_formula_inventory(self) -> None:
        if not hasattr(self, "formula_inventory_table"):
            return
        query = self.formula_query_var.get().strip().casefold() if hasattr(self, "formula_query_var") else ""
        source = self.formula_source_var.get() if hasattr(self, "formula_source_var") else "Useful formula library"
        if source == "Useful formula library" and self.workset:
            package = self.workset[0].package
            candidates = [
                FormulaRecord(
                    package, entry.source, entry.category, "", "FormulaLibrary", entry.formula,
                    "", "", "Direct CM", "Formula Library", "Locally evaluable",
                )
                for entry in self.formula_library_entries
            ]
        else:
            candidates = self.formulas
        query_words = [word for word in query.split() if word]
        rows = []
        for row in candidates:
            searchable = " ".join((row.source_label, row.report_name, row.sheet_name, row.excel_range, row.formula, row.meaning, row.fixed_channel, row.support, row.object_type)).casefold()
            if row.engine == "Direct CM" and all(word in searchable for word in query_words):
                rows.append(row)
        self.formula_inventory_table.delete(*self.formula_inventory_table.get_children()); self.formula_by_iid.clear()
        for index, row in enumerate(rows):
            iid = f"inventory{index}"; self.formula_by_iid[iid] = row
            self.formula_inventory_table.insert("", "end", iid=iid, values=(row.source_label, row.report_name, row.sheet_name, row.excel_range, row.formula, row.meaning, row.fixed_channel, row.fixed_component, row.support or "Used by loaded report", row.object_type))
        if source == "Useful formula library":
            detail = "loading..." if self.formula_library_active else f"{len(self.formula_library_entries)} available"
            self.formula_count_label.configure(text=f"{len(rows)} shown | {detail}")
        else:
            self.formula_count_label.configure(text=f"{len(rows)} shown | {len(self.formulas)} report formula(s) cached")

    def _evaluate_formula(self) -> None:
        contexts = [self.injection_by_iid[iid] for iid in self.formula_source_table.selection() if iid in self.injection_by_iid]
        formulas = [self.formula_by_iid[iid] for iid in self.formula_inventory_table.selection() if iid in self.formula_by_iid]
        if not contexts or not formulas:
            messagebox.showwarning("CM formula", "Select at least one CMBX formula and one injection context.", parent=self.root); return
        self._set_workflow_step(2)
        if any(row.formula.strip().casefold().startswith("chm.") and not row.fixed_channel for row in formulas):
            context_keys = {row.key for row in contexts}
            channel_names = {
                row.channel.name for row in self._filtered_channels("formula")
                if f"{row.package.path}|{row.sequence.id}|{row.injection.id}" in context_keys
            }
            if len(channel_names) != 1:
                messagebox.showwarning(
                    "CM formula",
                    "The selected chm.* formula needs one signal context. Use the Channel filter below the formula table so the selected injections resolve to exactly one channel name.",
                    parent=self.root,
                )
                return
            channel_name = next(iter(channel_names))
            formulas = [
                FormulaRecord(
                    row.package, row.report_name, row.sheet_name, row.excel_range, row.object_type,
                    row.formula, channel_name if row.formula.strip().casefold().startswith("chm.") and not row.fixed_channel else row.fixed_channel,
                    row.fixed_component, row.engine, row.source_scope, row.support,
                )
                for row in formulas
            ]
        count = len(contexts) * len(formulas)
        self._background(f"Batch-previewing {len(formulas)} formula(s) across {len(contexts)} injection(s) ({count} evaluation(s))...", lambda: evaluate_formula_batch(contexts, formulas), self._formula_done)

    def _formula_done(self, result, error) -> None:
        if error:
            self._log(f"Formula evaluation failed: {error}"); messagebox.showerror("CM formula", str(error), parent=self.root); return
        self.formula_result_table.delete(*self.formula_result_table.get_children())
        for row in result:
            self.formula_result_table.insert("", "end", values=(row.package, row.sequence, row.injection, row.formula, row.fixed_channel, row.value, row.status, row.detail))
        ok = sum(row.status == "ok" for row in result)
        self._log(f"Formula evaluation complete: {ok}/{len(result)} returned ok.")


def main() -> None:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--task", choices=tuple(ReadAnalyzeWindow.TASKS))
    args, _unknown = parser.parse_known_args()
    enable_dpi_awareness()
    root = tk.Tk()
    ReadAnalyzeWindow(root, initial_task=args.task)
    root.mainloop()


if __name__ == "__main__":
    main()
