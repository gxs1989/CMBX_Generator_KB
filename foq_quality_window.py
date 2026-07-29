from __future__ import annotations

import argparse
import csv
import json
import queue
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk

from business_ui_components import RoundedButton, enable_dpi_awareness
from db_upload_service import DatabaseUploadConfig, fetch_table_rows, list_database_tables, test_database_connection
from foq_quality_service import (
    FoqMetricResult,
    attach_history,
    coerce_number,
    default_mapping_path,
    evaluate_candidate,
    filter_database_rows,
    filter_history_for_device,
    inspect_foq_sources,
    metric_catalog_for_devices,
    summarize_history,
)
from read_analyze_service import discover_cmbx_paths
from windows_credentials import protect_secret, unprotect_secret


DEFAULT_WORKSPACE = Path(r"C:\ProgramData\CMBX Data Explorer Workspace")
DEFAULT_CONFIG = DEFAULT_WORKSPACE / "database_config.json"
DEFAULT_EXPORT = DEFAULT_WORKSPACE / "exports" / "foq_quick_check"
DEFAULT_METRIC_PRESETS = DEFAULT_WORKSPACE / "foq_metric_presets.json"


class FoqQualityWindow:
    TASKS = {
        "foq": ("FOQ Quick Check", "Calculate every mapped result, review SPEC status and compare completed CMBX files with history."),
        "quality": ("Quality Data & Database", "Read historical production data and inspect metric trends with QC control limits."),
    }

    def __init__(self, root: tk.Tk, task: str = "foq"):
        self.root = root
        self.task = task if task in self.TASKS else "foq"
        self.colors = {
            "bg": "#FFFFFF", "surface": "#FFFFFF", "alt": "#F6F7F9", "border": "#E1E4E8",
            "text": "#202124", "muted": "#73777F", "primary": "#3598F5", "hover": "#2389EB",
            "soft": "#EAF4FE", "success": "#158A52", "warning": "#B26A00", "danger": "#C53C37",
        }
        self.source_paths: list[Path] = []
        self.candidates = []
        self.inventory = []
        self.selected_sequence_ids: set[tuple[str, str]] = set()
        self.selected_injection_ids: dict[tuple[str, str], set[str]] = {}
        self.inventory_by_iid = {}
        self.injection_by_iid = {}
        self.metrics: list[FoqMetricResult] = []
        self.history_rows: list[dict[str, object]] = []
        self.db_rows: list[dict[str, object]] = []
        self.database_tables: list[tuple[str, str]] = []
        self.ui_queue: queue.Queue = queue.Queue()
        self.mapping_var = tk.StringVar(value=str(default_mapping_path()))
        self.status_var = tk.StringVar(value="Ready")
        self.metric_var = tk.StringVar()
        self.metric_filter_var = tk.StringVar()
        self.selected_metric_fields: set[str] = set()
        self.metric_scope_confirmed = False
        self.history_scope_confirmed = False
        self.history_use_var = tk.BooleanVar(value=True)
        self.history_table_var = tk.StringVar(value="dbo.VTCC")
        self.history_model_var = tk.StringVar()
        self.history_variant_var = tk.StringVar()
        self.history_timebase_var = tk.StringVar()
        self.history_date_from_var = tk.StringVar()
        self.history_date_to_var = tk.StringVar()
        self.history_selected_models: set[str] = set()
        self.history_selected_variants: set[str] = set()
        self.history_selected_timebases: set[str] = set()
        self.history_scope_rows: list[dict[str, object]] = []
        self.table_var = tk.StringVar(value="dbo.VTCC")
        self.history_limit_var = tk.StringVar(value="5000")
        self.db_vars = self._database_defaults()
        self._setup()
        self._build_shell()
        self.root.after(50,self._drain_ui_queue)
        self.show_task()

    def _font(self, size: int, weight: str = "normal"):
        return ("Segoe UI", size, weight)

    def _setup(self) -> None:
        title, _description = self.TASKS[self.task]
        self.root.title(title)
        self.root.geometry("1540x920")
        self.root.minsize(1120, 720)
        self.root.configure(bg=self.colors["bg"])
        try:
            self.root.state("zoomed")
        except tk.TclError:
            pass
        style = ttk.Style(self.root)
        style.configure("Quality.Treeview", font=self._font(9), rowheight=28, background="#FFFFFF", fieldbackground="#FFFFFF")
        style.configure("Quality.Treeview.Heading", font=self._font(9, "bold"), background="#F1F2F4")
        style.configure("Quality.TCombobox", font=self._font(9), padding=5)

    def _build_shell(self) -> None:
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        header = tk.Frame(self.root, bg=self.colors["surface"], height=78, highlightthickness=1, highlightbackground=self.colors["border"])
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.columnconfigure(1, weight=1)
        tk.Label(header, text="Quality Control & Database", font=self._font(19, "bold"), bg=self.colors["surface"], fg=self.colors["text"]).grid(row=0, column=0, sticky="w", padx=28, pady=(14, 2))
        self.scope_label = tk.Label(header, text=self.TASKS[self.task][0], font=self._font(9), bg=self.colors["surface"], fg=self.colors["muted"])
        self.scope_label.grid(row=1, column=0, sticky="w", padx=28, pady=(0, 12))
        other = "quality" if self.task == "foq" else "foq"
        self._button(header, self.TASKS[other][0], lambda: self._switch_task(other), neutral=True, width=205).grid(row=0, column=2, rowspan=2, padx=28, pady=17)
        self.content = tk.Frame(self.root, bg=self.colors["bg"])
        self.content.grid(row=1, column=0, sticky="nsew")
        self.content.rowconfigure(0, weight=1)
        self.content.columnconfigure(0, weight=1)
        footer = tk.Frame(self.root, bg=self.colors["surface"], height=88, highlightthickness=1, highlightbackground=self.colors["border"])
        footer.grid(row=2, column=0, sticky="ew")
        footer.grid_propagate(False)
        footer.columnconfigure(0, weight=1)
        tk.Label(footer, text="Progress", font=self._font(8, "bold"), bg=self.colors["surface"], fg=self.colors["muted"]).grid(row=0, column=0, sticky="w", padx=28, pady=(8, 1))
        self.log = tk.Text(footer, height=2, relief="flat", bd=0, bg=self.colors["surface"], fg=self.colors["muted"], font=self._font(8), wrap="word")
        self.log.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 8))

    def _button(self, parent, text, command, *, neutral=False, width=145):
        return RoundedButton(parent, text, command, width=width, height=42, radius=9,
            bg=self.colors["surface"] if neutral else self.colors["primary"],
            hover_bg=self.colors["alt"] if neutral else self.colors["hover"],
            fg=self.colors["text"] if neutral else "#FFFFFF",
            border=self.colors["border"] if neutral else self.colors["primary"],
            parent_bg=str(parent.cget("bg")), font=self._font(9, "bold"))

    def _switch_task(self, task: str) -> None:
        self.task = task
        self.scope_label.configure(text=self.TASKS[task][0])
        self.show_task()

    def _page(self):
        for child in self.content.winfo_children():
            child.destroy()
        page = tk.Frame(self.content, bg=self.colors["bg"])
        page.grid(row=0, column=0, sticky="nsew", padx=28, pady=22)
        page.columnconfigure(0, weight=1)
        return page

    def _heading(self, page, title: str, description: str, steps: tuple[str, ...], active: int):
        tk.Label(page, text=title, font=self._font(20, "bold"), bg=self.colors["bg"], fg=self.colors["text"]).grid(row=0, column=0, sticky="w")
        tk.Label(page, text=description, font=self._font(10), bg=self.colors["bg"], fg=self.colors["muted"], wraplength=1120, justify="left").grid(row=1, column=0, sticky="w", pady=(4, 12))
        bar = tk.Frame(page, bg=self.colors["bg"])
        bar.grid(row=2, column=0, sticky="w", pady=(0, 14))
        for index, label in enumerate(steps):
            color = self.colors["success"] if index < active else self.colors["primary"] if index == active else "#E9EAEC"
            fg = "#FFFFFF" if index <= active else self.colors["muted"]
            tk.Label(bar, text=str(index + 1), width=3, padx=3, pady=6, font=self._font(9, "bold"), bg=color, fg=fg).pack(side="left")
            tk.Label(bar, text=label, padx=9, font=self._font(9, "bold" if index == active else "normal"), bg=self.colors["bg"], fg=self.colors["primary"] if index == active else self.colors["muted"]).pack(side="left")
            if index < len(steps) - 1:
                tk.Frame(bar, width=32, height=1, bg=self.colors["border"]).pack(side="left", padx=3)

    def show_task(self) -> None:
        if self.task == "foq":
            self._show_foq()
        else:
            self._show_quality()

    def _show_foq(self) -> None:
        page = self._page()
        active_step=3 if self.metrics else 2 if self.history_scope_confirmed else 1 if self.metric_scope_confirmed else 0
        self._heading(page, *self.TASKS["foq"], ("Choose CMBX & injections", "Choose metrics", "Filter database", "Review results"), active_step)
        page.rowconfigure(5, weight=1)
        controls = tk.Frame(page, bg=self.colors["alt"], highlightthickness=1, highlightbackground=self.colors["border"])
        controls.grid(row=3, column=0, sticky="ew", pady=(0, 12))
        controls.columnconfigure(1, weight=1)
        self._button(controls, "Add CMBX", self._add_files, width=120).grid(row=0, column=0, padx=(14, 6), pady=12)
        action_group=tk.Frame(controls,bg=self.colors["alt"])
        action_group.grid(row=0,column=1,sticky="e",padx=(6,14),pady=8)
        self._button(action_group, "Add folder", self._add_folder, neutral=True, width=112).pack(side="left",padx=5)
        self._button(action_group, "Clear", self._clear_sources, neutral=True, width=78).pack(side="left",padx=5)
        self._button(action_group, "Choose metrics", self._choose_metrics, neutral=True, width=130).pack(side="left",padx=5)
        self._button(action_group, "Database scope", self._history_comparison_dialog, neutral=True, width=145).pack(side="left",padx=5)
        self._button(action_group, "Run analysis", self._run_foq, width=130).pack(side="left",padx=(14,0))
        tk.Label(controls, text="FOQ Location", font=self._font(9, "bold"), bg=self.colors["alt"], fg=self.colors["text"]).grid(row=1, column=0, padx=(14, 6), pady=(0,12),sticky="w")
        location_row=tk.Frame(controls,bg=self.colors["alt"]);location_row.grid(row=1,column=1,sticky="ew",padx=(0,14),pady=(0,12));location_row.columnconfigure(0,weight=1)
        tk.Entry(location_row, textvariable=self.mapping_var, font=self._font(9), relief="solid", bd=1).grid(row=0, column=0, sticky="ew", ipady=6, padx=(0,8))
        self._button(location_row, "Browse", self._browse_mapping, neutral=True, width=88).grid(row=0, column=1)

        source_shell=tk.Frame(page,bg=self.colors["surface"])
        source_shell.grid(row=4,column=0,sticky="ew",pady=(0,10));source_shell.columnconfigure(0,weight=1)
        tk.Label(source_shell,text="CMBX and Sequence scope",font=self._font(10,"bold"),bg=self.colors["surface"],fg=self.colors["text"]).grid(row=0,column=0,sticky="w",pady=(0,4))
        self.source_tree=ttk.Treeview(source_shell,columns=("selected","device","report","status"),show="tree headings",height=7,style="Quality.Treeview",selectmode="browse")
        self.source_tree.heading("#0",text="CMBX / Sequence");self.source_tree.column("#0",width=390,minwidth=220,stretch=True)
        for column,title,width in (("selected","Use",55),("device","Device",110),("report","Report Template",210),("status","Status",260)):
            self.source_tree.heading(column,text=title);self.source_tree.column(column,width=width,minwidth=50,stretch=column=="status")
        source_y=ttk.Scrollbar(source_shell,orient="vertical",command=self.source_tree.yview);self.source_tree.configure(yscrollcommand=source_y.set)
        self.source_tree.grid(row=1,column=0,sticky="ew");source_y.grid(row=1,column=1,sticky="ns")
        self.source_tree.tag_configure("eligible",foreground=self.colors["primary"]);self.source_tree.tag_configure("support",foreground=self.colors["muted"])
        self.source_tree.bind("<ButtonRelease-1>",self._toggle_sequence_scope)
        self._fill_source_tree()

        body = tk.PanedWindow(page, orient="horizontal", sashwidth=5, bg=self.colors["border"], bd=0)
        body.grid(row=5, column=0, sticky="nsew")
        left = tk.Frame(body, bg=self.colors["surface"])
        right = tk.Frame(body, bg=self.colors["surface"])
        body.add(left, minsize=760, stretch="always")
        body.add(right, minsize=350, stretch="always")
        left.rowconfigure(1, weight=1); left.columnconfigure(0, weight=1)
        toolbar = tk.Frame(left, bg=self.colors["surface"])
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        self.summary_label = tk.Label(toolbar, text=self._foq_summary(), font=self._font(10, "bold"), bg=self.colors["surface"], fg=self.colors["text"])
        self.summary_label.pack(side="left")
        self._button(toolbar, "Export CSV", self._export_foq, neutral=True, width=110).pack(side="right")
        columns = ("context", "device", "field", "value", "unit", "spec", "history", "mean", "delta", "source")
        self.foq_tree = ttk.Treeview(left, columns=columns, show="headings", style="Quality.Treeview", selectmode="browse")
        headings = {"context":"CMBX / Sequence", "device":"Device", "field":"Metric", "value":"Value", "unit":"Unit", "spec":"SPEC", "history":"History", "mean":"History mean", "delta":"Delta", "source":"Evidence"}
        widths = {"context":155,"device":82,"field":128,"value":76,"unit":48,"spec":64,"history":82,"mean":78,"delta":68,"source":145}
        for col in columns:
            self.foq_tree.heading(col, text=headings[col]); self.foq_tree.column(col, width=widths[col], minwidth=55, stretch=col in {"sequence","field","source"})
        y = ttk.Scrollbar(left, orient="vertical", command=self.foq_tree.yview); x = ttk.Scrollbar(left, orient="horizontal", command=self.foq_tree.xview)
        self.foq_tree.configure(yscrollcommand=y.set, xscrollcommand=x.set)
        self.foq_tree.grid(row=1, column=0, sticky="nsew"); y.grid(row=1,column=1,sticky="ns"); x.grid(row=2,column=0,sticky="ew")
        self.foq_tree.tag_configure("fail", foreground=self.colors["danger"])
        self.foq_tree.tag_configure("pass", foreground=self.colors["success"])
        self.foq_tree.tag_configure("warn", foreground=self.colors["warning"])
        self.foq_tree.bind("<<TreeviewSelect>>", lambda _event: self._draw_foq_chart())
        self._fill_foq_tree()

        right.rowconfigure(2, weight=1); right.columnconfigure(0, weight=1)
        tk.Label(right, text="Metric comparison", font=self._font(12, "bold"), bg=self.colors["surface"], fg=self.colors["text"]).grid(row=0,column=0,sticky="w",padx=14,pady=(8,3))
        fields = sorted({row.db_field for row in self.metrics if coerce_number(row.value) is not None})
        self.metric_combo = ttk.Combobox(right, textvariable=self.metric_var, values=fields, state="readonly", style="Quality.TCombobox")
        self.metric_combo.grid(row=1,column=0,sticky="ew",padx=14,pady=(2,8)); self.metric_combo.bind("<<ComboboxSelected>>", lambda _event:self._draw_foq_chart())
        if fields and self.metric_var.get() not in fields: self.metric_var.set(fields[0])
        self.chart = tk.Canvas(right, bg="#FFFFFF", highlightthickness=1, highlightbackground=self.colors["border"])
        self.chart.grid(row=2,column=0,sticky="nsew",padx=14,pady=(0,12)); self.chart.bind("<Configure>", lambda _event:self._draw_foq_chart())
        self.root.after_idle(self._draw_foq_chart)

    def _show_quality(self) -> None:
        page = self._page()
        self._heading(page, *self.TASKS["quality"], ("Connect database", "Choose table and metric", "Review QC curve"), 0 if not self.db_rows else 2)
        page.rowconfigure(4, weight=1)
        controls = tk.Frame(page, bg=self.colors["alt"], highlightthickness=1, highlightbackground=self.colors["border"])
        controls.grid(row=3,column=0,sticky="ew",pady=(0,12)); controls.columnconfigure(2,weight=1)
        self._button(controls,"Database settings",self._database_dialog,neutral=True,width=155).grid(row=0,column=0,padx=(14,6),pady=12)
        self._button(controls,"Connect",self._connect_database,width=105).grid(row=0,column=1,padx=6,pady=12)
        self.table_combo = ttk.Combobox(controls,textvariable=self.table_var,values=[f"{s}.{t}" for s,t in self.database_tables],style="Quality.TCombobox")
        self.table_combo.grid(row=0,column=2,sticky="ew",padx=8)
        tk.Label(controls,text="Rows",font=self._font(9),bg=self.colors["alt"],fg=self.colors["muted"]).grid(row=0,column=3,padx=(8,2))
        tk.Entry(controls,textvariable=self.history_limit_var,width=8,font=self._font(9)).grid(row=0,column=4,ipady=6)
        self._button(controls,"Load history",self._load_quality_table,width=125).grid(row=0,column=5,padx=(10,14))
        body=tk.PanedWindow(page,orient="horizontal",sashwidth=5,bg=self.colors["border"],bd=0); body.grid(row=4,column=0,sticky="nsew")
        left=tk.Frame(body,bg=self.colors["surface"]); right=tk.Frame(body,bg=self.colors["surface"]); body.add(left,minsize=480); body.add(right,minsize=560,stretch="always")
        left.rowconfigure(5,weight=1); left.columnconfigure(0,weight=1); right.rowconfigure(1,weight=1); right.columnconfigure(0,weight=1)
        tk.Label(left,text="Find metric",font=self._font(10,"bold"),bg=self.colors["surface"],fg=self.colors["text"]).grid(row=0,column=0,sticky="w",padx=12,pady=(10,3))
        metric_search=tk.Entry(left,textvariable=self.metric_filter_var,font=self._font(9),relief="solid",bd=1)
        metric_search.grid(row=1,column=0,sticky="ew",padx=12,ipady=6);metric_search.bind("<KeyRelease>",lambda _event:self._refresh_quality_metric_options())
        tk.Label(left,text="Metric",font=self._font(9,"bold"),bg=self.colors["surface"],fg=self.colors["muted"]).grid(row=2,column=0,sticky="w",padx=12,pady=(8,3))
        numeric=self._numeric_db_fields(); self.quality_metric_combo=ttk.Combobox(left,textvariable=self.metric_var,values=numeric,state="readonly",style="Quality.TCombobox")
        self.quality_metric_combo.grid(row=3,column=0,sticky="ew",padx=12,pady=(0,8)); self.quality_metric_combo.bind("<<ComboboxSelected>>",lambda _event:self._refresh_quality_view())
        if numeric and self.metric_var.get() not in numeric:self.metric_var.set(numeric[0])
        self.quality_summary=tk.Label(left,text="Load a database table to calculate QC statistics.",font=self._font(10),bg=self.colors["soft"],fg=self.colors["text"],justify="left",anchor="nw",padx=14,pady=12,wraplength=420)
        self.quality_summary.grid(row=4,column=0,sticky="ew",padx=12,pady=(0,8))
        history_shell=tk.Frame(left,bg=self.colors["surface"]);history_shell.grid(row=5,column=0,sticky="nsew",padx=12,pady=(0,12));history_shell.rowconfigure(0,weight=1);history_shell.columnconfigure(0,weight=1)
        self.history_tree=ttk.Treeview(history_shell,show="headings",style="Quality.Treeview")
        history_y=ttk.Scrollbar(history_shell,orient="vertical",command=self.history_tree.yview);history_x=ttk.Scrollbar(history_shell,orient="horizontal",command=self.history_tree.xview)
        self.history_tree.configure(yscrollcommand=history_y.set,xscrollcommand=history_x.set);self.history_tree.grid(row=0,column=0,sticky="nsew");history_y.grid(row=0,column=1,sticky="ns");history_x.grid(row=1,column=0,sticky="ew")
        tk.Label(right,text="Individuals control chart",font=self._font(12,"bold"),bg=self.colors["surface"],fg=self.colors["text"]).grid(row=0,column=0,sticky="w",padx=14,pady=(10,5))
        self.chart=tk.Canvas(right,bg="#FFFFFF",highlightthickness=1,highlightbackground=self.colors["border"]); self.chart.grid(row=1,column=0,sticky="nsew",padx=14,pady=(0,12)); self.chart.bind("<Configure>",lambda _event:self._draw_quality_chart())
        self._refresh_quality_view()

    def _add_files(self):
        paths=filedialog.askopenfilenames(parent=self.root,title="Add completed CMBX",filetypes=[("CMBX packages","*.cmbx")])
        self._add_source_paths(Path(path) for path in paths)

    def _add_folder(self):
        folder=filedialog.askdirectory(parent=self.root,title="Add CMBX folder")
        if folder:self._add_source_paths(discover_cmbx_paths([folder]))

    def _add_source_paths(self, paths):
        known={str(path).lower() for path in self.source_paths}
        for path in paths:
            path=Path(path)
            if str(path).lower() not in known:self.source_paths.append(path);known.add(str(path).lower())
        self.status_var.set(f"{len(self.source_paths)} CMBX file(s) selected")
        self._log(self.status_var.get()); self._scan_source_inventory()

    def _clear_sources(self):
        self.source_paths=[];self.candidates=[];self.inventory=[];self.selected_sequence_ids=set();self.selected_injection_ids={};self.metrics=[];self.history_rows=[];self.metric_scope_confirmed=False;self.history_scope_confirmed=False;self.show_task()

    def _scan_source_inventory(self):
        mapping=Path(self.mapping_var.get())
        if not mapping.exists():
            self._fail(f"FOQ Location file not found:\n{mapping}");return
        self._log("Expanding CMBX packages and identifying sequence candidates...")
        paths=list(self.source_paths)
        def work():
            inventory,errors=inspect_foq_sources(paths,mapping)
            self._call_ui(lambda:self._finish_source_inventory(inventory,errors))
        threading.Thread(target=work,daemon=True).start()

    def _finish_source_inventory(self,inventory,errors):
        self.inventory=inventory
        self.selected_sequence_ids={self._sequence_key(item) for item in inventory if item.eligible}
        self.selected_injection_ids={}
        for item in inventory:
            if not item.eligible:continue
            injections=[child for child in item.sequence.children if child.kind=="injection"]
            counts={name:sum(child.name.strip().lower()==name for child in injections) for name in {child.name.strip().lower() for child in injections}}
            selected={injection.id for injection in injections if injection.id and counts[injection.name.strip().lower()]==1}
            self.selected_injection_ids[self._sequence_key(item)]=selected
        catalog=self._metric_catalog()
        if not self.selected_metric_fields:
            self.selected_metric_fields=set(catalog)
        else:
            self.selected_metric_fields.intersection_update(catalog)
        self.history_selected_models={item.device for item in inventory if item.eligible}
        self.history_selected_variants=set();self.history_selected_timebases=set();self.history_date_from_var.set("");self.history_date_to_var.set("")
        self.metric_scope_confirmed=False;self.history_scope_confirmed=False;self.metrics=[]
        ready=sum(item.eligible for item in inventory);support=len(inventory)-ready
        self._log(f"Sequence scope ready: {ready} checkable, {support} support/unresolved, {len(errors)} package error(s).")
        for path,detail in errors:self._log(f"  {path.name}: {detail}")
        self.show_task()

    def _fill_source_tree(self):
        if not hasattr(self,"source_tree"):return
        self.source_tree.delete(*self.source_tree.get_children());self.inventory_by_iid={};self.injection_by_iid={}
        package_nodes={}
        for index,item in enumerate(self.inventory):
            package_key=str(item.package.path).lower()
            parent=package_nodes.get(package_key)
            if parent is None:
                parent=f"pkg:{len(package_nodes)}";package_nodes[package_key]=parent
                self.source_tree.insert("","end",iid=parent,text=item.package.path.name,values=("","","",""),open=True,tags=("eligible",))
            iid=f"seq:{index}";self.inventory_by_iid[iid]=item
            selected="✓" if self._sequence_key(item) in self.selected_sequence_ids else ""
            sequence_status=item.reason
            if item.eligible:
                pending=sum(text.startswith(item.sequence.name+" /") for text in self._unresolved_duplicate_groups())
                if pending:sequence_status=f"Choose {pending} duplicate injection occurrence(s)"
            self.source_tree.insert(parent,"end",iid=iid,text=item.sequence.name,values=(selected,item.device,item.report_template,sequence_status),open=item.eligible,tags=("eligible" if item.eligible else "support",))
            if item.eligible:
                injections=[child for child in item.sequence.children if child.kind=="injection"]
                counts={name:sum(child.name.strip().lower()==name for child in injections) for name in {child.name.strip().lower() for child in injections}}
                occurrences={}
                for injection_index,injection in enumerate(injections):
                    name_key=injection.name.strip().lower();occurrences[name_key]=occurrences.get(name_key,0)+1
                    injection_iid=f"inj:{index}:{injection_index}";self.injection_by_iid[injection_iid]=(item,injection)
                    chosen="✓" if injection.id in self.selected_injection_ids.get(self._sequence_key(item),set()) else ""
                    if counts[name_key]>1:
                        detail=("Selected" if chosen else "Choose one")+f" • duplicate {occurrences[name_key]}/{counts[name_key]}"
                    else:detail="Injection"
                    self.source_tree.insert(iid,"end",iid=injection_iid,text=injection.name,values=(chosen,"","",detail),tags=("eligible",))

    def _toggle_sequence_scope(self,event):
        iid=self.source_tree.identify_row(event.y)
        if not iid:return
        injection_item=self.injection_by_iid.get(iid)
        if injection_item is not None:
            item,injection=injection_item;sequence_key=self._sequence_key(item);chosen=self.selected_injection_ids.setdefault(sequence_key,set())
            same_name=[child for child in item.sequence.children if child.kind=="injection" and child.name.strip().lower()==injection.name.strip().lower()]
            if len(same_name)>1:
                chosen.difference_update(child.id for child in same_name)
                if injection.id:chosen.add(injection.id)
            elif injection.id in chosen:chosen.remove(injection.id)
            elif injection.id:chosen.add(injection.id)
            self.metrics=[];self._fill_source_tree();return
        item=self.inventory_by_iid.get(iid)
        if item is not None:
            if not item.eligible:return
            key=self._sequence_key(item)
            if key in self.selected_sequence_ids:self.selected_sequence_ids.remove(key)
            else:self.selected_sequence_ids.add(key)
        elif iid.startswith("pkg:"):
            children=[self.inventory_by_iid[child] for child in self.source_tree.get_children(iid) if child in self.inventory_by_iid and self.inventory_by_iid[child].eligible]
            keys={self._sequence_key(child) for child in children}
            if keys and keys.issubset(self.selected_sequence_ids):self.selected_sequence_ids-=keys
            else:self.selected_sequence_ids|=keys
        catalog=set(self._metric_catalog())
        self.selected_metric_fields.intersection_update(catalog)
        if catalog and not self.selected_metric_fields:self.selected_metric_fields=set(catalog)
        self.metric_scope_confirmed=False;self.history_scope_confirmed=False;self.metrics=[]
        self._fill_source_tree()

    def _metric_catalog(self):
        devices={item.device for item in self.inventory if item.eligible and self._sequence_key(item) in self.selected_sequence_ids}
        try:
            return metric_catalog_for_devices(self.mapping_var.get(),devices)
        except Exception as exc:
            self._log(f"Metric catalog unavailable: {exc}")
            return []

    def _choose_metrics(self):
        if not self.inventory:
            return messagebox.showinfo("FOQ Quick Check","Add CMBX files and choose sequences first.",parent=self.root)
        unresolved=self._unresolved_duplicate_groups()
        if unresolved:
            return messagebox.showwarning("FOQ Quick Check",f"Choose one occurrence for each duplicate injection first:\n\n{unresolved[0]}",parent=self.root)
        catalog=self._metric_catalog()
        if not catalog:
            return messagebox.showwarning("FOQ Quick Check","No common numeric FOQ metrics were found for the selected device models.",parent=self.root)
        dialog=tk.Toplevel(self.root);dialog.title("Choose metrics");dialog.transient(self.root);dialog.grab_set();dialog.geometry("650x700");dialog.minsize(500,460);dialog.configure(bg=self.colors["bg"])
        dialog.rowconfigure(4,weight=1);dialog.columnconfigure(0,weight=1)
        tk.Label(dialog,text="Choose metrics to calculate",font=self._font(15,"bold"),bg=self.colors["bg"],fg=self.colors["text"]).grid(row=0,column=0,sticky="w",padx=22,pady=(18,4))
        tk.Label(dialog,text="For multiple device models, only common mapped metrics are listed.",font=self._font(9),bg=self.colors["bg"],fg=self.colors["muted"]).grid(row=1,column=0,sticky="w",padx=22,pady=(0,10))
        presets=self._load_metric_presets();preset_var=tk.StringVar()
        preset_row=tk.Frame(dialog,bg=self.colors["bg"]);preset_row.grid(row=2,column=0,sticky="ew",padx=22,pady=(0,9));preset_row.columnconfigure(0,weight=1)
        preset_combo=ttk.Combobox(preset_row,textvariable=preset_var,values=sorted(presets),state="readonly",style="Quality.TCombobox");preset_combo.grid(row=0,column=0,sticky="ew",padx=(0,6))
        search_var=tk.StringVar();search=tk.Entry(dialog,textvariable=search_var,font=self._font(10),relief="solid",bd=1);search.grid(row=3,column=0,sticky="ew",padx=22,ipady=7)
        shell=tk.Frame(dialog,bg=self.colors["bg"]);shell.grid(row=4,column=0,sticky="nsew",padx=22,pady=10);shell.rowconfigure(0,weight=1);shell.columnconfigure(0,weight=1)
        listing=tk.Listbox(shell,selectmode="extended",exportselection=False,font=self._font(10),relief="solid",bd=1,activestyle="none")
        scroll=ttk.Scrollbar(shell,orient="vertical",command=listing.yview);listing.configure(yscrollcommand=scroll.set);listing.grid(row=0,column=0,sticky="nsew");scroll.grid(row=0,column=1,sticky="ns")
        chosen=set(self.selected_metric_fields);visible=[]
        def remember():
            for field in visible:chosen.discard(field)
            chosen.update(visible[index] for index in listing.curselection())
        def refill(*_args):
            nonlocal visible
            query=search_var.get().strip().lower();visible=[field for field in catalog if query in field.lower()]
            listing.delete(0,"end")
            for index,field in enumerate(visible):
                listing.insert("end",field)
                if field in chosen:listing.selection_set(index)
        def change_filter(*_args):remember();refill()
        def select_all():chosen.update(catalog);refill()
        def clear_all():chosen.clear();refill()
        def load_preset():
            chosen.clear();chosen.update(field for field in presets.get(preset_var.get(),[]) if field in catalog);refill()
        def save_preset():
            remember();name=simpledialog.askstring("Save metric set","Metric set name:",parent=dialog)
            if not name:return
            presets[name.strip()]=sorted(chosen);self._save_metric_presets(presets);preset_combo.configure(values=sorted(presets));preset_var.set(name.strip());self._log(f"Saved metric set: {name.strip()}")
        def apply():
            remember()
            if not chosen:return messagebox.showwarning("Choose metrics","Select at least one metric.",parent=dialog)
            self.selected_metric_fields=set(chosen);self.metric_scope_confirmed=True;self.history_scope_confirmed=False;self.metrics=[];self._log(f"Metric scope updated: {len(chosen)} selected.");dialog.destroy();self.show_task()
        search_var.trace_add("write",change_filter);refill()
        self._button(preset_row,"Use set",load_preset,neutral=True,width=88).grid(row=0,column=1,padx=3);self._button(preset_row,"Save set",save_preset,neutral=True,width=92).grid(row=0,column=2,padx=(3,0))
        buttons=tk.Frame(dialog,bg=self.colors["bg"]);buttons.grid(row=5,column=0,sticky="ew",padx=22,pady=(0,18))
        self._button(buttons,"All",select_all,neutral=True,width=78).pack(side="left",padx=(0,6));self._button(buttons,"Clear",clear_all,neutral=True,width=78).pack(side="left");self._button(buttons,"Apply",apply,width=100).pack(side="right")

    @staticmethod
    def _load_metric_presets():
        try:
            data=json.loads(DEFAULT_METRIC_PRESETS.read_text(encoding="utf-8"))
            return {str(name):[str(field) for field in fields] for name,fields in data.items() if isinstance(fields,list)}
        except Exception:return {}

    @staticmethod
    def _save_metric_presets(presets):
        DEFAULT_METRIC_PRESETS.parent.mkdir(parents=True,exist_ok=True)
        DEFAULT_METRIC_PRESETS.write_text(json.dumps(presets,ensure_ascii=False,indent=2),encoding="utf-8")

    @staticmethod
    def _sequence_key(item):
        return (str(item.package.path).lower(),item.sequence.id or item.sequence.url or item.sequence.name)

    def _unresolved_duplicate_groups(self):
        unresolved=[]
        for item in self.inventory:
            sequence_key=self._sequence_key(item)
            if not item.eligible or sequence_key not in self.selected_sequence_ids:continue
            selected=self.selected_injection_ids.get(sequence_key,set());groups={}
            for injection in (child for child in item.sequence.children if child.kind=="injection"):
                groups.setdefault(injection.name.strip().lower(),[]).append(injection)
            for injections in groups.values():
                if len(injections)>1 and not any(injection.id in selected for injection in injections):
                    unresolved.append(f"{item.sequence.name} / {injections[0].name} ({len(injections)} occurrences)")
        return unresolved

    def _browse_mapping(self):
        path=filedialog.askopenfilename(parent=self.root,title="Choose FOQ Location workbook",filetypes=[("Excel 97-2003","*.xls"),("Excel","*.xlsx")])
        if path:
            self.mapping_var.set(path)
            if self.source_paths:self._scan_source_inventory()

    def _run_foq(self):
        if not self.source_paths:return messagebox.showwarning("FOQ Quick Check","Add one or more completed CMBX files first.",parent=self.root)
        mapping=Path(self.mapping_var.get())
        if not mapping.exists():return messagebox.showerror("FOQ Quick Check",f"FOQ Location file not found:\n{mapping}",parent=self.root)
        selected=[item.candidate for item in self.inventory if item.candidate is not None and self._sequence_key(item) in self.selected_sequence_ids]
        if not selected:
            if not self.inventory:
                self._scan_source_inventory()
                return messagebox.showinfo("FOQ Quick Check","Sequence scope is being prepared. Select a sequence and run again.",parent=self.root)
            return messagebox.showwarning("FOQ Quick Check","Select at least one checkable sequence.",parent=self.root)
        unresolved=self._unresolved_duplicate_groups()
        if unresolved:return messagebox.showwarning("FOQ Quick Check",f"Choose duplicate injection occurrences before analysis:\n\n"+"\n".join(unresolved),parent=self.root)
        if not self.metric_scope_confirmed or not self.selected_metric_fields:
            return messagebox.showwarning("FOQ Quick Check","Choose at least one metric before running the check.",parent=self.root)
        if not self.history_scope_confirmed:
            return messagebox.showwarning("FOQ Quick Check","Confirm the database comparison scope before running the analysis.",parent=self.root)
        fields=sorted(self.selected_metric_fields)
        self._log(f"Starting FOQ calculation for {len(selected)} selected sequence(s) and {len(fields)} metric(s)...")
        self.status_var.set("FOQ calculation running")
        def work():
            try:
                candidates=selected;errors=[]
                rows=[]
                for index,candidate in enumerate(candidates,1):
                    self._thread_log(f"[{index}/{len(candidates)}] {candidate.sequence.name} / {candidate.device}: calculating mapped report cells")
                    try:
                        injection_ids=self.selected_injection_ids.get(self._sequence_key(candidate),set())
                        rows.extend(evaluate_candidate(candidate,mapping,progress=self._foq_progress,db_fields=fields,selected_injection_ids=injection_ids))
                    except Exception as exc:
                        errors.append((candidate.package.path,f"{candidate.sequence.name}: {exc}"))
                        self._thread_log(f"  Skipped: {exc}")
                self._call_ui(lambda:self._finish_foq(candidates,rows,errors))
            except Exception as exc:self._call_ui(lambda exc=exc:self._fail(str(exc)))
        threading.Thread(target=work,daemon=True).start()

    def _finish_foq(self,candidates,rows,errors):
        self.candidates=candidates;self.metrics=attach_history(rows,self.history_rows) if self.history_rows else rows
        self._log(f"FOQ check complete: {len(candidates)} sequence(s), {len(rows)} mapped value(s), {len(errors)} load error(s).")
        self.show_task()

    def _history_comparison_dialog(self):
        if not self.inventory:return messagebox.showinfo("FOQ Quick Check","Choose completed CMBX sequences first.",parent=self.root)
        if not self.metric_scope_confirmed:return messagebox.showinfo("FOQ Quick Check","Choose and confirm the metric set first.",parent=self.root)
        devices=sorted({item.device for item in self.inventory if item.eligible and self._sequence_key(item) in self.selected_sequence_ids})
        config=self._db_config()
        if self.history_table_var.get() in {"","dbo.VTCC"}:
            self.history_table_var.set(f"{config.schema}.{self._table_name(config,devices[0] if devices else '')}")
        if not self.history_selected_models:self.history_selected_models=set(devices)
        dialog=tk.Toplevel(self.root);dialog.title("Historical database comparison");dialog.transient(self.root);dialog.grab_set();dialog.geometry("760x650");dialog.minsize(650,560);dialog.configure(bg=self.colors["bg"]);dialog.columnconfigure(1,weight=1)
        tk.Label(dialog,text="Historical comparison scope",font=self._font(16,"bold"),bg=self.colors["bg"],fg=self.colors["text"]).grid(row=0,column=0,columnspan=3,sticky="w",padx=22,pady=(20,4))
        source=self.db_vars["dsn"].get().strip() or f"{self.db_vars['server'].get()} / {self.db_vars['database'].get()}"
        tk.Label(dialog,text=f"Source: {source}",font=self._font(9),bg=self.colors["bg"],fg=self.colors["muted"],wraplength=610,justify="left").grid(row=1,column=0,columnspan=3,sticky="w",padx=22,pady=(0,10))
        tk.Checkbutton(dialog,text="Compare current CMBX results with database history",variable=self.history_use_var,bg=self.colors["bg"],fg=self.colors["text"],activebackground=self.colors["bg"],font=self._font(10)).grid(row=2,column=0,columnspan=3,sticky="w",padx=18,pady=6)
        table_values=[f"{schema}.{table}" for schema,table in self.database_tables]
        if self.history_table_var.get() not in table_values:table_values.insert(0,self.history_table_var.get())
        self._scope_row_label(dialog,3,"Table")
        table_combo=ttk.Combobox(dialog,textvariable=self.history_table_var,values=table_values,state="readonly",style="Quality.TCombobox")
        table_combo.grid(row=3,column=1,columnspan=2,sticky="ew",padx=(0,22),pady=7)
        displays={"model":tk.StringVar(value="Loading..."),"variant":tk.StringVar(value="Loading..."),"timebase":tk.StringVar(value="Loading...")}
        choices={"model":[],"variant":[],"timebase":[]}
        selected={"model":self.history_selected_models,"variant":self.history_selected_variants,"timebase":self.history_selected_timebases}
        labels={"model":"ModelNo","variant":"ModelVariant","timebase":"TimeBase"};choice_buttons={}
        for row,key in enumerate(("model","variant","timebase"),start=4):
            self._scope_row_label(dialog,row,labels[key])
            choice_buttons[key]=tk.Button(dialog,textvariable=displays[key],command=lambda key=key:self._select_scope_values(dialog,labels[key],choices[key],selected[key],displays[key]),anchor="w",font=self._font(9),bg="#FFFFFF",fg=self.colors["text"],relief="solid",bd=1,padx=9,pady=7,state="disabled")
            choice_buttons[key].grid(row=row,column=1,columnspan=2,sticky="ew",padx=(0,22),pady=7)
        self._scope_row_label(dialog,7,"TestDate from")
        date_from=ttk.Combobox(dialog,textvariable=self.history_date_from_var,values=("All",),state="readonly",style="Quality.TCombobox");date_from.grid(row=7,column=1,columnspan=2,sticky="ew",padx=(0,22),pady=7)
        self._scope_row_label(dialog,8,"TestDate to")
        date_to=ttk.Combobox(dialog,textvariable=self.history_date_to_var,values=("All",),state="readonly",style="Quality.TCombobox");date_to.grid(row=8,column=1,columnspan=2,sticky="ew",padx=(0,22),pady=7)
        self._scope_row_label(dialog,9,"Maximum rows")
        tk.Spinbox(dialog,textvariable=self.history_limit_var,from_=100,to=100000,increment=100,width=12,font=self._font(9),relief="solid",bd=1).grid(row=9,column=1,sticky="w",pady=7,ipady=5)
        scope_status=tk.StringVar(value="Loading database choices...")
        tk.Label(dialog,textvariable=scope_status,font=self._font(9),bg=self.colors["bg"],fg=self.colors["primary"],wraplength=610,justify="left").grid(row=10,column=0,columnspan=3,sticky="w",padx=22,pady=(7,8))
        def settings():self._database_dialog()
        def apply():
            dialog.destroy()
            if not self.history_use_var.get():
                self.history_rows=[];self.history_scope_confirmed=True;self._log("Historical comparison disabled; SPEC-only analysis selected.");self.show_task();return
            self.history_model_var.set(",".join(sorted(self.history_selected_models)))
            self.history_variant_var.set(",".join(sorted(self.history_selected_variants)))
            self.history_timebase_var.set(",".join(sorted(self.history_selected_timebases)))
            if self.history_date_from_var.get()=="All":self.history_date_from_var.set("")
            if self.history_date_to_var.get()=="All":self.history_date_to_var.set("")
            self._load_filtered_history()
        footer=tk.Frame(dialog,bg=self.colors["bg"]);footer.grid(row=11,column=0,columnspan=3,sticky="ew",padx=22,pady=(12,20))
        self._button(footer,"Database settings",settings,neutral=True,width=155).pack(side="left")
        refresh=self._button(footer,"Refresh choices",lambda:self._load_history_scope_choices(dialog,table_combo,choices,selected,displays,choice_buttons,date_from,date_to,scope_status),neutral=True,width=140);refresh.pack(side="left",padx=6)
        self._button(footer,"Cancel",dialog.destroy,neutral=True,width=90).pack(side="right",padx=(6,0));self._button(footer,"Apply",apply,width=100).pack(side="right")
        table_combo.bind("<<ComboboxSelected>>",lambda _event:self._load_history_scope_choices(dialog,table_combo,choices,selected,displays,choice_buttons,date_from,date_to,scope_status))
        dialog.after(80,lambda:self._load_history_scope_choices(dialog,table_combo,choices,selected,displays,choice_buttons,date_from,date_to,scope_status))

    def _scope_row_label(self,parent,row,text):
        tk.Label(parent,text=text,font=self._font(9,"bold"),bg=self.colors["bg"],fg=self.colors["text"]).grid(row=row,column=0,sticky="w",padx=(22,10),pady=7)

    def _load_history_scope_choices(self,dialog,table_combo,choices,selected,displays,buttons,date_from,date_to,status):
        status.set("Loading available database values...")
        for button in buttons.values():button.configure(state="disabled")
        table_name=self.history_table_var.get().strip()
        def work():
            try:
                config=self._db_config();tables=list_database_tables(config)
                schema=config.schema;table=table_name
                if "." in table:schema,table=table.split(".",1)
                rows=fetch_table_rows(config,table=table,schema=schema,limit=self._limit())
                self._call_ui(lambda:self._finish_history_scope_choices(dialog,tables,rows,table_combo,choices,selected,displays,buttons,date_from,date_to,status))
            except Exception as exc:self._call_ui(lambda exc=exc:status.set(f"Could not load choices: {exc}"))
        threading.Thread(target=work,daemon=True).start()

    def _finish_history_scope_choices(self,dialog,tables,rows,table_combo,choices,selected,displays,buttons,date_from,date_to,status):
        if not dialog.winfo_exists():return
        self.database_tables=tables;self.history_scope_rows=rows
        table_values=[f"{schema}.{table}" for schema,table in tables]
        if self.history_table_var.get() not in table_values:table_values.insert(0,self.history_table_var.get())
        table_combo.configure(values=table_values)
        field_names={"model":("ModelNo","Device","DeviceType"),"variant":("ModelVariant",),"timebase":("TimeBase",)}
        for key,candidates in field_names.items():
            values=sorted({str(value).strip() for row in rows if (value:=self._first_row_value(row,candidates)) not in (None,"")},key=str.lower)
            choices[key][:]=values;selected[key].intersection_update(values)
            current_devices={item.device for item in self.inventory if item.eligible and self._sequence_key(item) in self.selected_sequence_ids}
            if key=="model" and not selected[key]:selected[key].update(value for value in values if value in current_devices)
            self._update_scope_display(displays[key],selected[key]);buttons[key].configure(state="normal")
        dates=sorted({str(value)[:10] for row in rows if (value:=self._first_row_value(row,("TestDate",))) not in (None,"")})
        date_values=["All",*dates]
        date_from.configure(values=date_values);date_to.configure(values=date_values)
        if self.history_date_from_var.get() not in date_values:self.history_date_from_var.set("All")
        if self.history_date_to_var.get() not in date_values:self.history_date_to_var.set("All")
        status.set(f"{len(rows)} row(s) inspected. Choose one or more values, then Apply.")

    def _select_scope_values(self,parent,title,choices,selected,display_var):
        picker=tk.Toplevel(parent);picker.title(f"Choose {title}");picker.transient(parent);picker.grab_set();picker.geometry("460x480");picker.configure(bg=self.colors["bg"]);picker.rowconfigure(1,weight=1);picker.columnconfigure(0,weight=1)
        tk.Label(picker,text=f"Choose {title}",font=self._font(14,"bold"),bg=self.colors["bg"],fg=self.colors["text"]).grid(row=0,column=0,sticky="w",padx=18,pady=(16,8))
        listing=tk.Listbox(picker,selectmode="extended",exportselection=False,font=self._font(10),relief="solid",bd=1);listing.grid(row=1,column=0,sticky="nsew",padx=18)
        for index,value in enumerate(choices):listing.insert("end",value);listing.selection_set(index) if value in selected else None
        def apply():selected.clear();selected.update(choices[index] for index in listing.curselection());self._update_scope_display(display_var,selected);picker.destroy()
        controls=tk.Frame(picker,bg=self.colors["bg"]);controls.grid(row=2,column=0,sticky="ew",padx=18,pady=16)
        self._button(controls,"All",lambda:listing.selection_set(0,"end"),neutral=True,width=75).pack(side="left");self._button(controls,"Clear",lambda:listing.selection_clear(0,"end"),neutral=True,width=75).pack(side="left",padx=6);self._button(controls,"Apply",apply,width=95).pack(side="right")

    @staticmethod
    def _first_row_value(row,candidates):
        for candidate in candidates:
            for key,value in row.items():
                if key.lower()==candidate.lower():return value
        return None

    @staticmethod
    def _update_scope_display(variable,selected):
        values=sorted(selected)
        variable.set("All" if not values else ", ".join(values[:3])+(f" +{len(values)-3}" if len(values)>3 else ""))

    def _load_filtered_history(self):
        self._save_database_defaults();self._log("Reading and filtering historical database rows...")
        def work():
            try:
                config=self._db_config()
                table=self.history_table_var.get().strip();schema=config.schema
                if "." in table:schema,table=table.split(".",1)
                rows=fetch_table_rows(config,table=table,schema=schema,limit=self._limit())
                filters={"model":self.history_model_var.get(),"variant":self.history_variant_var.get(),"timebase":self.history_timebase_var.get(),"date_from":self.history_date_from_var.get(),"date_to":self.history_date_to_var.get()}
                filtered=filter_database_rows(rows,filters)
                scope="; ".join(f"{key}={value}" for key,value in filters.items() if value.strip()) or "all fetched rows"
                self._call_ui(lambda:self._finish_history(filtered,scope))
            except Exception as exc:self._call_ui(lambda exc=exc:self._fail(str(exc)))
        threading.Thread(target=work,daemon=True).start()

    def _finish_history(self,rows,scope):
        self.history_rows=rows;self.history_scope_confirmed=True
        if self.metrics:self.metrics=attach_history(self.metrics,rows)
        self._log(f"Loaded {len(rows)} historical database row(s); baseline scope: {scope}.");self.show_task()

    def _fill_foq_tree(self):
        if not hasattr(self,"foq_tree"):return
        for index,row in enumerate(self.metrics):
            mean="" if row.history.mean is None else f"{row.history.mean:.6g}";delta="" if row.history_delta is None else f"{row.history_delta:+.6g}"
            tag="fail" if row.spec_status=="fail" or row.history_status=="outside-3sigma" else "pass" if row.spec_status=="pass" else "warn"
            context=f"{Path(row.package).stem[:18]} / {row.sequence[:24]}"
            self.foq_tree.insert("","end",iid=str(index),values=(context,row.device,row.db_field,self._display(row.value),row.unit,row.spec_status,row.history_status,mean,delta,f"{row.report_sheet}!{row.report_cell} / {row.spec_evidence}"),tags=(tag,))

    def _foq_summary(self):
        result_rows=[row for row in self.metrics if row.db_field.upper().startswith("RES_")]
        failures=sum(row.spec_status=="fail" for row in result_rows);missing=sum(row.calculation_status!="ok" for row in self.metrics);outliers=sum(row.history_status in {"outside-2sigma","outside-3sigma"} for row in self.metrics)
        if not self.metrics:
            selected=len(self.selected_sequence_ids)
            return f"Results and comparison  |  {selected} sequence(s)  |  {len(self.selected_metric_fields)} metric(s)  |  Click Run check"
        return f"Results and comparison  |  {len(self.metrics)} values  |  {failures}/{len(result_rows)} tests failed  |  {missing} missing  |  {outliers} history alert"

    def _draw_foq_chart(self):
        if not hasattr(self,"chart") or self.task!="foq":return
        self.chart.delete("all");field=self.metric_var.get();rows=[row for row in self.metrics if row.db_field==field and coerce_number(row.value) is not None]
        if not rows:self.chart.create_text(20,20,anchor="nw",text="Choose a numeric metric after running the check.",fill=self.colors["muted"],font=self._font(10));return
        values=[coerce_number(row.value) for row in rows];history=next((row.history for row in rows if row.history.mean is not None),None)
        history_values=[number for item in self.history_rows if (number:=coerce_number(next((value for key,value in item.items() if key.lower()==field.lower()),None))) is not None]
        refs=[history.mean,history.ucl,history.lcl] if history else [];nums=[float(v) for v in values+history_values+refs if v is not None]
        self._draw_metric_scatter(rows,nums,history,history_values)

    def _draw_metric_scatter(self,rows,nums,history,history_values):
        w=max(self.chart.winfo_width(),420);h=max(self.chart.winfo_height(),320);left,top,right,bottom=65,30,w-20,h-72
        lo=min(nums);hi=max(nums);pad=(hi-lo)*.12 or 1;lo-=pad;hi+=pad
        def y(v):return bottom-(float(v)-lo)/(hi-lo)*(bottom-top)
        self.chart.create_line(left,top,left,bottom,right,bottom,fill="#A9ADB5")
        points=history_values[-min(len(history_values),400):]
        current_width=max(130,min(240,(right-left)*.28));history_right=right-current_width if points else left
        for index,value in enumerate(points):
            x=left+(history_right-left)*(index+.5)/max(len(points),1)
            self.chart.create_oval(x-2,y(value)-2,x+2,y(value)+2,fill="#B8BDC5",outline="")
        if points:
            self.chart.create_line(history_right+8,top,history_right+8,bottom,fill=self.colors["border"],dash=(3,3))
            self.chart.create_text(left,bottom+16,anchor="w",text="Filtered history",font=self._font(8,"bold"),fill=self.colors["muted"])
        current_left=history_right+18 if points else left
        current_span=max(1,right-current_left);count=len(rows)
        for i,row in enumerate(rows):
            value=coerce_number(row.value);x=current_left+current_span*(i+.5)/max(count,1);color=self.colors["danger"] if row.spec_status=="fail" else self.colors["primary"]
            self.chart.create_oval(x-7,y(value)-7,x+7,y(value)+7,fill=color,outline="#FFFFFF",width=2)
            self.chart.create_oval(x-9,y(value)-9,x+9,y(value)+9,outline=color,width=2)
            self.chart.create_text(x,y(value)-15,text=f"{value:.5g}",font=self._font(8,"bold"),fill=color)
            self.chart.create_text(x,bottom+18,text=row.sequence[:16],angle=25,anchor="n",font=self._font(7),fill=self.colors["muted"])
        if history and history.mean is not None:
            for value,color,label in ((history.mean,"#5E6470","Mean"),(history.ucl,self.colors["warning"],"UCL"),(history.lcl,self.colors["warning"],"LCL")):
                self.chart.create_line(left,y(value),right,y(value),fill=color,dash=(5,3),width=2);self.chart.create_text(right-4,y(value)-7,anchor="e",text=f"{label} {value:.5g}",fill=color,font=self._font(8,"bold"))
        suffix=f" | {len(points)} historical / {len(rows)} current" if points else f" | {len(rows)} current"
        self.chart.create_text(left,10,anchor="w",text=self.metric_var.get()+suffix,font=self._font(11,"bold"),fill=self.colors["text"])

    def _export_foq(self):
        if not self.metrics:return
        DEFAULT_EXPORT.mkdir(parents=True,exist_ok=True);path=filedialog.asksaveasfilename(parent=self.root,initialdir=DEFAULT_EXPORT,initialfile="FOQ_quick_check.csv",defaultextension=".csv",filetypes=[("CSV","*.csv")])
        if not path:return
        with Path(path).open("w",newline="",encoding="utf-8-sig") as handle:
            writer=csv.writer(handle);writer.writerow(["CMBX","Sequence","Device","DB Field","Description","Value","Unit","Calculation","SPEC","SPEC Evidence","History N","History Mean","History SD","Delta","Z","History Status","Report Sheet","Cell","Injection","Detail"])
            for row in self.metrics:writer.writerow([row.package,row.sequence,row.device,row.db_field,row.description,row.value,row.unit,row.calculation_status,row.spec_status,row.spec_evidence,row.history.count,row.history.mean,row.history.stdev,row.history_delta,row.history_z,row.history_status,row.report_sheet,row.report_cell,row.injection,row.detail])
        self._log(f"Exported {len(self.metrics)} result row(s) to {path}")

    def _connect_database(self):
        if not self._database_dialog():return
        self._log("Connecting and reading table catalog...")
        def work():
            try:
                config=self._db_config();message=test_database_connection(config);tables=list_database_tables(config)
                self._call_ui(lambda:self._finish_connect(message,tables))
            except Exception as exc:self._call_ui(lambda exc=exc:self._fail(str(exc)))
        threading.Thread(target=work,daemon=True).start()

    def _finish_connect(self,message,tables):
        self.database_tables=tables;self._log(f"{message}. {len(tables)} table(s) available.");self.show_task()

    def _load_quality_table(self):
        config=self._db_config();table=self.table_var.get().strip();schema="dbo"
        if "." in table:schema,table=table.split(".",1)
        self._log(f"Reading {schema}.{table}...")
        def work():
            try:
                rows=fetch_table_rows(config,table=table,schema=schema,limit=self._limit());self._call_ui(lambda:self._finish_quality(rows))
            except Exception as exc:self._call_ui(lambda exc=exc:self._fail(str(exc)))
        threading.Thread(target=work,daemon=True).start()

    def _finish_quality(self,rows):self.db_rows=rows;self._log(f"Loaded {len(rows)} historical row(s).");self.show_task()

    def _numeric_db_fields(self):
        if not self.db_rows:return []
        return [field for field in self.db_rows[0] if sum(coerce_number(row.get(field)) is not None for row in self.db_rows)>=max(2,len(self.db_rows)//3)]

    def _refresh_quality_metric_options(self):
        if not hasattr(self,"quality_metric_combo"):return
        query=self.metric_filter_var.get().strip().lower()
        fields=[field for field in self._numeric_db_fields() if query in field.lower()]
        self.quality_metric_combo.configure(values=fields)
        if fields and self.metric_var.get() not in fields:self.metric_var.set(fields[0]);self._refresh_quality_view()

    def _refresh_quality_view(self):
        if not hasattr(self,"history_tree"):return
        field=self.metric_var.get();available=list(self.db_rows[0]) if self.db_rows else []
        identities=("ID","TestDate","Serial","ModelNo","ModelVariant","TimeBase")
        columns=[]
        for wanted in identities:
            actual=next((name for name in available if name.lower()==wanted.lower()),None)
            if actual and actual not in columns:columns.append(actual)
        actual_metric=next((name for name in available if name.lower()==field.lower()),None)
        if actual_metric and actual_metric not in columns:columns.append(actual_metric)
        self.history_tree.configure(columns=columns);self.history_tree.delete(*self.history_tree.get_children())
        for col in columns:
            self.history_tree.heading(col,text=col);self.history_tree.column(col,width=145 if col==actual_metric else 105,minwidth=70,anchor="e" if col==actual_metric else "w")
        for row in self.db_rows[:1000]:self.history_tree.insert("","end",values=[self._display(row.get(col)) for col in columns])
        values=[number for row in self.db_rows if (number:=coerce_number(row.get(field))) is not None];summary=summarize_history(values)
        text=(f"{field or 'No metric selected'}\nN = {summary.count}\nMean = {self._display(summary.mean)}\nSD = {self._display(summary.stdev)}\nUCL = {self._display(summary.ucl)}\nLCL = {self._display(summary.lcl)}")
        self.quality_summary.configure(text=text);self._draw_quality_chart()

    def _draw_quality_chart(self):
        if not hasattr(self,"chart") or self.task!="quality":return
        self.chart.delete("all");field=self.metric_var.get();values=[number for row in self.db_rows if (number:=coerce_number(row.get(field))) is not None]
        if not values:self.chart.create_text(20,20,anchor="nw",text="Load history and choose a numeric metric.",font=self._font(10),fill=self.colors["muted"]);return
        summary=summarize_history(values);w=max(self.chart.winfo_width(),500);h=max(self.chart.winfo_height(),350);left,top,right,bottom=65,30,w-25,h-50
        lo=min(values+[summary.lcl]);hi=max(values+[summary.ucl]);pad=(hi-lo)*.1 or 1;lo-=pad;hi+=pad
        def y(v):return bottom-(v-lo)/(hi-lo)*(bottom-top)
        self.chart.create_line(left,top,left,bottom,right,bottom,fill="#A9ADB5")
        for value,color,label in ((summary.mean,"#5E6470","Mean"),(summary.ucl,self.colors["danger"],"UCL"),(summary.lcl,self.colors["danger"],"LCL")):
            self.chart.create_line(left,y(value),right,y(value),fill=color,dash=(5,3),width=2);self.chart.create_text(right-3,y(value)-7,anchor="e",text=f"{label} {value:.5g}",fill=color,font=self._font(8,"bold"))
        usable=right-left;points=values[-min(len(values),400):];coords=[]
        for i,value in enumerate(points):
            x=left+(usable*i/max(len(points)-1,1));coords.extend((x,y(value)))
        if len(coords)>=4:self.chart.create_line(*coords,fill=self.colors["primary"],width=2)
        for i,value in enumerate(points):
            x=left+(usable*i/max(len(points)-1,1));color=self.colors["danger"] if value>summary.ucl or value<summary.lcl else self.colors["primary"];self.chart.create_oval(x-2,y(value)-2,x+2,y(value)+2,fill=color,outline="")
        self.chart.create_text(left,10,anchor="w",text=f"{field} | last {len(points)} records",font=self._font(11,"bold"),fill=self.colors["text"])

    def _database_defaults(self):
        data={"server":"10.68.178.52","database":"QCLab","username":"QCUser","password":"","schema":"dbo","table":"AUTO","driver":"ODBC Driver 17 for SQL Server","dsn":"","trust_server_certificate":True}
        try:
            saved=json.loads(DEFAULT_CONFIG.read_text(encoding="utf-8"));protected=saved.pop("password_dpapi","");data.update(saved);data["password"]=unprotect_secret(protected) or str(saved.get("password", ""))
        except Exception:pass
        return {key:tk.StringVar(value=str(value)) for key,value in data.items() if key!="trust_server_certificate"}

    def _database_dialog(self):
        dialog=tk.Toplevel(self.root);dialog.title("Database connection");dialog.transient(self.root);dialog.grab_set();dialog.configure(bg=self.colors["bg"]);dialog.resizable(False,False)
        fields=(("DSN (optional)","dsn"),("Server","server"),("Database","database"),("Username","username"),("Password","password"),("Schema","schema"),("Table / AUTO","table"),("ODBC driver","driver"))
        for row,(label,key) in enumerate(fields):
            tk.Label(dialog,text=label,font=self._font(9,"bold"),bg=self.colors["bg"],fg=self.colors["text"]).grid(row=row,column=0,sticky="w",padx=18,pady=6)
            tk.Entry(dialog,textvariable=self.db_vars[key],show="*" if key=="password" else "",width=46,font=self._font(9)).grid(row=row,column=1,padx=18,pady=6,ipady=5)
            if key=="dsn":self._button(dialog,"Browse .dsn",lambda:self._browse_dsn_file(dialog),neutral=True,width=105).grid(row=row,column=2,padx=(0,18),pady=4)
        result={"ok":False}
        def accept():self._save_database_defaults();result["ok"]=True;dialog.destroy()
        buttons=tk.Frame(dialog,bg=self.colors["bg"]);buttons.grid(row=len(fields),column=0,columnspan=2,sticky="e",padx=18,pady=16)
        self._button(buttons,"Cancel",dialog.destroy,neutral=True,width=90).pack(side="left",padx=5);self._button(buttons,"Use",accept,width=90).pack(side="left",padx=5)
        dialog.wait_window();return result["ok"]

    def _save_database_defaults(self):
        data={key:variable.get() for key,variable in self.db_vars.items() if key!="password"}
        data["password_dpapi"]=protect_secret(self.db_vars["password"].get())
        DEFAULT_CONFIG.parent.mkdir(parents=True,exist_ok=True)
        DEFAULT_CONFIG.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")

    def _browse_dsn_file(self,parent):
        path=filedialog.askopenfilename(parent=parent,title="Choose local ODBC DSN",filetypes=[("ODBC data source","*.dsn"),("All files","*.*")])
        if path:self.db_vars["dsn"].set(path)

    def _db_config(self):
        return DatabaseUploadConfig(server=self.db_vars["server"].get().strip(),database=self.db_vars["database"].get().strip(),username=self.db_vars["username"].get().strip(),password=self.db_vars["password"].get(),schema=self.db_vars["schema"].get().strip() or "dbo",table=self.db_vars["table"].get().strip() or "AUTO",driver=self.db_vars["driver"].get().strip() or "ODBC Driver 17 for SQL Server",dsn=self.db_vars["dsn"].get().strip())

    def _table_name(self,config,device):
        if config.table.upper()!="AUTO":return config.table
        from db_upload_service import FOQ_TABLE_BY_DEVICE_TYPE
        return FOQ_TABLE_BY_DEVICE_TYPE.get(device.upper(),"VTCC")

    def _limit(self):
        try:return max(1,min(int(self.history_limit_var.get()),100000))
        except ValueError:return 5000

    def _log(self,message):
        stamp=time.strftime("%H:%M:%S");self.log.insert("end",f"[{stamp}] {message}\n");self.log.see("end")

    def _call_ui(self,callback):self.ui_queue.put(callback)

    def _foq_progress(self,message):
        text=str(message)
        if text.startswith("__PROGRESS__=") and "|" in text:
            percent,detail=text.split("|",1)
            text=f"  {percent.removeprefix('__PROGRESS__=')}% {detail}"
        self._thread_log(text)

    def _drain_ui_queue(self):
        try:
            while True:self.ui_queue.get_nowait()()
        except queue.Empty:pass
        try:self.root.after(50,self._drain_ui_queue)
        except tk.TclError:pass

    def _thread_log(self,message):self._call_ui(lambda:self._log(message))
    def _fail(self,message):self._log(f"Error: {message}");messagebox.showerror(self.TASKS[self.task][0],message,parent=self.root)
    @staticmethod
    def _display(value):
        if value is None:return ""
        if isinstance(value,float):return f"{value:.8g}"
        return str(value)


def main() -> None:
    parser=argparse.ArgumentParser();parser.add_argument("--task",choices=tuple(FoqQualityWindow.TASKS),default="foq");args=parser.parse_args()
    enable_dpi_awareness();root=tk.Tk();FoqQualityWindow(root,args.task);root.mainloop()


if __name__ == "__main__":main()
