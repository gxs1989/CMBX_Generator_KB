from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
import subprocess
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from business_ui_components import BlueCheckbutton, RoundedButton, RoundedPanel, enable_dpi_awareness
from generation_project import (
    DEFAULT_PROJECT_ROOT,
    DEFAULT_WORKSPACE,
    AssetGenerationRequest,
    AssetPreflight,
    generate_asset,
    preflight_asset,
    recommended_online_kb_files_for_modules,
)
from method_md_linter import lint_error_rows
from web_ai_package import (
    AI_CONFIG_FILE,
    AIProviderSettings,
    PromptOptimization,
    base_prompt,
    create_web_ai_zip,
    generate_method_markdown,
    generate_report_markdown,
    load_ai_config,
    optimize_prompt,
)


class MethodReportCreationWindow:
    STEP_TITLES = ("Choose asset", "Choose mode", "Prepare & generate", "Import & preview", "Generate CMBX")
    MODULES = ("TCC", "RID", "VAS", "VVWD", "Pump")

    def __init__(self, root: tk.Tk, initial_asset: str | None = None):
        self.root = root
        self.colors = {
            "window": "#FFFFFF", "sidebar": "#F7F7F8", "panel": "#F5F5F6", "drop": "#ECEDEF",
            "border": "#E3E4E7", "text": "#222326", "muted": "#7C8087", "primary": "#3598F5",
            "primary_hover": "#2389EB", "primary_soft": "#EAF4FE", "error": "#C4322B",
            "error_soft": "#FEE2E2", "warning": "#A85D00", "stage": "#F4B183",
            "branch": "#C6EFCE", "comment": "#15803D", "row": "#FFFFFF", "success": "#198754",
        }
        self.current_step = 0
        selected_asset = initial_asset if initial_asset in {"method", "report"} else "method"
        self.asset_type = tk.StringVar(value=selected_asset)
        self.asset_name = tk.StringVar(value="New test method")
        self.source_md = tk.StringVar()
        self.method_basis_md = tk.StringVar()
        self.output_root = tk.StringVar(value=str(DEFAULT_PROJECT_ROOT))
        self.cm_version = tk.StringVar(value="7.2 compatible")
        self.small_context = tk.BooleanVar(value=True)
        self.keep_md = tk.BooleanVar(value=True)
        self.md_save_root = tk.StringVar(value=str(DEFAULT_PROJECT_ROOT / "AI_generated"))
        self.api_progress_var = tk.DoubleVar(value=0.0)
        self.api_progress_text = tk.StringVar(value="")
        self.module_vars = {name: tk.BooleanVar(value=name == "TCC") for name in self.MODULES}
        self.generation_mode = ""
        self.api_started = 0.0
        self.intent = ""
        self.prompt_prepared = False
        self.kb_files: list[Path] = []
        self.preflight: AssetPreflight | None = None
        self.generated_path: Path | None = None
        self.busy = False
        self._setup_window()
        self._setup_styles()
        self._build_shell()
        if selected_asset == "report":
            self.asset_name.set("New test report")
        self.show_step(1 if initial_asset in {"method", "report"} else 0)

    def _font(self, size: int, weight: str = "normal") -> tuple[str, int, str]:
        return ("Segoe UI", size, weight)

    def _setup_window(self) -> None:
        self.root.title("Method & Report Creation")
        self.root.geometry("1420x900")
        self.root.minsize(1080, 720)
        self.root.configure(bg=self.colors["window"])
        try:
            self.root.state("zoomed")
        except tk.TclError:
            pass

    def _setup_styles(self) -> None:
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(
            "Wizard.Treeview", font=self._font(10), rowheight=30,
            background="#FFFFFF", fieldbackground="#FFFFFF", borderwidth=0,
        )
        style.configure(
            "Wizard.Treeview.Heading", font=self._font(10, "bold"),
            background="#F0F1F3", foreground=self.colors["text"], borderwidth=0,
        )
        style.map("Wizard.Treeview", background=[("selected", "#DCEEFF")], foreground=[("selected", self.colors["text"])])
        style.configure("Wizard.TCheckbutton", font=self._font(10), background=self.colors["panel"], foreground=self.colors["text"])

    def _build_shell(self) -> None:
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        sidebar = tk.Frame(self.root, bg=self.colors["sidebar"], width=265, highlightthickness=1, highlightbackground=self.colors["border"])
        sidebar.grid(row=0, column=0, sticky="nsw")
        sidebar.grid_propagate(False)
        tk.Label(sidebar, text="CMBX Workspace", font=self._font(15, "bold"), bg=self.colors["sidebar"], fg=self.colors["text"]).pack(anchor="w", padx=30, pady=(30, 3))
        tk.Label(sidebar, text="Method, data and quality", font=self._font(10), bg=self.colors["sidebar"], fg=self.colors["muted"]).pack(anchor="w", padx=30, pady=(0, 28))
        self._sidebar_item(sidebar, "Home", False)
        self._sidebar_item(sidebar, "Design & Generate", True)
        self._sidebar_item(sidebar, "Chromatograms & Results", False)
        self._sidebar_item(sidebar, "Quality Control & Database", False)
        tk.Label(
            sidebar, text="Create one reviewed Method or\nReport asset at a time.", justify="left",
            font=self._font(9), bg=self.colors["sidebar"], fg=self.colors["muted"],
        ).pack(side="bottom", anchor="w", padx=30, pady=30)

        main = tk.Frame(self.root, bg=self.colors["window"])
        main.grid(row=0, column=1, sticky="nsew")
        main.columnconfigure(0, weight=1)
        main.rowconfigure(2, weight=1)
        top = tk.Frame(main, bg=self.colors["window"], height=68, highlightthickness=1, highlightbackground=self.colors["border"])
        top.grid(row=0, column=0, sticky="ew")
        top.grid_propagate(False)
        self.breadcrumb_label = tk.Label(
            top, text=f"Workspace / Design & Generate / {'Instrument Method Generation' if self.asset_type.get() == 'method' else 'Report Template Generation'}",
            font=self._font(11), bg=self.colors["window"], fg=self.colors["muted"],
        )
        self.breadcrumb_label.pack(anchor="w", padx=30, pady=22)

        heading = tk.Frame(main, bg=self.colors["window"])
        heading.grid(row=1, column=0, sticky="ew", padx=36, pady=(22, 10))
        heading.columnconfigure(0, weight=1)
        self.title_label = tk.Label(heading, text="Create a Chromeleon asset", font=self._font(22, "bold"), bg=self.colors["window"], fg=self.colors["text"])
        self.title_label.grid(row=0, column=0, sticky="w")
        self.subtitle_label = tk.Label(heading, text="Follow one step at a time.", font=self._font(11), bg=self.colors["window"], fg=self.colors["muted"])
        self.subtitle_label.grid(row=1, column=0, sticky="w", pady=(5, 0))
        self.stepper = tk.Frame(heading, bg=self.colors["window"])
        self.stepper.grid(row=2, column=0, sticky="w", pady=(17, 0))
        self.step_hint_label = tk.Label(
            heading, text="", font=self._font(9, "bold"), bg=self.colors["primary_soft"],
            fg=self.colors["primary"], anchor="w", justify="left", padx=12, pady=8,
        )
        self.step_hint_label.grid(row=3, column=0, sticky="ew", pady=(10, 0))

        self.page_host = tk.Frame(main, bg=self.colors["window"])
        self.page_host.grid(row=2, column=0, sticky="nsew", padx=36, pady=(0, 10))
        self.page_host.columnconfigure(0, weight=1)
        self.page_host.rowconfigure(0, weight=1)

        log_shell = tk.Frame(main, bg=self.colors["window"], height=104, highlightthickness=1, highlightbackground=self.colors["border"])
        log_shell.grid(row=3, column=0, sticky="ew")
        log_shell.grid_propagate(False)
        log_shell.columnconfigure(0, weight=1)
        tk.Label(log_shell, text="Progress log", font=self._font(9, "bold"), bg=self.colors["window"], fg=self.colors["text"]).grid(row=0, column=0, sticky="w", padx=30, pady=(8, 2))
        self.log_text = tk.Text(log_shell, height=3, font=("Consolas", 9), bg="#FAFAFB", fg="#52565D", relief="flat", wrap="word", state="disabled")
        self.log_text.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 8))

        footer = tk.Frame(main, bg=self.colors["window"], height=72, highlightthickness=1, highlightbackground=self.colors["border"])
        footer.grid(row=4, column=0, sticky="ew")
        footer.grid_propagate(False)
        footer.columnconfigure(1, weight=1)
        self.back_button = self._button(footer, "Back", self.go_back, neutral=True, width=112)
        self.back_button.grid(row=0, column=0, padx=(30, 0), pady=14)
        self.status_label = tk.Label(footer, text="", font=self._font(9), bg=self.colors["window"], fg=self.colors["muted"], wraplength=620, justify="center")
        self.status_label.grid(row=0, column=1, padx=18, sticky="ew")
        self.next_button = self._button(footer, "Continue", self.go_next, width=152)
        self.next_button.grid(row=0, column=2, padx=(0, 30), pady=14)
        self._log("Workflow opened. Choose Instrument Method or Report Template.")

    def _sidebar_item(self, parent: tk.Misc, text: str, selected: bool) -> None:
        bg = self.colors["primary"] if selected else self.colors["sidebar"]
        fg = "#FFFFFF" if selected else self.colors["muted"]
        label = tk.Label(parent, text=text, anchor="w", font=self._font(11, "bold" if selected else "normal"), bg=bg, fg=fg, padx=14, pady=12)
        label.pack(fill="x", padx=18, pady=3)

    def _button(self, parent: tk.Misc, text: str, command, *, neutral: bool = False, width: int = 150) -> RoundedButton:
        bg = self.colors["window"] if neutral else self.colors["primary"]
        fg = self.colors["text"] if neutral else "#FFFFFF"
        hover = self.colors["panel"] if neutral else self.colors["primary_hover"]
        return RoundedButton(
            parent, text, command, width=width, height=44, radius=9,
            bg=bg, hover_bg=hover, fg=fg,
            border=self.colors["border"] if neutral else self.colors["primary"],
            font=self._font(10, "bold"),
        )

    def _log(self, message: str) -> None:
        if not hasattr(self, "log_text"):
            return
        stamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"[{stamp}] {message}\n")
        lines = int(self.log_text.index("end-1c").split(".")[0])
        if lines > 120:
            self.log_text.delete("1.0", f"{lines - 100}.0")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def selected_modules(self) -> tuple[str, ...]:
        return tuple(name for name, variable in self.module_vars.items() if variable.get())

    def show_step(self, step: int) -> None:
        self.current_step = max(0, min(4, step))
        for child in self.page_host.winfo_children():
            child.destroy()
        for child in self.stepper.winfo_children():
            child.destroy()
        self._render_stepper()
        titles = (
            ("What do you want to create?", "Choose one asset. The next step opens immediately."),
            ("How do you want to generate the MD?", "Built-in API generation runs directly here; manual web mode packages evidence for an external model."),
            ("Prepare and generate the MD", "Choose modules, describe the requirement and run the selected generation mode."),
            ("Import and review the generated MD", "The MD is checked and rendered before CMBX generation."),
            ("Generate the CMBX", "Confirm the name and destination, then create the standalone Chromeleon package."),
        )
        self.title_label.configure(text=titles[self.current_step][0])
        self.subtitle_label.configure(text=titles[self.current_step][1])
        self.step_hint_label.configure(text=f"Step {self.current_step}: {self.STEP_TITLES[self.current_step]}  |  {titles[self.current_step][1]}")
        (self._page_choose, self._page_mode, self._page_define, self._page_import, self._page_generate)[self.current_step]()
        self.back_button.configure(state="disabled" if self.current_step == 0 or self.busy else "normal")
        if self.current_step == 2 and self.generation_mode == "api" and not self.source_md.get().strip():
            self.next_button.configure(text="Generate via API", state="disabled" if self.busy else "normal")
            self.step_hint_label.configure(
                text=f"Step 2: {self.STEP_TITLES[2]}  |  Describe the requirement, then click \"Generate via API\" below and wait for the progress to finish.",
            )
        else:
            self.next_button.configure(text="Generate CMBX" if self.current_step == 4 else "Continue", state="disabled" if self.busy else "normal")
        if self.current_step in (0, 1):
            self.next_button.grid_remove()
        else:
            self.next_button.grid()

    def _render_stepper(self) -> None:
        for index, title in enumerate(self.STEP_TITLES):
            active = index == self.current_step
            done = index < self.current_step
            color = self.colors["success"] if done else self.colors["primary"] if active else self.colors["panel"]
            number_color = "#FFFFFF" if active or done else self.colors["muted"]
            text_color = self.colors["primary"] if active else self.colors["success"] if done else self.colors["muted"]
            tk.Label(
                self.stepper, text=str(index), width=3, font=self._font(10, "bold"),
                bg=color, fg=number_color, padx=2, pady=5,
            ).pack(side="left")
            tk.Label(self.stepper, text=title, font=self._font(10, "bold" if active else "normal"), bg=self.colors["window"], fg=text_color).pack(side="left", padx=(7, 12))
            if index < 4:
                tk.Frame(self.stepper, bg=self.colors["border"], width=28, height=1).pack(side="left", padx=(0, 12))

    def _page_frame(self) -> tk.Frame:
        frame = tk.Frame(
            self.page_host, bg=self.colors["window"], highlightthickness=2,
            highlightbackground=self.colors["primary"], highlightcolor=self.colors["primary"],
        )
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        return frame

    def _page_choose(self) -> None:
        frame = self._page_frame()
        cards = tk.Frame(frame, bg=self.colors["window"])
        cards.grid(row=0, column=0, sticky="nsew")
        cards.rowconfigure(0, weight=1)
        cards.columnconfigure(0, weight=1, uniform="asset")
        cards.columnconfigure(1, weight=1, uniform="asset")
        self._asset_card(cards, 0, "method", "Instrument Method", "Compile a reviewed CM Method Script MD into a standalone method CMBX.")
        self._asset_card(cards, 1, "report", "Report Template", "Compile a reviewed Report MD into a standalone report-template CMBX.")

    def _asset_card(self, parent: tk.Misc, column: int, value: str, title: str, description: str) -> None:
        selected = self.asset_type.get() == value
        panel = RoundedPanel(
            parent, fill=self.colors["primary_soft"] if selected else self.colors["panel"],
            border=self.colors["primary"] if selected else self.colors["border"], radius=14, padding=14,
            parent_bg=self.colors["window"], height=330,
        )
        panel.grid(row=0, column=column, sticky="nsew", padx=(0 if column == 0 else 10, 10 if column == 0 else 0), pady=(8, 45))
        body = panel.body
        icon = "M" if value == "method" else "R"
        icon_label = tk.Label(body, text=icon, font=self._font(18, "bold"), width=3, height=2, bg=self.colors["primary"], fg="#FFFFFF")
        icon_label.pack(anchor="w", padx=16, pady=(14, 18))
        title_label = tk.Label(body, text=title, font=self._font(17, "bold"), bg=body["bg"], fg=self.colors["text"])
        title_label.pack(anchor="w", padx=16)
        desc_label = tk.Label(body, text=description, font=self._font(11), wraplength=430, justify="left", bg=body["bg"], fg=self.colors["muted"])
        desc_label.pack(anchor="w", padx=16, pady=(10, 18))
        action = self._button(body, "Choose", lambda v=value: self._select_asset(v), width=126)
        action.pack(anchor="w", padx=16, pady=(0, 16))
        for widget in (panel, body, icon_label, title_label, desc_label):
            widget.bind("<Button-1>", lambda _event, v=value: self._select_asset(v))

    def _select_asset(self, value: str) -> None:
        self.asset_type.set(value)
        self.breadcrumb_label.configure(
            text=f"Workspace / Design & Generate / {'Instrument Method Generation' if value == 'method' else 'Report Template Generation'}",
        )
        self.source_md.set("")
        self.preflight = None
        self.generated_path = None
        self.prompt_prepared = False
        self.asset_name.set("New test method" if value == "method" else "New test report")
        self.generation_mode = ""
        self.api_progress_var.set(0.0)
        self.api_progress_text.set("")
        self._log(f"Asset selected: {'Instrument Method' if value == 'method' else 'Report Template'}.")
        self.show_step(1)

    def _page_mode(self) -> None:
        frame = self._page_frame()
        cards = tk.Frame(frame, bg=self.colors["window"])
        cards.grid(row=0, column=0, sticky="nsew")
        cards.rowconfigure(0, weight=1)
        cards.columnconfigure(0, weight=1, uniform="mode")
        cards.columnconfigure(1, weight=1, uniform="mode")
        self._mode_card(
            cards, 0, "api", "API automatic generation",
            "Call GPT or DeepSeek directly with the local SPEC/KB evidence. Shows live progress and can keep a copy of the generated MD.",
        )
        self._mode_card(
            cards, 1, "manual", "Manual Web AI",
            "Package the SPEC/KB evidence into a ZIP, generate the MD in an external web model, then import it here for review and compilation.",
        )

    def _mode_card(self, parent: tk.Misc, column: int, value: str, title: str, description: str) -> None:
        selected = self.generation_mode == value
        panel = RoundedPanel(
            parent, fill=self.colors["primary_soft"] if selected else self.colors["panel"],
            border=self.colors["primary"] if selected else self.colors["border"], radius=14, padding=14,
            parent_bg=self.colors["window"], height=330,
        )
        panel.grid(row=0, column=column, sticky="nsew", padx=(0 if column == 0 else 10, 10 if column == 0 else 0), pady=(8, 45))
        body = panel.body
        icon = "A" if value == "api" else "W"
        icon_label = tk.Label(body, text=icon, font=self._font(18, "bold"), width=3, height=2, bg=self.colors["primary"], fg="#FFFFFF")
        icon_label.pack(anchor="w", padx=16, pady=(14, 18))
        title_label = tk.Label(body, text=title, font=self._font(17, "bold"), bg=body["bg"], fg=self.colors["text"])
        title_label.pack(anchor="w", padx=16)
        desc_label = tk.Label(body, text=description, font=self._font(11), wraplength=430, justify="left", bg=body["bg"], fg=self.colors["muted"])
        desc_label.pack(anchor="w", padx=16, pady=(10, 18))

        def choose() -> None:
            self.generation_mode = value
            self._log(f"Generation mode selected: {'API automatic' if value == 'api' else 'Manual Web AI'}.")
            self.show_step(2)

        action = self._button(body, "Choose", choose, width=126)
        action.pack(anchor="w", padx=16, pady=(0, 16))
        for widget in (panel, body, icon_label, title_label, desc_label):
            widget.bind("<Button-1>", lambda _event, fn=choose: fn())

    def _page_define_api(self) -> None:
        frame = self._page_frame()
        content = tk.Frame(frame, bg=self.colors["window"])
        content.grid(row=0, column=0, sticky="nsew")
        content.columnconfigure(0, weight=2, uniform="api")
        content.columnconfigure(1, weight=3, uniform="api")
        content.rowconfigure(0, weight=1)

        left = RoundedPanel(content, fill=self.colors["panel"], border=self.colors["border"], radius=12, padding=12, parent_bg=self.colors["window"])
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=6)
        form = left.body
        form.columnconfigure(1, weight=1)
        row = 0
        tk.Label(form, text="1. Select modules", font=self._font(14, "bold"), bg=form["bg"], fg=self.colors["text"]).grid(row=row, column=0, columnspan=2, sticky="w", padx=12, pady=(10, 5)); row += 1
        module_row = tk.Frame(form, bg=form["bg"])
        module_row.grid(row=row, column=0, columnspan=2, sticky="w", padx=8, pady=(0, 8)); row += 1
        for index, name in enumerate(self.MODULES):
            BlueCheckbutton(
                module_row, name, self.module_vars[name], self._modules_changed,
                bg=form["bg"], fg=self.colors["text"], active=self.colors["primary"], font=self._font(10),
            ).grid(row=index // 3, column=index % 3, sticky="w", padx=6, pady=4)

        tk.Label(form, text="2. Requirement", font=self._font(14, "bold"), bg=form["bg"], fg=self.colors["text"]).grid(row=row, column=0, columnspan=2, sticky="w", padx=12, pady=(16, 5)); row += 1
        self.intent_text = tk.Text(form, height=5, font=self._font(10), wrap="word", relief="flat", bg=self.colors["window"], fg=self.colors["text"], padx=12, pady=10, highlightthickness=1, highlightbackground=self.colors["border"])
        self.intent_text.grid(row=row, column=0, columnspan=2, sticky="nsew", padx=12, pady=(0, 8))
        form.rowconfigure(row, weight=1)
        row += 1
        self.intent_text.insert("1.0", self.intent)

        tk.Label(form, text="3. AI provider", font=self._font(14, "bold"), bg=form["bg"], fg=self.colors["text"]).grid(row=row, column=0, columnspan=2, sticky="w", padx=12, pady=(16, 5)); row += 1
        self.api_setting_label = tk.Label(
            form,
            text="",
            font=self._font(9), bg=form["bg"], fg=self.colors["muted"],
        )
        self.api_setting_label.grid(row=row, column=0, sticky="w", padx=12, pady=(0, 4)); row += 1
        self._refresh_api_setting_label()
        self._button(form, "AI settings", self._open_ai_settings, neutral=True, width=116).grid(row=row, column=0, columnspan=2, sticky="w", padx=12, pady=(0, 8)); row += 1

        tk.Label(form, text="4. Options", font=self._font(14, "bold"), bg=form["bg"], fg=self.colors["text"]).grid(row=row, column=0, columnspan=2, sticky="w", padx=12, pady=(14, 4)); row += 1
        BlueCheckbutton(
            form, "Small evidence package (<200 KB per file, recommended for speed)", self.small_context,
            self._refresh_kb_files, bg=form["bg"], fg=self.colors["text"], active=self.colors["primary"], font=self._font(9),
        ).grid(row=row, column=0, columnspan=2, sticky="w", padx=12, pady=3); row += 1
        BlueCheckbutton(
            form, "Keep a copy of the generated MD", self.keep_md,
            lambda: None, bg=form["bg"], fg=self.colors["text"], active=self.colors["primary"], font=self._font(9),
        ).grid(row=row, column=0, columnspan=2, sticky="w", padx=12, pady=3); row += 1
        tk.Entry(form, textvariable=self.md_save_root, font=self._font(9), relief="flat", highlightthickness=1, highlightbackground=self.colors["border"], bg=self.colors["window"]).grid(row=row, column=0, sticky="ew", padx=(12, 4), pady=(0, 6), ipady=6)
        self._button(form, "Choose", self._choose_md_save_root, neutral=True, width=92).grid(row=row, column=1, sticky="w", pady=(0, 6)); row += 1

        self.api_generate_button = self._button(form, "Generate via API", self._start_auto_generate, width=190)
        self.api_generate_button.grid(row=row, column=0, columnspan=2, sticky="w", padx=12, pady=(8, 4)); row += 1
        progress_row = tk.Frame(form, bg=form["bg"])
        progress_row.grid(row=row, column=0, columnspan=2, sticky="ew", padx=12, pady=(2, 0)); row += 1
        progress_row.columnconfigure(0, weight=1)
        self.api_progress_bar = ttk.Progressbar(progress_row, variable=self.api_progress_var, maximum=100)
        self.api_progress_bar.grid(row=0, column=0, sticky="ew")
        self.api_elapsed_label = tk.Label(progress_row, text="", font=self._font(9), bg=form["bg"], fg=self.colors["muted"])
        self.api_elapsed_label.grid(row=0, column=1, padx=(10, 0))
        self.api_status_label = tk.Label(form, textvariable=self.api_progress_text, font=self._font(9), bg=form["bg"], fg=self.colors["muted"], anchor="w", justify="left", wraplength=430)
        self.api_status_label.grid(row=row, column=0, columnspan=2, sticky="ew", padx=12, pady=(3, 8))

        right = RoundedPanel(content, fill=self.colors["panel"], border=self.colors["border"], radius=12, padding=12, parent_bg=self.colors["window"])
        right.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=6)
        docs = right.body
        docs.columnconfigure(0, weight=1)
        docs.rowconfigure(2, weight=1)
        tk.Label(docs, text="Evidence sent to the API", font=self._font(13, "bold"), bg=docs["bg"], fg=self.colors["text"]).grid(row=0, column=0, sticky="w", padx=12, pady=(10, 4))
        self.api_context_label = tk.Label(docs, text="", font=self._font(9), bg=docs["bg"], fg=self.colors["muted"], anchor="w", wraplength=690, justify="left")
        self.api_context_label.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 8))
        columns = ("file", "context", "size")
        self.docs_tree = ttk.Treeview(docs, columns=columns, show="headings", style="Wizard.Treeview", selectmode="browse")
        self.docs_tree.heading("file", text="File")
        self.docs_tree.heading("context", text="Module / context")
        self.docs_tree.heading("size", text="Size")
        self.docs_tree.column("file", width=300, stretch=True)
        self.docs_tree.column("context", width=180, stretch=False)
        self.docs_tree.column("size", width=80, stretch=False, anchor="e")
        ybar = ttk.Scrollbar(docs, orient="vertical", command=self.docs_tree.yview)
        self.docs_tree.configure(yscrollcommand=ybar.set)
        self.docs_tree.grid(row=2, column=0, sticky="nsew", padx=(12, 0), pady=(0, 8))
        ybar.grid(row=2, column=1, sticky="ns", padx=(0, 12), pady=(0, 8))
        self.docs_tree.bind("<Double-Button-1>", self._open_selected_kb)
        self._button(docs, "Open selected", self._open_selected_kb, neutral=True, width=138).grid(row=3, column=0, columnspan=2, sticky="w", padx=12, pady=(0, 10))
        self._refresh_kb_files()

    def _refresh_api_setting_label(self) -> None:
        if not hasattr(self, "api_setting_label") or not self.api_setting_label.winfo_exists():
            return
        config = load_ai_config()
        provider = str(config.get("provider") or "gpt").strip().lower()
        model = str(config.get("model") or "").strip()
        key_ready = bool(str(config.get("api_key") or "").strip())
        self.api_setting_label.configure(
            text=f"{provider} · {model} · {'API key configured' if key_ready else 'API key required'}",
            fg=self.colors["success"] if key_ready else self.colors["warning"],
        )

    def _choose_md_save_root(self) -> None:
        value = filedialog.askdirectory(parent=self.root, title="Select MD save folder", initialdir=self.md_save_root.get())
        if value:
            self.md_save_root.set(value)

    def _page_define(self) -> None:
        if self.generation_mode == "api":
            self._page_define_api()
        else:
            self._page_define_manual()

    def _page_define_manual(self) -> None:
        frame = self._page_frame()
        content = tk.Frame(frame, bg=self.colors["window"])
        content.grid(row=0, column=0, sticky="nsew")
        content.columnconfigure(0, weight=2, uniform="define")
        content.columnconfigure(1, weight=3, uniform="define")
        content.rowconfigure(0, weight=1)

        left = RoundedPanel(content, fill=self.colors["panel"], border=self.colors["border"], radius=12, padding=12, parent_bg=self.colors["window"])
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=6)
        form = left.body
        form.columnconfigure(0, weight=1)
        form.rowconfigure(5, weight=1)
        tk.Label(form, text="1. Select modules", font=self._font(14, "bold"), bg=form["bg"], fg=self.colors["text"]).grid(row=0, column=0, sticky="w", padx=12, pady=(10, 5))
        tk.Label(form, text="Select every module relevant to the test. Files are combined and deduplicated.", font=self._font(9), wraplength=430, justify="left", bg=form["bg"], fg=self.colors["muted"]).grid(row=1, column=0, sticky="w", padx=12, pady=(0, 10))
        module_row = tk.Frame(form, bg=form["bg"])
        module_row.grid(row=2, column=0, sticky="w", padx=8)
        for index, name in enumerate(self.MODULES):
            BlueCheckbutton(
                module_row, name, self.module_vars[name], self._modules_changed,
                bg=form["bg"], fg=self.colors["text"], active=self.colors["primary"], font=self._font(10),
            ).grid(row=index // 2, column=index % 2, sticky="w", padx=6, pady=5)

        tk.Label(form, text="2. Optional prompt preparation", font=self._font(14, "bold"), bg=form["bg"], fg=self.colors["text"]).grid(row=3, column=0, sticky="w", padx=12, pady=(20, 5))
        tk.Label(
            form,
            text="Enter a requirement, then optionally optimize it. The complete prompt stays visible and editable; Optimize can be run again after your edits.",
            font=self._font(9), wraplength=430, justify="left", bg=form["bg"], fg=self.colors["muted"],
        ).grid(row=4, column=0, sticky="w", padx=12, pady=(0, 8))
        self.intent_text = tk.Text(form, height=7, font=self._font(10), wrap="word", relief="flat", bg=self.colors["window"], fg=self.colors["text"], padx=12, pady=10, highlightthickness=1, highlightbackground=self.colors["border"])
        self.intent_text.grid(row=5, column=0, sticky="nsew", padx=12, pady=(0, 8))
        self.intent_text.insert("1.0", self.intent)
        prompt_actions = tk.Frame(form, bg=form["bg"])
        prompt_actions.grid(row=6, column=0, sticky="ew", padx=12, pady=(0, 5))
        self._button(prompt_actions, "AI settings", self._open_ai_settings, neutral=True, width=116).pack(side="left")
        self.optimize_prompt_button = self._button(prompt_actions, "Optimize", self._start_prompt_optimization, width=116)
        self.optimize_prompt_button.pack(side="left", padx=8)
        prompt_status = "Optimized prompt is visible and editable; choose Optimize to regenerate it." if self.prompt_prepared else "Prompt is editable and has not been optimized locally."
        self.prompt_status_label = tk.Label(form, text=prompt_status, font=self._font(8), bg=form["bg"], fg=self.colors["success"] if self.prompt_prepared else self.colors["muted"], wraplength=430, justify="left")
        self.prompt_status_label.grid(row=7, column=0, sticky="w", padx=12, pady=(0, 10))

        right = RoundedPanel(content, fill=self.colors["panel"], border=self.colors["border"], radius=12, padding=12, parent_bg=self.colors["window"])
        right.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=6)
        docs = right.body
        docs.columnconfigure(0, weight=1)
        tree_row = 3 if self.asset_type.get() == "report" else 2
        docs.rowconfigure(tree_row, weight=1)
        tk.Label(docs, text="Related SPEC and KB files", font=self._font(14, "bold"), bg=docs["bg"], fg=self.colors["text"]).grid(row=0, column=0, sticky="w", padx=12, pady=(10, 4))
        tk.Label(docs, text="Double-click a file to inspect it. The package contains these files plus 00_PROMPT.md.", font=self._font(9), bg=docs["bg"], fg=self.colors["muted"], wraplength=690, justify="left").grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))
        if self.asset_type.get() == "report":
            basis = tk.Frame(docs, bg=docs["bg"])
            basis.grid(row=2, column=0, columnspan=2, sticky="ew", padx=12, pady=(0, 9))
            basis.columnconfigure(1, weight=1)
            tk.Label(basis, text="Method basis", font=self._font(9, "bold"), bg=docs["bg"], fg=self.colors["text"]).grid(row=0, column=0, sticky="w", padx=(0, 8))
            tk.Entry(basis, textvariable=self.method_basis_md, state="readonly", readonlybackground="#FFFFFF", font=self._font(9), relief="flat", highlightthickness=1, highlightbackground=self.colors["border"]).grid(row=0, column=1, sticky="ew", ipady=6)
            self._button(basis, "Choose MD", self._choose_method_basis, neutral=True, width=108).grid(row=0, column=2, padx=(8, 0))
            self._button(basis, "Recent", self._choose_recent_method_basis, neutral=True, width=92).grid(row=0, column=3, padx=(8, 0))
            tk.Label(basis, text="Recommended: attach the generated Method MD so the report uses the same channels, variables and RetTimes.", font=self._font(8), bg=docs["bg"], fg=self.colors["muted"], wraplength=620, justify="left").grid(row=1, column=0, columnspan=4, sticky="w", pady=(5, 0))
        columns = ("file", "context", "size")
        self.docs_tree = ttk.Treeview(docs, columns=columns, show="headings", style="Wizard.Treeview", selectmode="browse")
        self.docs_tree.heading("file", text="File")
        self.docs_tree.heading("context", text="Module / context")
        self.docs_tree.heading("size", text="Size")
        self.docs_tree.column("file", width=300, stretch=True)
        self.docs_tree.column("context", width=180, stretch=False)
        self.docs_tree.column("size", width=80, stretch=False, anchor="e")
        ybar = ttk.Scrollbar(docs, orient="vertical", command=self.docs_tree.yview)
        self.docs_tree.configure(yscrollcommand=ybar.set)
        self.docs_tree.grid(row=tree_row, column=0, sticky="nsew", padx=(12, 0), pady=(0, 8))
        ybar.grid(row=tree_row, column=1, sticky="ns", padx=(0, 12), pady=(0, 8))
        self.docs_tree.bind("<Double-Button-1>", self._open_selected_kb)
        options = tk.Frame(docs, bg=docs["bg"])
        options.grid(row=tree_row + 1, column=0, columnspan=2, sticky="ew", padx=12, pady=(2, 8))
        BlueCheckbutton(
            options, "Small-file package (<200 KB per MD)", self.small_context, self._refresh_kb_files,
            bg=docs["bg"], fg=self.colors["text"], active=self.colors["primary"], font=self._font(9),
        ).pack(side="left")
        self.package_note = tk.Label(options, text="", font=self._font(8), bg=docs["bg"], fg=self.colors["warning"], wraplength=350, justify="left")
        self.package_note.pack(side="left", padx=12)
        actions = tk.Frame(docs, bg=docs["bg"])
        actions.grid(row=tree_row + 2, column=0, columnspan=2, sticky="ew", padx=12, pady=(0, 10))
        self._button(actions, "Open selected", self._open_selected_kb, neutral=True, width=138).pack(side="left")
        self._button(actions, "Create ZIP", self._start_package, width=126).pack(side="right")
        self._refresh_kb_files()

    def _start_auto_generate(self) -> None:
        modules = self.selected_modules()
        if not modules:
            messagebox.showwarning("Method & Report Creation", "Select at least one module.", parent=self.root)
            return
        self._capture_page()
        requirement = self.intent.strip()
        if not requirement:
            messagebox.showwarning("Method & Report Creation", "Enter the test/report requirement first.", parent=self.root)
            return
        config = load_ai_config()
        provider = str(config.get("provider") or "gpt").strip().lower()
        api_key = str(config.get("api_key") or "").strip()
        if not api_key:
            messagebox.showwarning(
                "Method & Report Creation",
                f"{provider} API key is empty. Configure it in AI settings first.",
                parent=self.root,
            )
            self._open_ai_settings()
            return
        basis_path: Path | None = None
        if self.asset_type.get() == "report":
            basis_value = self.method_basis_md.get().strip()
            if not basis_value:
                messagebox.showwarning(
                    "Method & Report Creation",
                    "Attach a Method MD basis before automatic Report generation.",
                    parent=self.root,
                )
                return
            basis_path = Path(basis_value)
            if not basis_path.is_file():
                messagebox.showerror("Method & Report Creation", f"Method basis MD not found:\n{basis_value}", parent=self.root)
                return
        kb_files = recommended_online_kb_files_for_modules(
            self.asset_type.get(), modules, small_context=bool(self.small_context.get()),
        )
        if not kb_files:
            messagebox.showwarning(
                "Method & Report Creation",
                "No SPEC/KB files were found for the selected modules.",
                parent=self.root,
            )
            return
        context_bytes = sum(path.stat().st_size for path in kb_files if path.is_file())
        context_name = "small" if self.small_context.get() else "full"
        self._log(f"API evidence: {len(kb_files)} file(s), {context_bytes // 1024} KB, {context_name} package")
        settings = AIProviderSettings(
            provider=provider,
            base_url=str(config.get("base_url") or "").strip(),
            model=str(config.get("model") or "").strip(),
            api_key=api_key,
        )
        kind = "Method" if self.asset_type.get() == "method" else "Report"
        self._set_api_progress(3, f"Preparing {kind} evidence...")
        self._set_busy(True, f"Calling {provider} API to generate {kind} Markdown...")
        self._log(f"Automatic {provider} generation started: {', '.join(modules)}")
        self._start_api_timer()
        threading.Thread(
            target=self._auto_generate_worker,
            args=(modules, requirement, kb_files, settings, basis_path),
            daemon=True,
        ).start()

    def _auto_generate_worker(
        self,
        modules: tuple[str, ...],
        requirement: str,
        kb_files: list[Path],
        settings: AIProviderSettings,
        basis_path: Path | None,
    ) -> None:
        try:
            self._post_progress(8, f"Calling {settings.provider} API ({settings.model})...")
            if self.asset_type.get() == "report":
                if not basis_path or not basis_path.is_file():
                    raise ValueError("A valid Method MD basis is required for Report generation.")
                method_markdowns = [(basis_path.name, basis_path.read_text(encoding="utf-8", errors="replace"))]
                generated = generate_report_markdown(requirement, modules, kb_files, method_markdowns, settings)
            else:
                generated = generate_method_markdown(requirement, modules, kb_files, settings)
            self._post_progress(70, "API returned Markdown; saving the MD...")
            out_dir = DEFAULT_PROJECT_ROOT / "AI_generated"
            out_dir.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            kind = "method" if self.asset_type.get() == "method" else "report"
            path = out_dir / f"{kind}_{settings.provider}_{stamp}.md"
            path.write_text(generated, encoding="utf-8")
            kept_paths = [path]
            if self.keep_md.get():
                save_root = Path(self.md_save_root.get().strip() or str(out_dir))
                if save_root.resolve() != out_dir.resolve():
                    save_root.mkdir(parents=True, exist_ok=True)
                    kept = save_root / path.name
                    kept.write_text(generated, encoding="utf-8")
                    kept_paths.append(kept)
            self._post_progress(85, "Running MD structural preflight...")
            checked = preflight_asset(self.asset_type.get(), path)
            self.root.after(0, lambda p=path, k=kept_paths, c=checked: self._finish_auto_generate(p, k, c))
        except Exception as exc:
            self.root.after(0, lambda error=exc: self._task_failed("Automatic generation", error))

    def _post_progress(self, percent: float, text: str) -> None:
        self.root.after(0, lambda: self._set_api_progress(percent, text))

    def _set_api_progress(self, percent: float, text: str) -> None:
        self.api_progress_var.set(percent)
        self.api_progress_text.set(text)
        self.status_label.configure(text=text)

    def _start_api_timer(self) -> None:
        self.api_started = time.monotonic()
        self._tick_api_timer()

    def _tick_api_timer(self) -> None:
        if not self.busy:
            if hasattr(self, "api_elapsed_label") and self.api_elapsed_label.winfo_exists():
                self.api_elapsed_label.configure(text="")
            return
        elapsed = time.monotonic() - self.api_started
        if hasattr(self, "api_elapsed_label") and self.api_elapsed_label.winfo_exists():
            self.api_elapsed_label.configure(text=f"{elapsed:.0f} s")
        self.root.after(1000, self._tick_api_timer)

    def _finish_auto_generate(self, path: Path, kept_paths: list[Path], checked: AssetPreflight) -> None:
        self.source_md.set(str(path))
        self.preflight = checked
        self.generated_path = None
        elapsed = time.monotonic() - self.api_started
        self._log(f"API-generated MD saved: {path} ({elapsed:.0f} s total)")
        for kept in kept_paths[1:]:
            self._log(f"MD copy saved: {kept}")
        self._set_api_progress(100, f"Generated in {elapsed:.0f} s. Review the MD in the next step.")
        self._set_busy(False, f"Generated in {elapsed:.0f} s. Review the MD in the next step.")
        self.show_step(3)

    def _refresh_kb_files(self) -> None:
        if not hasattr(self, "docs_tree") or not self.docs_tree.winfo_exists():
            return
        self.docs_tree.delete(*self.docs_tree.get_children())
        modules = self.selected_modules()
        self.kb_files = recommended_online_kb_files_for_modules(
            self.asset_type.get(), modules, small_context=bool(self.small_context.get()),
        )
        basis_path = Path(self.method_basis_md.get()) if self.method_basis_md.get().strip() else None
        if self.asset_type.get() == "report" and basis_path and basis_path.is_file():
            self.kb_files = [basis_path, *[path for path in self.kb_files if path.resolve() != basis_path.resolve()]]
        context = "Small <200 KB" if self.small_context.get() else "Full"
        total_bytes = 0
        for index, path in enumerate(self.kb_files):
            module = "Method basis" if basis_path and path.resolve() == basis_path.resolve() else next((item for item in modules if item in path.parts), "Common")
            size = f"{path.stat().st_size / 1024:.1f} KB" if path.is_file() else "Missing"
            if path.is_file():
                total_bytes += path.stat().st_size
            self.docs_tree.insert("", "end", iid=str(index), values=(path.name, f"{module} / {context}", size))
        if hasattr(self, "api_context_label") and self.api_context_label.winfo_exists():
            self.api_context_label.configure(
                text=f"{len(self.kb_files)} file(s) · {total_bytes / 1024:.0f} KB · {context} package",
            )
        if hasattr(self, "package_note") and self.package_note.winfo_exists():
            if self.small_context.get():
                self.package_note.configure(text="Extract before upload to a file-limited model.")
            else:
                self.package_note.configure(text="")

    def _modules_changed(self) -> None:
        self.prompt_prepared = False
        if hasattr(self, "prompt_status_label") and self.prompt_status_label.winfo_exists():
            self.prompt_status_label.configure(text="Modules changed. Review or optimize the prompt again.", fg=self.colors["warning"])
        self._refresh_kb_files()

    def _start_prompt_optimization(self) -> None:
        self._capture_page()
        modules = self.selected_modules()
        if not modules:
            messagebox.showwarning("Prompt optimization", "Select at least one module.", parent=self.root)
            return
        if not self.intent.strip():
            messagebox.showwarning("Prompt optimization", "Enter the test or report requirement first.", parent=self.root)
            return
        prepared = self.prompt_prepared
        self._set_busy(True, "Optimizing the visible prompt...")
        self._log("Prompt optimization started. The result will replace the editable prompt text.")
        threading.Thread(
            target=self._prompt_optimization_worker,
            args=(modules, self.intent, prepared), daemon=True,
        ).start()

    def _prompt_optimization_worker(self, modules: tuple[str, ...], text: str, prepared: bool) -> None:
        try:
            result = optimize_prompt(
                self.asset_type.get(), modules, text, prepared_prompt=prepared,
                has_method_basis=bool(self.method_basis_md.get().strip()),
            )
            self.root.after(0, lambda: self._finish_prompt_optimization(result))
        except Exception as exc:
            self.root.after(0, lambda error=exc: self._task_failed("Prompt optimization", error))

    def _finish_prompt_optimization(self, result: PromptOptimization) -> None:
        self.intent = result.prompt
        self.prompt_prepared = True
        if hasattr(self, "intent_text") and self.intent_text.winfo_exists():
            self.intent_text.delete("1.0", "end")
            self.intent_text.insert("1.0", result.prompt)
        if hasattr(self, "prompt_status_label") and self.prompt_status_label.winfo_exists():
            self.prompt_status_label.configure(
                text=result.detail + " You can edit the prompt and choose Optimize again.",
                fg=self.colors["success"] if result.used_ai else self.colors["warning"],
            )
        self._set_busy(False, result.detail)
        self._log(result.detail)

    def _start_package(self) -> None:
        self._capture_page()
        modules = self.selected_modules()
        if not modules:
            messagebox.showwarning("Method & Report Creation", "Select at least one module.", parent=self.root)
            return
        default_name = f"{'_'.join(modules)}_{self.asset_type.get()}_web_AI_package.zip"
        destination = filedialog.asksaveasfilename(
            parent=self.root, title="Save web AI package", initialdir=self.output_root.get(), initialfile=default_name,
            defaultextension=".zip", filetypes=(("ZIP package", "*.zip"),),
        )
        if not destination:
            return
        files = list(self.kb_files)
        prompt_text = self.intent
        prompt_prepared = self.prompt_prepared
        small = bool(self.small_context.get())
        self._set_busy(True, "Preparing web AI package...")
        self._log(f"Packaging {len(files)} related file(s) for {', '.join(modules)}.")
        if prompt_prepared and prompt_text.strip():
            self._log("Packaging the visible, user-reviewed optimized prompt without another hidden AI call.")
        elif prompt_text.strip():
            self._log("Packaging the visible requirement inside the standard generation prompt.")
        else:
            self._log("No local request entered; packaging an editable prompt template.")
        threading.Thread(
            target=self._package_worker,
            args=(Path(destination), modules, files, prompt_text, prompt_prepared, small), daemon=True,
        ).start()

    def _package_worker(self, destination: Path, modules: tuple[str, ...], files: list[Path], prompt_text: str, prompt_prepared: bool, small: bool) -> None:
        try:
            if prompt_prepared and prompt_text.strip():
                prompt = PromptOptimization(prompt_text.strip(), True, "Packaged the visible user-reviewed optimized prompt.")
            else:
                prompt = PromptOptimization(
                    base_prompt(
                        self.asset_type.get(), modules, prompt_text,
                        has_method_basis=bool(self.method_basis_md.get().strip()),
                    ), False,
                    "Packaged the visible requirement using the standard editable prompt template.",
                )
            path = create_web_ai_zip(
                destination, asset_type=self.asset_type.get(), modules=modules,
                files=files, prompt=prompt, small_context=small,
            )
            self.root.after(0, lambda: self._finish_package(path, prompt.detail, small))
        except Exception as exc:
            self.root.after(0, lambda error=exc: self._task_failed("Web AI package", error))

    def _finish_package(self, path: Path, detail: str, small: bool) -> None:
        self._set_busy(False, f"Package ready: {path.name}")
        self._log(detail)
        self._log(f"ZIP created: {path}")
        note = "\n\nExtract the ZIP and upload the individual files to a model with a 200 KB file limit." if small else ""
        messagebox.showinfo("Web AI package", f"Package created:\n{path}{note}", parent=self.root)

    def _open_ai_settings(self) -> None:
        config = load_ai_config()
        dialog = tk.Toplevel(self.root)
        dialog.title("AI settings")
        dialog.geometry("620x380")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.colors["window"])
        values = {
            "provider": tk.StringVar(value=str(config.get("provider", "gpt"))),
            "base_url": tk.StringVar(value=config["base_url"]),
            "model": tk.StringVar(value=config["model"]),
            "api_key": tk.StringVar(value=config["api_key"]),
        }
        tk.Label(dialog, text="Prompt optimization API", font=self._font(16, "bold"), bg=self.colors["window"], fg=self.colors["text"]).grid(row=0, column=0, columnspan=2, sticky="w", padx=28, pady=(24, 15))
        tk.Label(dialog, text="Provider", font=self._font(10, "bold"), bg=self.colors["window"], fg=self.colors["text"]).grid(row=1, column=0, sticky="w", padx=(28, 12), pady=7)
        provider_box = ttk.Combobox(
            dialog, textvariable=values["provider"], values=("gpt", "deepseek"),
            state="readonly", font=self._font(10),
        )
        provider_box.grid(row=1, column=1, sticky="ew", padx=(0, 28), pady=7, ipady=6)

        def on_provider_change(_event=None) -> None:
            selected = str(values["provider"].get() or "gpt").strip().lower()
            if selected == "deepseek":
                if not values["base_url"].get().strip():
                    values["base_url"].set("https://api.deepseek.com/v1")
                if not values["model"].get().strip():
                    values["model"].set("deepseek-chat")
            elif selected == "gpt":
                if not values["base_url"].get().strip():
                    values["base_url"].set("https://api.openai.com/v1")
                if not values["model"].get().strip():
                    values["model"].set("gpt-5.5")

        provider_box.bind("<<ComboboxSelected>>", on_provider_change)

        for offset, (key, label) in enumerate((("base_url", "Base URL"), ("model", "Model ID"), ("api_key", "API key")), start=2):
            tk.Label(dialog, text=label, font=self._font(10, "bold"), bg=self.colors["window"], fg=self.colors["text"]).grid(row=offset, column=0, sticky="w", padx=(28, 12), pady=7)
            entry = tk.Entry(dialog, textvariable=values[key], show="*" if key == "api_key" else "", font=self._font(10), relief="solid", bd=1)
            entry.grid(row=offset, column=1, sticky="ew", padx=(0, 28), pady=7, ipady=6)
        dialog.columnconfigure(1, weight=1)

        def save() -> None:
            AI_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
            AI_CONFIG_FILE.write_text(json.dumps({key: variable.get().strip() for key, variable in values.items()}, ensure_ascii=False, indent=2), encoding="utf-8")
            self._log(f"AI settings saved to {AI_CONFIG_FILE}.")
            self._refresh_api_setting_label()
            dialog.destroy()

        self._button(dialog, "Save", save, width=120).grid(row=5, column=1, sticky="e", padx=28, pady=20)

    def _page_import(self) -> None:
        frame = self._page_frame()
        frame.rowconfigure(1, weight=1)
        top = RoundedPanel(frame, fill=self.colors["panel"], border=self.colors["border"], radius=11, padding=8, parent_bg=self.colors["window"], height=128)
        top.grid(row=0, column=0, sticky="ew", pady=(6, 10), ipady=2)
        body = top.body
        body.columnconfigure(0, weight=1)
        kind = "Method" if self.asset_type.get() == "method" else "Report"
        tk.Label(body, text=f"Generated {kind} MD", font=self._font(13, "bold"), bg=body["bg"], fg=self.colors["text"]).grid(row=0, column=0, sticky="w", padx=14, pady=(8, 3))
        tk.Label(body, textvariable=self.source_md, font=self._font(9), bg=body["bg"], fg=self.colors["muted"], anchor="w", wraplength=900, justify="left").grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 8))
        self._button(body, "Choose MD", self._choose_md, width=108).grid(row=0, column=1, rowspan=2, padx=14, pady=8)

        preview = tk.Frame(frame, bg=self.colors["window"])
        preview.grid(row=1, column=0, sticky="nsew")
        preview.columnconfigure(0, weight=1)
        preview.rowconfigure(1, weight=1)
        self.preview_status = tk.Label(preview, text="Choose the generated MD to begin automatic preflight.", font=self._font(10), bg=self.colors["window"], fg=self.colors["muted"], anchor="w")
        self.preview_status.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        self.preview_host = tk.Frame(preview, bg=self.colors["panel"], highlightthickness=1, highlightbackground=self.colors["border"])
        self.preview_host.grid(row=1, column=0, sticky="nsew")
        self.preview_host.columnconfigure(0, weight=1)
        self.preview_host.rowconfigure(0, weight=1)
        self._render_asset_preview()
        if self.source_md.get() and self.preflight is None and not self.busy:
            self._start_preflight()

    def _page_generate(self) -> None:
        frame = self._page_frame()
        panel = RoundedPanel(frame, fill=self.colors["panel"], border=self.colors["border"], radius=12, padding=12, parent_bg=self.colors["window"])
        panel.grid(row=0, column=0, sticky="nsew", pady=6)
        body = panel.body
        body.columnconfigure(1, weight=1)
        kind = "Instrument Method" if self.asset_type.get() == "method" else "Report Template"
        tk.Label(body, text="Ready to generate", font=self._font(16, "bold"), bg=body["bg"], fg=self.colors["text"]).grid(row=0, column=0, columnspan=3, sticky="w", padx=16, pady=(14, 18))
        self._field_label(body, "Asset type", 1)
        self._value_label(body, kind, 1)
        self._field_label(body, "Modules", 2)
        self._value_label(body, ", ".join(self.selected_modules()), 2)
        self._field_label(body, "Source MD", 3)
        self._value_label(body, self.source_md.get(), 3)
        self._field_label(body, "Asset name", 4)
        if self.asset_type.get() == "method":
            tk.Entry(body, textvariable=self.asset_name, font=self._font(10), relief="flat", highlightthickness=1, highlightbackground=self.colors["border"]).grid(row=4, column=1, columnspan=2, sticky="ew", padx=(8, 18), pady=8, ipady=7)
            self._field_label(body, "CM target", 5)
            ttk.Combobox(body, textvariable=self.cm_version, values=("7.2 compatible", "7.3"), state="readonly", font=self._font(10)).grid(row=5, column=1, sticky="w", padx=8, pady=8)
        else:
            report_name = self.preflight.report_spec.template_name if self.preflight and self.preflight.report_spec else self.asset_name.get()
            self.asset_name.set(report_name)
            self._value_label(body, report_name + " (defined by Report MD)", 4)
            self._field_label(body, "Method basis", 5)
            self._value_label(body, self.method_basis_md.get() or "No Method MD linked", 5)
        output_row = 6
        self._field_label(body, "Output folder", output_row)
        tk.Entry(body, textvariable=self.output_root, font=self._font(10), relief="flat", highlightthickness=1, highlightbackground=self.colors["border"]).grid(row=output_row, column=1, sticky="ew", padx=8, pady=8, ipady=7)
        self._button(body, "Choose", self._choose_output, neutral=True, width=116).grid(row=output_row, column=2, padx=(8, 18), pady=8)
        result_text = f"Preview passed. A history manifest will be saved automatically.{chr(10) + str(self.generated_path) if self.generated_path else ''}"
        self.generation_result = tk.Label(body, text=result_text, font=self._font(10), wraplength=850, justify="left", bg=body["bg"], fg=self.colors["primary"] if self.generated_path else self.colors["muted"])
        self.generation_result.grid(row=output_row + 1, column=0, columnspan=3, sticky="w", padx=16, pady=(22, 20))

    def _field_label(self, parent: tk.Misc, text: str, row: int) -> None:
        tk.Label(parent, text=text, font=self._font(10, "bold"), bg=parent["bg"], fg=self.colors["text"], width=15, anchor="w").grid(row=row, column=0, sticky="w", padx=(16, 8), pady=8)

    def _value_label(self, parent: tk.Misc, text: str, row: int) -> None:
        tk.Label(parent, text=text, font=self._font(10), bg=parent["bg"], fg=self.colors["muted"], anchor="w", wraplength=850, justify="left").grid(row=row, column=1, columnspan=2, sticky="w", padx=8, pady=8)

    def _capture_page(self) -> None:
        if hasattr(self, "intent_text") and self.intent_text.winfo_exists():
            self.intent = self.intent_text.get("1.0", "end").strip()

    def go_back(self) -> None:
        if self.busy:
            return
        self._capture_page()
        self.show_step(self.current_step - 1)

    def go_next(self) -> None:
        if self.busy:
            return
        self._capture_page()
        if self.current_step == 2:
            if self.generation_mode == "api":
                if not self.source_md.get().strip():
                    self._start_auto_generate()
                    return
                if not self.preflight or not self.preflight.ready:
                    messagebox.showwarning("Method & Report Creation", "Wait for the MD preflight to finish before continuing.", parent=self.root)
                    return
            else:
                if not self.selected_modules():
                    messagebox.showwarning("Method & Report Creation", "Select at least one module.", parent=self.root)
                    return
            self.show_step(3)
        elif self.current_step == 3:
            if not self.preflight or not self.preflight.ready:
                messagebox.showwarning("Method & Report Creation", "Import an MD that passes preflight before continuing.", parent=self.root)
                return
            self.show_step(4)
        elif self.current_step == 4:
            self._start_generation()

    def _choose_md(self) -> None:
        kind = "Method" if self.asset_type.get() == "method" else "Report"
        value = filedialog.askopenfilename(parent=self.root, title=f"Select generated {kind} MD", filetypes=(("Markdown", "*.md *.MD"), ("All files", "*.*")))
        if value:
            self.source_md.set(value)
            self.preflight = None
            self.generated_path = None
            self._log(f"Selected {kind} MD: {value}")
            self.show_step(3)

    def _choose_method_basis(self) -> None:
        value = filedialog.askopenfilename(
            parent=self.root, title="Select generated Method MD",
            initialdir=str(DEFAULT_PROJECT_ROOT),
            filetypes=(("Markdown", "*.md *.MD"), ("All files", "*.*")),
        )
        if value:
            self.method_basis_md.set(value)
            self.prompt_prepared = False
            self._log(f"Report method basis selected: {value}")
            self._refresh_kb_files()

    def _choose_recent_method_basis(self) -> None:
        records: list[tuple[str, str, Path]] = []
        if DEFAULT_PROJECT_ROOT.is_dir():
            for manifest in sorted(DEFAULT_PROJECT_ROOT.glob("*/project.json"), reverse=True):
                try:
                    payload = json.loads(manifest.read_text(encoding="utf-8"))
                    if payload.get("asset_type") != "method":
                        continue
                    source = Path(str(payload.get("source_md", "")))
                    if source.is_file():
                        records.append((str(payload.get("created_at", "")), str(payload.get("asset_name", source.stem)), source))
                except (OSError, ValueError, TypeError, json.JSONDecodeError):
                    continue
        if not records:
            messagebox.showinfo("Recent methods", "No generated Method MD was found in generation history.", parent=self.root)
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Choose a generated Method MD")
        dialog.geometry("760x430")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.colors["window"])
        tk.Label(
            dialog, text="Recent generated methods", font=self._font(15, "bold"),
            bg=self.colors["window"], fg=self.colors["text"],
        ).pack(anchor="w", padx=24, pady=(22, 10))
        tree = ttk.Treeview(
            dialog, columns=("created", "name", "file"), show="headings",
            style="Wizard.Treeview", selectmode="browse",
        )
        tree.heading("created", text="Created")
        tree.heading("name", text="Method")
        tree.heading("file", text="Method MD")
        tree.column("created", width=150, stretch=False)
        tree.column("name", width=190, stretch=False)
        tree.column("file", width=370, stretch=True)
        tree.pack(fill="both", expand=True, padx=24, pady=(0, 12))
        for index, (created, name, source) in enumerate(records):
            tree.insert("", "end", iid=str(index), values=(created, name, source.name))

        def use_selected(_event=None) -> None:
            selection = tree.selection()
            if not selection:
                return
            source = records[int(selection[0])][2]
            self.method_basis_md.set(str(source))
            self.prompt_prepared = False
            self._refresh_kb_files()
            self._log(f"Recent generated Method MD linked to report: {source}")
            dialog.destroy()

        tree.bind("<Double-Button-1>", use_selected)
        self._button(dialog, "Use selected", use_selected, width=132).pack(anchor="e", padx=24, pady=(0, 20))

    def _start_preflight(self) -> None:
        path = Path(self.source_md.get())
        self._set_busy(True, "Checking MD structure and compiler compatibility...")
        self._log(f"Preflight started: {path.name}")
        threading.Thread(target=self._preflight_worker, args=(self.asset_type.get(), path), daemon=True).start()

    def _preflight_worker(self, asset_type: str, path: Path) -> None:
        try:
            result = preflight_asset(asset_type, path)
            self.root.after(0, lambda: self._finish_preflight(result))
        except Exception as exc:
            self.root.after(0, lambda error=exc: self._task_failed("Preview", error))

    def _finish_preflight(self, result: AssetPreflight) -> None:
        self.preflight = result
        detail = f"{len(result.errors)} error(s), {len(result.warnings)} warning(s)"
        self._log(f"Preflight finished: {detail}.")
        self._set_busy(False, "Preview ready." if result.ready else "MD contains blocking issues.")
        if self.current_step == 3:
            self.show_step(3)

    def _render_asset_preview(self) -> None:
        for child in self.preview_host.winfo_children():
            child.destroy()
        if self.preflight is None:
            return
        result = self.preflight
        warning_text = f" {len(result.warnings)} warning(s)." if result.warnings else ""
        if result.ready:
            self.preview_status.configure(text="Ready to generate." + warning_text, fg=self.colors["primary"])
        else:
            self.preview_status.configure(
                text=f"Blocked: {len(result.errors)} error(s). Regenerate the MD or contact xiaoshu.guan@thermofisher.com.",
                fg=self.colors["error"],
            )
        if self.asset_type.get() == "method":
            self._render_method_tree(result)
        else:
            self._render_report_tree(result)

    def _tree_shell(self, columns: tuple[str, ...]) -> tuple[ttk.Treeview, ttk.Scrollbar, ttk.Scrollbar]:
        tree = ttk.Treeview(self.preview_host, columns=columns, show="headings", style="Wizard.Treeview")
        ybar = ttk.Scrollbar(self.preview_host, orient="vertical", command=tree.yview)
        xbar = ttk.Scrollbar(self.preview_host, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=ybar.set, xscrollcommand=xbar.set)
        tree.grid(row=0, column=0, sticky="nsew")
        ybar.grid(row=0, column=1, sticky="ns")
        xbar.grid(row=1, column=0, sticky="ew")
        return tree, ybar, xbar

    def _render_method_tree(self, result: AssetPreflight) -> None:
        columns = ("number", "kind", "time", "command", "value", "comment")
        tree, _, _ = self._tree_shell(columns)
        widths = (62, 90, 130, 360, 430, 460)
        for name, width in zip(columns, widths):
            tree.heading(name, text="#" if name == "number" else name.title())
            tree.column(name, width=width, minwidth=width, stretch=False)
        tree.tag_configure("cm_stage", background=self.colors["stage"], foreground=self.colors["text"])
        tree.tag_configure("cm_branch", background=self.colors["branch"], foreground="#14532D")
        tree.tag_configure("cm_comment", foreground=self.colors["comment"])
        tree.tag_configure("cm_command", background=self.colors["row"], foreground=self.colors["text"])
        tree.tag_configure("cm_end", background=self.colors["stage"], foreground="#7C2D12")
        tree.tag_configure("cm_invalid", background=self.colors["error_soft"], foreground="#991B1B")
        invalid = lint_error_rows(result.method_rows)
        for row in result.method_rows:
            row_id = str(row.get("#", ""))
            kind = str(row.get("Kind", "")).strip().lower()
            if row_id in invalid:
                tag = "cm_invalid"
            elif kind == "stage":
                tag = "cm_stage"
            elif kind in {"branch", "trigger"}:
                tag = "cm_branch"
            elif kind == "comment":
                tag = "cm_comment"
            elif kind == "end":
                tag = "cm_end"
            else:
                tag = "cm_command"
            tree.insert(
                "", "end",
                values=(row_id, row.get("Kind", ""), row.get("Time", ""), row.get("Command", ""), row.get("Value", ""), row.get("Comment", "")),
                tags=(tag,),
            )
        if result.errors:
            self._issue_panel(result.errors)

    def _render_report_tree(self, result: AssetPreflight) -> None:
        columns = ("type", "sheet", "range", "definition", "source")
        tree, _, _ = self._tree_shell(columns)
        widths = (150, 190, 110, 610, 330)
        for name, width in zip(columns, widths):
            tree.heading(name, text=name.title())
            tree.column(name, width=width, minwidth=width, stretch=False)
        tree.tag_configure("sheet", background=self.colors["stage"], foreground=self.colors["text"])
        tree.tag_configure("formula", background=self.colors["branch"], foreground="#14532D")
        tree.tag_configure("workbook", background="#E0F2FE", foreground="#075985")
        tree.tag_configure("dynamic", background="#F3E8FF", foreground="#6B21A8")
        spec = result.report_spec
        if spec:
            for sheet in spec.sheets:
                tree.insert("", "end", values=("Sheet", sheet.name, "", f"active={sheet.is_active}; each_injection={sheet.each_injection}", ""), tags=("sheet",))
            for item in spec.patches:
                tree.insert("", "end", values=("CM formula", item.sheet_name, item.excel_range, item.formula, item.fixed_channel or item.fixed_component), tags=("formula",))
            for item in spec.workbook_patches:
                tree.insert("", "end", values=("Workbook " + item.value_type, item.sheet_name, item.excel_range, item.value, item.number_format), tags=("workbook",))
            for item in spec.dynamic_tables:
                tree.insert("", "end", values=("Dynamic table", item.sheet_name, item.excel_range, item.table_type, item.processing_method), tags=("dynamic",))
        if result.errors:
            self._issue_panel(result.errors)

    def _issue_panel(self, errors: list[str]) -> None:
        text = tk.Text(self.preview_host, height=5, font=("Consolas", 9), bg="#FFF5F4", fg=self.colors["error"], relief="flat", wrap="word")
        text.insert("1.0", "Regenerate the MD or contact xiaoshu.guan@thermofisher.com.\n\n" + "\n".join(errors))
        text.configure(state="disabled")
        text.grid(row=2, column=0, columnspan=2, sticky="ew")

    def _start_generation(self) -> None:
        if self.preflight is None or not self.preflight.ready:
            return
        if not self.asset_name.get().strip():
            messagebox.showwarning("Method & Report Creation", "Enter the asset name.", parent=self.root)
            return
        request = AssetGenerationRequest(
            self.asset_type.get(), self.asset_name.get().strip(), ", ".join(self.selected_modules()), self.intent,
            self.cm_version.get(), Path(self.source_md.get()), Path(self.output_root.get()),
            basis_method_md=Path(self.method_basis_md.get()) if self.method_basis_md.get().strip() else None,
        )
        self._set_busy(True, "Generating standalone CMBX and history manifest...")
        self._log(f"CMBX generation started for {request.asset_name}.")
        threading.Thread(target=self._generation_worker, args=(request, self.preflight), daemon=True).start()

    def _generation_worker(self, request: AssetGenerationRequest, preflight: AssetPreflight) -> None:
        try:
            result = generate_asset(request, preflight)
            self.root.after(0, lambda: self._finish_generation(result.project_dir))
        except Exception as exc:
            self.root.after(0, lambda error=exc: self._task_failed("Generation", error))

    def _finish_generation(self, project_dir: Path) -> None:
        self.generated_path = project_dir
        self._set_busy(False, f"Generated: {project_dir}")
        self._log(f"CMBX and history manifest generated: {project_dir}")
        if self.current_step == 3:
            self.show_step(3)
        messagebox.showinfo("Method & Report Creation", f"CMBX generated successfully:\n\n{project_dir}", parent=self.root)

    def _set_busy(self, busy: bool, text: str) -> None:
        self.busy = busy
        self.status_label.configure(text=text)
        self.back_button.configure(state="disabled" if busy or self.current_step == 0 else "normal")
        self.next_button.configure(state="disabled" if busy else "normal", cursor="watch" if busy else "hand2")
        if hasattr(self, "optimize_prompt_button") and self.optimize_prompt_button.winfo_exists():
            self.optimize_prompt_button.configure(state="disabled" if busy else "normal")
        if hasattr(self, "api_generate_button") and self.api_generate_button.winfo_exists():
            self.api_generate_button.configure(state="disabled" if busy else "normal")

    def _task_failed(self, label: str, error: Exception) -> None:
        self._set_busy(False, f"{label} failed: {error}")
        self._log(f"ERROR - {label}: {error}")
        messagebox.showerror("Method & Report Creation", str(error), parent=self.root)

    def _choose_output(self) -> None:
        value = filedialog.askdirectory(parent=self.root, title="Select generation history folder", initialdir=self.output_root.get())
        if value:
            self.output_root.set(value)

    def _open_selected_kb(self, _event=None) -> None:
        if not hasattr(self, "docs_tree"):
            return
        selection = self.docs_tree.selection()
        if selection:
            index = int(selection[0])
            if 0 <= index < len(self.kb_files):
                self._open_path(self.kb_files[index])

    @staticmethod
    def _open_path(path: Path) -> None:
        if os.name == "nt":
            os.startfile(path)  # type: ignore[attr-defined]
        else:
            subprocess.Popen(["xdg-open", str(path)])


def main() -> None:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--asset", choices=("method", "report"))
    args, _unknown = parser.parse_known_args()
    enable_dpi_awareness()
    root = tk.Tk()
    MethodReportCreationWindow(root, initial_asset=args.asset)
    root.mainloop()


if __name__ == "__main__":
    main()
