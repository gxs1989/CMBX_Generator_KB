from __future__ import annotations

import os
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from external_report_engine import ExternalReportEngine, InjectionReportResult, write_external_report_workbook
from external_report_spec import ExternalReportSpec, parse_external_report_md
from formula_catalog import (
    FormulaCatalogEntry,
    build_formula_catalog,
    external_scalar_block,
    filter_formula_catalog,
    unified_md_block,
)


UNIFIED_REPORT_SPEC = Path(__file__).resolve().parent / "docs" / "CM_REPORT_TEMPLATE_MD_TO_CMBX_SPEC.md"


class ExternalReportWindow:
    def __init__(self, parent: tk.Misc, *, initial_paths: list[Path] | None = None, output_folder: Path | None = None):
        self.parent = parent
        self.output_folder = output_folder or Path.cwd()
        self.paths: list[Path] = []
        self.packages = []
        self.spec: ExternalReportSpec | None = None
        self.results: list[InjectionReportResult] = []
        self.row_keys: dict[str, tuple[str, str]] = {}
        self.formula_catalog = build_formula_catalog(Path(__file__).resolve().parent / "docs")
        self.formula_row_context: dict[str, FormulaCatalogEntry] = {}
        self.top = tk.Toplevel(parent)
        self.top.title("External Report Engine")
        self.top.geometry("1500x900")
        self.top.minsize(1120, 720)
        try:
            self.top.state("zoomed")
        except tk.TclError:
            pass
        self._build_ui()
        for path in initial_paths or []:
            self._add_path(path)

    def _build_ui(self) -> None:
        shell = ttk.Frame(self.top, padding=12)
        shell.pack(fill="both", expand=True)
        shell.columnconfigure(0, weight=1)
        shell.rowconfigure(2, weight=1)

        toolbar = ttk.Frame(shell)
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        ttk.Label(toolbar, text="External Report Engine", font=("Calibri", 18, "bold")).pack(side="left", padx=(0, 18))
        ttk.Button(toolbar, text="Add CMBX", command=self._browse_cmbx).pack(side="left", padx=3)
        ttk.Button(toolbar, text="Add Folder", command=self._browse_folder).pack(side="left", padx=3)
        ttk.Button(toolbar, text="Remove", command=self._remove_paths).pack(side="left", padx=3)
        ttk.Button(toolbar, text="Load Report MD", command=self._browse_md).pack(side="left", padx=(14, 3))
        ttk.Button(toolbar, text="Formula Finder", command=self._show_formula_finder).pack(side="left", padx=3)
        ttk.Button(toolbar, text="Open Unified Spec", command=self._open_unified_spec).pack(side="left", padx=3)
        ttk.Button(toolbar, text="Preflight", command=self._preflight).pack(side="left", padx=(14, 3))
        ttk.Button(toolbar, text="Preview Selected", command=self._preview_selected).pack(side="left", padx=3)
        ttk.Button(toolbar, text="Batch Preview", command=self._preview_all).pack(side="left", padx=3)
        ttk.Button(toolbar, text="Export XLSX", command=self._export).pack(side="left", padx=(14, 3))
        ttk.Button(toolbar, text="Close", command=self.top.destroy).pack(side="right")

        self.status_var = tk.StringVar(value="Add CMBX files and paste or load a deterministic Report MD.")
        ttk.Label(shell, textvariable=self.status_var).grid(row=1, column=0, sticky="ew", pady=(0, 6))

        main = ttk.Panedwindow(shell, orient="vertical")
        main.grid(row=2, column=0, sticky="nsew")
        upper = ttk.Panedwindow(main, orient="horizontal")
        lower = ttk.Notebook(main)
        main.add(upper, weight=2)
        main.add(lower, weight=3)

        sources = ttk.LabelFrame(upper, text="CMBX Sources", padding=6)
        editor = ttk.LabelFrame(upper, text="Report MD", padding=6)
        upper.add(sources, weight=2)
        upper.add(editor, weight=3)

        sources.columnconfigure(0, weight=1)
        sources.rowconfigure(0, weight=1)
        self.source_tree = ttk.Treeview(sources, columns=("path",), show="headings", selectmode="extended")
        self.source_tree.heading("path", text="CMBX File")
        self.source_tree.column("path", width=520)
        self.source_tree.grid(row=0, column=0, sticky="nsew")
        source_scroll = ttk.Scrollbar(sources, orient="vertical", command=self.source_tree.yview)
        source_scroll.grid(row=0, column=1, sticky="ns")
        self.source_tree.configure(yscrollcommand=source_scroll.set)

        editor.columnconfigure(0, weight=1)
        editor.rowconfigure(0, weight=1)
        self.md_text = tk.Text(editor, wrap="none", undo=True, font=("Consolas", 9))
        self.md_text.grid(row=0, column=0, sticky="nsew")
        md_y = ttk.Scrollbar(editor, orient="vertical", command=self.md_text.yview)
        md_x = ttk.Scrollbar(editor, orient="horizontal", command=self.md_text.xview)
        md_y.grid(row=0, column=1, sticky="ns")
        md_x.grid(row=1, column=0, sticky="ew")
        self.md_text.configure(yscrollcommand=md_y.set, xscrollcommand=md_x.set)

        compatibility_tab = ttk.Frame(lower, padding=6)
        summary_tab = ttk.Frame(lower, padding=6)
        tables_tab = ttk.Frame(lower, padding=6)
        plot_tab = ttk.Frame(lower, padding=6)
        log_tab = ttk.Frame(lower, padding=6)
        lower.add(compatibility_tab, text="Compatibility")
        lower.add(summary_tab, text="Report Preview")
        lower.add(tables_tab, text="Dynamic Tables")
        lower.add(plot_tab, text="Plots")
        lower.add(log_tab, text="Log")

        self.compat_tree = self._tree(compatibility_tab, ("package", "sequence", "injection", "status", "detail"), (180, 170, 210, 90, 620), selectmode="extended")
        self.summary_tree = self._tree(summary_tab, ("package", "sequence", "injection", "item", "value", "status", "detail"), (150, 150, 180, 190, 130, 90, 420))
        self.table_tree = self._tree(tables_tab, ("package", "injection", "table", "time_min", "device", "property", "value", "message"), (150, 180, 160, 90, 140, 200, 160, 420))
        self.plot_selector = ttk.Combobox(plot_tab, state="readonly")
        self.plot_selector.pack(fill="x", pady=(0, 6))
        self.plot_selector.bind("<<ComboboxSelected>>", lambda _event: self._draw_plot())
        self.plot_canvas = tk.Canvas(plot_tab, bg="white", highlightthickness=1, highlightbackground="#CBD5E1")
        self.plot_canvas.pack(fill="both", expand=True)
        self.plot_canvas.bind("<Configure>", lambda _event: self._draw_plot())
        self.log_text = tk.Text(log_tab, wrap="word", state="disabled", font=("Consolas", 9))
        self.log_text.pack(fill="both", expand=True)

    def _tree(self, parent, columns, widths, selectmode="browse"):
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        tree = ttk.Treeview(parent, columns=columns, show="headings", selectmode=selectmode)
        for name, width in zip(columns, widths):
            tree.heading(name, text=name.replace("_", " ").title())
            tree.column(name, width=width, anchor="w")
        tree.grid(row=0, column=0, sticky="nsew")
        y = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        x = ttk.Scrollbar(parent, orient="horizontal", command=tree.xview)
        y.grid(row=0, column=1, sticky="ns")
        x.grid(row=1, column=0, sticky="ew")
        tree.configure(yscrollcommand=y.set, xscrollcommand=x.set)
        return tree

    def _browse_cmbx(self) -> None:
        for name in filedialog.askopenfilenames(parent=self.top, title="Add CMBX files", filetypes=[("CMBX", "*.cmbx")]):
            self._add_path(Path(name))

    def _browse_folder(self) -> None:
        name = filedialog.askdirectory(parent=self.top, title="Add a folder of CMBX files")
        if name:
            for path in Path(name).rglob("*.cmbx"):
                if "deleted" not in {part.casefold() for part in path.parts}:
                    self._add_path(path)

    def _add_path(self, path: Path) -> None:
        path = path.resolve()
        if path.suffix.casefold() != ".cmbx" or path in self.paths:
            return
        self.paths.append(path)
        self.source_tree.insert("", "end", iid=str(len(self.paths) - 1), values=(str(path),))

    def _remove_paths(self) -> None:
        remove = {Path(self.source_tree.item(iid, "values")[0]) for iid in self.source_tree.selection()}
        self.paths = [path for path in self.paths if path not in remove]
        self.source_tree.delete(*self.source_tree.get_children())
        for index, path in enumerate(self.paths):
            self.source_tree.insert("", "end", iid=str(index), values=(str(path),))

    def _browse_md(self) -> None:
        name = filedialog.askopenfilename(parent=self.top, title="Load Report MD", filetypes=[("Markdown", "*.md"), ("All", "*.*")])
        if name:
            self.md_text.delete("1.0", "end")
            self.md_text.insert("1.0", Path(name).read_text(encoding="utf-8-sig"))

    def _open_unified_spec(self) -> None:
        if not UNIFIED_REPORT_SPEC.exists():
            self._fail(FileNotFoundError(UNIFIED_REPORT_SPEC))
            return
        os.startfile(str(UNIFIED_REPORT_SPEC))

    def _show_formula_finder(self) -> None:
        dialog = tk.Toplevel(self.top)
        dialog.title("Formula Finder")
        dialog.geometry("1220x760")
        dialog.minsize(900, 560)
        dialog.transient(self.top)
        dialog.lift()
        shell = ttk.Frame(dialog, padding=10)
        shell.pack(fill="both", expand=True)
        shell.columnconfigure(0, weight=1)
        shell.rowconfigure(1, weight=1)

        filters = ttk.Frame(shell)
        filters.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        filters.columnconfigure(1, weight=1)
        ttk.Label(filters, text="Search").grid(row=0, column=0, padx=(0, 6))
        query_var = tk.StringVar()
        query_entry = ttk.Entry(filters, textvariable=query_var)
        query_entry.grid(row=0, column=1, sticky="ew")
        ttk.Label(filters, text="Engine").grid(row=0, column=2, padx=(12, 6))
        engine_var = tk.StringVar(value="All")
        engine_combo = ttk.Combobox(filters, textvariable=engine_var, values=("All", "CM Report", "FormulaOne"), state="readonly", width=14)
        engine_combo.grid(row=0, column=3)
        external_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(filters, text="External V1 only", variable=external_var).grid(row=0, column=4, padx=(12, 0))

        paned = ttk.Panedwindow(shell, orient="vertical")
        paned.grid(row=1, column=0, sticky="nsew")
        list_frame = ttk.Frame(paned)
        detail_frame = ttk.LabelFrame(paned, text="Formula Detail", padding=8)
        paned.add(list_frame, weight=3)
        paned.add(detail_frame, weight=2)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        columns = ("name", "formula", "engine", "category", "support", "summary")
        tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        widths = (190, 320, 100, 140, 100, 420)
        for column, width in zip(columns, widths):
            tree.heading(column, text=column.title())
            tree.column(column, width=width, anchor="w")
        tree.grid(row=0, column=0, sticky="nsew")
        tree_y = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
        tree_x = ttk.Scrollbar(list_frame, orient="horizontal", command=tree.xview)
        tree_y.grid(row=0, column=1, sticky="ns")
        tree_x.grid(row=1, column=0, sticky="ew")
        tree.configure(yscrollcommand=tree_y.set, xscrollcommand=tree_x.set)
        detail = tk.Text(detail_frame, wrap="word", height=8, state="disabled", font=("Consolas", 9))
        detail.pack(fill="both", expand=True)

        actions = ttk.Frame(shell)
        actions.grid(row=2, column=0, sticky="ew", pady=(8, 0))
        count_var = tk.StringVar()
        ttk.Label(actions, textvariable=count_var).pack(side="left")

        def selected_entry() -> FormulaCatalogEntry | None:
            selection = tree.selection()
            return self.formula_row_context.get(selection[0]) if selection else None

        def insert_block(external: bool = False) -> None:
            entry = selected_entry()
            if not entry:
                return
            try:
                block = external_scalar_block(entry) if external else unified_md_block(entry)
            except Exception as exc:
                messagebox.showwarning("Formula Finder", str(exc), parent=dialog)
                return
            self.md_text.insert("insert", block)
            self.md_text.see("insert")
            self.status_var.set("Inserted an External executable Scalar block." if external else "Inserted a CM Report Template block; it is not executed by External Preview.")
            dialog.lift()

        def copy_formula() -> None:
            entry = selected_entry()
            if entry and entry.formula:
                dialog.clipboard_clear()
                dialog.clipboard_append(entry.formula)

        ttk.Button(actions, text="Insert CM Template Block", command=insert_block).pack(side="right", padx=3)
        ttk.Button(actions, text="Use in External Preview", command=lambda: insert_block(True)).pack(side="right", padx=3)
        ttk.Button(actions, text="Copy Formula", command=copy_formula).pack(side="right", padx=3)
        ttk.Button(actions, text="Close", command=dialog.destroy).pack(side="right", padx=(3, 12))

        def show_detail(_event=None) -> None:
            entry = selected_entry()
            detail.configure(state="normal")
            detail.delete("1.0", "end")
            if entry:
                detail.insert("1.0", f"Name: {entry.name}\nFormula: {entry.formula or '[conceptual Help topic]'}\nEngine: {entry.engine}\nCategory: {entry.category}\nSupport: {entry.support}\nSource: {entry.source}\n\n{entry.summary}")
            detail.configure(state="disabled")

        def refresh(*_args) -> None:
            rows = filter_formula_catalog(self.formula_catalog, query_var.get(), engine_var.get(), external_var.get())
            tree.delete(*tree.get_children())
            self.formula_row_context.clear()
            for index, entry in enumerate(rows):
                iid = str(index)
                self.formula_row_context[iid] = entry
                tree.insert("", "end", iid=iid, values=(entry.name, entry.formula, entry.engine, entry.category, entry.support, entry.summary))
            count_var.set(f"{len(rows)} formula/topic entries")
            show_detail()

        query_var.trace_add("write", refresh)
        engine_var.trace_add("write", refresh)
        external_var.trace_add("write", refresh)
        tree.bind("<<TreeviewSelect>>", show_detail)
        tree.bind("<Double-1>", lambda _event: insert_block(selected_entry().support == "External V1" if selected_entry() else False))
        refresh()
        query_entry.focus_set()

    def _parse(self) -> tuple[ExternalReportSpec, ExternalReportEngine]:
        text = self.md_text.get("1.0", "end-1c")
        self.spec = parse_external_report_md(text, from_text=True)
        if not self.spec.operations:
            raise ValueError(
                "Report MD has no External executable blocks. In Formula Finder choose a formula marked External V1, "
                "then click 'Use in External Preview' to insert a ### Scalar block. A ### CM Formula block is only for CM Report Template compilation."
            )
        return self.spec, ExternalReportEngine(self.spec)

    def _run(self, label: str, work, done) -> None:
        self.status_var.set(label)
        def target():
            try:
                value = work()
                self.top.after(0, lambda: done(value))
            except Exception as exc:
                self.top.after(0, lambda error=exc: self._fail(error))
        threading.Thread(target=target, daemon=True).start()

    def _preflight(self) -> None:
        try:
            _spec, engine = self._parse()
        except Exception as exc:
            self._fail(exc)
            return
        self._run("Reading CMBX metadata and audit requirements...", lambda: (engine.load_packages(self.paths), engine), self._show_preflight)

    def _show_preflight(self, payload) -> None:
        self.packages, engine = payload
        rows = engine.compatibility_matrix(self.packages)
        self.compat_tree.delete(*self.compat_tree.get_children())
        self.row_keys.clear()
        for index, row in enumerate(rows):
            iid = str(index)
            package = next(package for package in self.packages if package.path == row.package_path)
            self.row_keys[iid] = (str(package.path.resolve()), row.injection_id)
            self.compat_tree.insert("", "end", iid=iid, values=(row.package_path.name, row.sequence_name, row.injection_name, "compatible" if row.compatible else "blocked", row.detail))
        compatible = sum(row.compatible for row in rows)
        self.status_var.set(f"Preflight complete: {compatible}/{len(rows)} injection(s) compatible.")
        self._log(f"Preflight: {compatible}/{len(rows)} compatible")

    def _preview_selected(self) -> None:
        selected_iids = self.compat_tree.selection()
        selected = {self.row_keys[iid] for iid in selected_iids if iid in self.row_keys}
        if not selected:
            messagebox.showinfo("External Report Engine", "Select one or more compatible injection rows in Compatibility first.", parent=self.top)
            return
        self._execute(selected)

    def _preview_all(self) -> None:
        self._execute(None)

    def _execute(self, selected) -> None:
        try:
            _spec, engine = self._parse()
        except Exception as exc:
            self._fail(exc)
            return
        def work():
            packages = self.packages or engine.load_packages(self.paths)
            return packages, engine.execute(packages, selected)
        self._run("Calculating report preview...", work, self._show_results)

    def _show_results(self, payload) -> None:
        self.packages, self.results = payload
        self.summary_tree.delete(*self.summary_tree.get_children())
        self.table_tree.delete(*self.table_tree.get_children())
        plot_names: list[str] = []
        for result_index, result in enumerate(self.results):
            for value in result.values:
                self.summary_tree.insert("", "end", values=(result.package_path.name, result.sequence_name, result.injection_name, value.label, value.value, value.status, value.detail))
            for error in result.errors:
                self.summary_tree.insert("", "end", values=(result.package_path.name, result.sequence_name, result.injection_name, "Error", "", "blocked", error))
            for table_id, rows in result.tables.items():
                for row in rows:
                    self.table_tree.insert("", "end", values=(result.package_path.name, result.injection_name, table_id, row.get("time_min", ""), row.get("device", ""), row.get("property", row.get("edge", "")), row.get("value", ""), row.get("message", "")))
            for plot_id in result.plots:
                plot_names.append(f"{result_index}: {result.package_path.name} / {result.injection_name} / {plot_id}")
        self.plot_selector["values"] = plot_names
        if plot_names:
            self.plot_selector.current(0)
            self._draw_plot()
        self.status_var.set(f"Preview complete: {len(self.results)} injection report(s).")
        self._log(f"Executed report for {len(self.results)} injection(s)")

    def _draw_plot(self) -> None:
        canvas = self.plot_canvas
        canvas.delete("all")
        selection = self.plot_selector.get()
        if not selection or not self.results:
            return
        try:
            result_index = int(selection.split(":", 1)[0])
            plot_id = selection.rsplit(" / ", 1)[1]
            points = self.results[result_index].plots[plot_id]
        except (ValueError, IndexError, KeyError):
            return
        width, height = max(100, canvas.winfo_width()), max(100, canvas.winfo_height())
        margin = 45
        if len(points) < 2:
            canvas.create_text(width / 2, height / 2, text="No plot points")
            return
        xs = [point.time_min for point in points]
        ys = [point.value for point in points]
        xmin, xmax, ymin, ymax = min(xs), max(xs), min(ys), max(ys)
        if xmax == xmin: xmax += 1
        if ymax == ymin: ymax += 1
        coords = []
        for point in points:
            coords.extend((margin + (point.time_min - xmin) / (xmax - xmin) * (width - 2 * margin), height - margin - (point.value - ymin) / (ymax - ymin) * (height - 2 * margin)))
        canvas.create_line(margin, height - margin, width - margin, height - margin, fill="#64748B")
        canvas.create_line(margin, margin, margin, height - margin, fill="#64748B")
        canvas.create_line(*coords, fill="#2563EB", width=2)
        canvas.create_text(width / 2, 18, text=selection)
        canvas.create_text(width / 2, height - 14, text=f"Time (min): {xmin:.3g} .. {xmax:.3g}")
        canvas.create_text(12, height / 2, text=f"{ymin:.3g}\n..\n{ymax:.3g}", anchor="w")

    def _export(self) -> None:
        if not self.spec or not self.results:
            messagebox.showinfo("External Report Engine", "Run a preview before exporting.", parent=self.top)
            return
        default = self.output_folder / "external_reports" / f"{self.spec.name}.xlsx"
        default.parent.mkdir(parents=True, exist_ok=True)
        name = filedialog.asksaveasfilename(parent=self.top, title="Export report workbook", initialdir=str(default.parent), initialfile=default.name, defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
        if name:
            path = write_external_report_workbook(self.spec, self.results, name)
            self.status_var.set(f"Exported {path}")

    def _log(self, text: str) -> None:
        self.log_text.configure(state="normal")
        self.log_text.insert("end", text + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _fail(self, exc: Exception) -> None:
        self.status_var.set(f"Error: {exc}")
        self._log(f"ERROR: {exc}")
        messagebox.showerror("External Report Engine", str(exc), parent=self.top)
