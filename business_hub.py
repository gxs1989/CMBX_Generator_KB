from __future__ import annotations

import ctypes
import os
import subprocess
import sys
import tkinter as tk
import webbrowser
from dataclasses import dataclass
from pathlib import Path
from tkinter import messagebox, ttk

from business_ui_components import RoundedButton, _rounded_polygon


APP_TITLE = "CMBX Workspace"
APP_SUBTITLE = "Guided methods, data, verification and quality"
APP_VERSION = "V1.4 Business Preview"
APP_DIR = Path(__file__).resolve().parent
APPSLAB_URL = "https://appslab.thermofisher.com/"


@dataclass(frozen=True)
class BusinessCenter:
    id: str
    number: int
    title: str
    description: str
    inputs: str
    outputs: str
    action: str
    status: str


@dataclass(frozen=True)
class Journey:
    id: str
    title: str
    description: str
    center_ids: tuple[str, ...]


CENTERS: tuple[BusinessCenter, ...] = (
    BusinessCenter(
        "method-generation", 1, "Instrument Method Generation",
        "Prepare web-AI evidence, review Method MD and compile a traceable method CMBX.",
        "Test intent, Method MD and module SPEC/KB", "Method CMBX and generation history",
        "method_creation", "native",
    ),
    BusinessCenter(
        "report-generation", 2, "Report Template Generation",
        "Generate a report from a reviewed Report MD, optionally grounded in a generated Method MD.",
        "Method basis, Report MD and module SPEC/KB", "Report-template CMBX and generation history",
        "report_creation", "native",
    ),
    BusinessCenter(
        "hplc-applications", 3, "HPLC Applications & Workflows",
        "Discover, import, understand and adapt complete Thermo Scientific HPLC applications.",
        "AppsLab eWorkflow, application documents, local configuration and sample plan",
        "Local application project, compatibility report and derived assets",
        "appslab", "planned",
    ),
    BusinessCenter(
        "raw-export", 4, "Batch Raw Data Export",
        "Select a function first, then build a multi-CMBX workspace and export matching raw channels.",
        "One or many CMBX files or folders", "Filtered raw-data TSV exports",
        "raw_export", "native",
    ),
    BusinessCenter(
        "chromatograms", 5, "Chromatograms & Integration",
        "Build a CMBX workspace, compare channel traces and inspect external integration results.",
        "One or many CMBX files or folders", "Interactive chromatograms and integration results",
        "chromatograms", "native",
    ),
    BusinessCenter(
        "direct-formulas", 6, "Direct CM Formula Results",
        "Build a CMBX workspace and batch-evaluate useful or embedded Direct CM formulas.",
        "One or many CMBX files or folders", "Cross-injection formula result lists",
        "direct_formulas", "native",
    ),
    BusinessCenter(
        "foq-check", 7, "FOQ Quick Check",
        "One-click calculation of mapped FOQ values with SPEC decisions and historical comparison.",
        "Completed FOQ CMBX files, FOQ Location workbook and optional historical database",
        "Comparable metrics, pass/fail, history alerts, charts and report-cell evidence",
        "foq_check", "native",
    ),
    BusinessCenter(
        "quality-data", 8, "Quality Data & Database",
        "Read production history, inspect metric distributions and monitor QC control limits.",
        "SQL Server or DSN data source and a quality table",
        "Historical records, summary statistics and QC control charts",
        "quality_data", "native",
    ),
)

JOURNEYS: tuple[Journey, ...] = (
    Journey("design", "Design & Generate", "Create methods, reports and reusable HPLC application assets.", ("method-generation", "report-generation", "hplc-applications")),
    Journey("analyze", "Chromatograms & Results", "Choose an outcome first, then build the CMBX workspace used by that workflow.", ("raw-export", "chromatograms", "direct-formulas")),
    Journey("quality", "Quality Control & Database", "Check FOQ results, compare specifications and track quality history.", ("foq-check", "quality-data")),
)

# Compatibility alias for callers from the first preview.
WORKFLOWS = JOURNEYS

CENTER_LIMITATIONS = {
    "method-generation": "Requires a reviewed Method MD. Final execution still depends on matching Chromeleon instrument configuration.",
    "report-generation": "Compiles supported report structures and formulas. Complex processing-method integration remains a separate workflow.",
    "hplc-applications": "Application discovery is available through AppsLab; the managed local application library is still planned.",
    "raw-export": "Exports collected raw signals only; it does not reinterpret processing-method results.",
    "chromatograms": "External integration is available for review, but it is not yet a complete replacement for every Chromeleon integration event.",
    "direct-formulas": "Focuses on Direct CM formulas. FormulaOne workbook logic is intentionally excluded from the fast formula catalog.",
    "foq-check": "Requires a completed CMBX and supported FOQ Location/report contract. Missing mappings remain visible for review.",
    "quality-data": "Provides historical filtering and QC statistics. Predictive failure models and Power BI publishing are not yet included.",
}


def center_by_id(center_id: str) -> BusinessCenter:
    return next(center for center in CENTERS if center.id == center_id)


def workflow_by_id(workflow_id: str) -> Journey:
    return next(journey for journey in JOURNEYS if journey.id == workflow_id)


def task_by_id(task_id: str) -> BusinessCenter:
    return center_by_id(task_id)


def python_gui_executable(executable: str | Path | None = None) -> Path:
    current = Path(executable or sys.executable).resolve()
    if current.name.lower() == "python.exe" and current.with_name("pythonw.exe").exists():
        return current.with_name("pythonw.exe")
    return current


def child_command(script_name: str, executable: str | Path | None = None, *args: str) -> list[str]:
    script = APP_DIR / script_name
    if not script.is_file():
        raise FileNotFoundError(script)
    return [str(python_gui_executable(executable)), "-B", str(script), *args]


class BusinessMindMap(tk.Canvas):
    """Responsive business map with optional preview-first Home navigation."""

    JOURNEY_COLORS = {
        "design": ("#EAF4FE", "#267DCC"),
        "analyze": ("#EAF7F3", "#187A65"),
        "quality": ("#FFF4E5", "#A45B00"),
    }

    def __init__(self, parent: tk.Misc, journeys: tuple[Journey, ...], on_journey, on_center, colors: dict[str, str], on_preview=None):
        super().__init__(parent, bg=colors["bg"], highlightthickness=0, bd=0, height=475)
        self.journeys = journeys
        self.on_journey = on_journey
        self.on_center = on_center
        self.colors = colors
        self.on_preview = on_preview
        self.focus_kind = ""
        self.focus_id = ""
        self.animation_progress = 1.0
        self.animation_job = None
        self.bind("<Configure>", self._draw)

    def _draw(self, _event=None) -> None:
        self.delete("all")
        width = max(720, self.winfo_width())
        if not self.on_preview or not self.focus_kind:
            self._draw_full(width)
        else:
            self._draw_focus(width)

    def _full_layout(self, width: int):
        root_w,root_h,category_h,task_h=210,54,62,58
        margin,gap=20,22;branch_count=max(1,len(self.journeys))
        column_w=min(330,max(210,(width-margin*2-gap*(branch_count-1))//branch_count))
        total_w=column_w*branch_count+gap*(branch_count-1);start_x=(width-total_w)//2
        layout={"root":(width//2-root_w//2,12,width//2+root_w//2,12+root_h)}
        for index,journey in enumerate(self.journeys):
            x1=start_x+index*(column_w+gap);x2=x1+column_w
            layout[f"journey:{journey.id}"]=(x1,128,x2,128+category_h)
            for task_index,center_id in enumerate(journey.center_ids):
                top=246+task_index*84;layout[f"center:{center_id}"]=(x1+12,top,x2-12,top+task_h)
        return layout

    def _draw_full(self,width: int) -> None:
        layout=self._full_layout(width);connector="#C9CDD3";root=layout["root"];root_x=(root[0]+root[2])//2;junction_y=98
        self._node("root",*root,"CMBX Workspace",self.colors["thermo_red"],"#FFFFFF",None,bold=True)
        journey_centers=[]
        for journey in self.journeys:
            box=layout[f"journey:{journey.id}"];journey_centers.append((box[0]+box[2])//2)
        self.create_line(root_x,root[3],root_x,junction_y,fill=connector,width=2)
        if journey_centers:self.create_line(journey_centers[0],junction_y,journey_centers[-1],junction_y,fill=connector,width=2)
        for journey in self.journeys:
            box=layout[f"journey:{journey.id}"];center_x=(box[0]+box[2])//2;soft,accent=self.JOURNEY_COLORS[journey.id]
            self.create_line(center_x,junction_y,center_x,box[1],fill=connector,width=2)
            self._node(f"journey:{journey.id}",*box,journey.title,soft,accent,lambda jid=journey.id:self._select_preview("journey",jid),bold=True)
            previous=box[3]
            for center_id in journey.center_ids:
                task_box=layout[f"center:{center_id}"];self.create_line(center_x,previous,center_x,task_box[1],fill=connector,width=2)
                center=center_by_id(center_id)
                self._node(f"center:{center_id}",*task_box,center.title,"#FFFFFF",self.colors["text"],lambda cid=center_id:self._select_preview("center",cid),outline=accent)
                previous=task_box[3]

    def _draw_focus(self,width: int) -> None:
        progress=self._ease(self.animation_progress);full=self._full_layout(width);left_width=max(370,int(width*.47));center_x=left_width//2
        root_target=(center_x-105,28,center_x+105,82)
        journey=self._focused_journey();journey_target=(center_x-150,142,center_x+150,204)
        nodes=[("root",full["root"],root_target)]
        journey_key=f"journey:{journey.id}";nodes.append((journey_key,full[journey_key],journey_target))
        if self.focus_kind=="center":
            center_ids=(self.focus_id,);tops=(276,)
        else:
            center_ids=journey.center_ids;tops=tuple(260+index*84 for index in range(len(center_ids)))
        for center_id,top in zip(center_ids,tops):
            key=f"center:{center_id}";nodes.append((key,full[key],(center_x-140,top,center_x+140,top+58)))
        current={key:self._interpolate(source,target,progress) for key,source,target in nodes}
        root=current["root"];jbox=current[journey_key];connector="#C9CDD3"
        self.create_line((root[0]+root[2])//2,root[3],(jbox[0]+jbox[2])//2,jbox[1],fill=connector,width=2)
        previous=jbox[3]
        for center_id in center_ids:
            box=current[f"center:{center_id}"];self.create_line((jbox[0]+jbox[2])//2,previous,(box[0]+box[2])//2,box[1],fill=connector,width=2);previous=box[3]
        self._node("root",*root,"CMBX Workspace",self.colors["thermo_red"],"#FFFFFF",self._clear_preview,bold=True)
        soft,accent=self.JOURNEY_COLORS[journey.id]
        self._node(journey_key,*jbox,journey.title,soft,accent,lambda jid=journey.id:self._select_preview("journey",jid),bold=True)
        for center_id in center_ids:
            center=center_by_id(center_id);box=current[f"center:{center_id}"]
            self._node(f"center:{center_id}",*box,center.title,"#FFFFFF",self.colors["text"],lambda cid=center_id:self._select_preview("center",cid),outline=accent)
        if progress>.25:self._draw_details(width,left_width,progress,journey)

    def _draw_details(self,width: int,left_width: int,progress: float,journey: Journey) -> None:
        panel_left=int(width+(left_width+28-width)*progress);panel_right=width-22;top,bottom=28,max(430,self.winfo_height()-28)
        _rounded_polygon(self,panel_left,top,panel_right,bottom,12,fill="#F8F9FA",outline=self.colors["border"],width=1)
        x=panel_left+28;text_width=max(260,panel_right-x-26)
        if self.focus_kind=="center":
            center=center_by_id(self.focus_id);eyebrow=journey.title.upper();title=center.title;description=center.description
            sections=(("INPUT",center.inputs),("OUTPUT",center.outputs),("CURRENT BOUNDARY",CENTER_LIMITATIONS.get(center.id,"No additional boundary recorded.")))
            action_text="Click the highlighted task again to open"
        else:
            eyebrow="BUSINESS BRANCH";title=journey.title;description=journey.description
            sections=(("AVAILABLE TASKS","\n".join(f"• {center_by_id(cid).title}" for cid in journey.center_ids)),("HOW TO CONTINUE","Choose a task in the focused branch, or click the branch again to open its task page."))
            action_text="Click a task to inspect it"
        self.create_text(x,top+25,anchor="nw",text=eyebrow,fill=self.colors["muted"],font=("Segoe UI",8,"bold"),width=text_width)
        self.create_text(x,top+55,anchor="nw",text=title,fill=self.colors["text"],font=("Segoe UI",18,"bold"),width=text_width)
        self.create_text(x,top+103,anchor="nw",text=description,fill=self.colors["muted"],font=("Segoe UI",10),width=text_width)
        y=top+165
        for label,value in sections:
            self.create_text(x,y,anchor="nw",text=label,fill=self.colors["muted"],font=("Segoe UI",8,"bold"),width=text_width);y+=24
            item=self.create_text(x,y,anchor="nw",text=value,fill=self.colors["text"],font=("Segoe UI",10),width=text_width);bounds=self.bbox(item);y=(bounds[3] if bounds else y+40)+24
        self.create_text(x,bottom-38,anchor="sw",text=action_text,fill=self.colors["primary"],font=("Segoe UI",9,"bold"),width=text_width)
        back_tag="preview-back";self.create_text(panel_right-24,top+24,anchor="ne",text="Back to all tasks",fill=self.colors["primary"],font=("Segoe UI",9,"bold"),tags=(back_tag,));self.tag_bind(back_tag,"<Button-1>",lambda _event:self._clear_preview());self.tag_bind(back_tag,"<Enter>",lambda _event:self.configure(cursor="hand2"));self.tag_bind(back_tag,"<Leave>",lambda _event:self.configure(cursor=""))

    def _select_preview(self,kind: str,item_id: str) -> None:
        if not self.on_preview:
            (self.on_center(item_id) if kind=="center" else self.on_journey(item_id));return
        if self.focus_kind==kind and self.focus_id==item_id and self.animation_progress>=1:
            (self.on_center(item_id) if kind=="center" else self.on_journey(item_id));return
        self.focus_kind=kind;self.focus_id=item_id;self.animation_progress=0.0
        self.on_preview(kind,item_id);self._animate_focus()

    def _clear_preview(self) -> None:
        if self.animation_job:
            try:self.after_cancel(self.animation_job)
            except tk.TclError:pass
        self.animation_job=None;self.focus_kind="";self.focus_id="";self.animation_progress=1.0;self._draw()
        if self.on_preview:self.on_preview("","")

    def _animate_focus(self) -> None:
        self.animation_progress=min(1.0,self.animation_progress+.075);self._draw()
        if self.animation_progress<1.0:self.animation_job=self.after(16,self._animate_focus)
        else:self.animation_job=None

    def _focused_journey(self) -> Journey:
        if self.focus_kind=="journey":return workflow_by_id(self.focus_id)
        return next(journey for journey in self.journeys if self.focus_id in journey.center_ids)

    @staticmethod
    def _interpolate(source,target,progress):
        return tuple(int(a+(b-a)*progress) for a,b in zip(source,target))

    @staticmethod
    def _ease(value: float) -> float:
        return 1-(1-value)**3

    def _node(
        self,
        node_id: str,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        text: str,
        fill: str,
        foreground: str,
        command,
        *,
        bold: bool = False,
        outline: str | None = None,
    ) -> None:
        tag = f"node::{node_id}"
        shape = _rounded_polygon(
            self, x1, y1, x2, y2, 10,
            fill=fill, outline=outline or fill, width=1.4, tags=(tag,),
        )
        label = self.create_text(
            (x1 + x2) // 2, (y1 + y2) // 2, text=text,
            fill=foreground, width=max(120, x2 - x1 - 24), justify="center",
            font=("Segoe UI", 11, "bold" if bold else "normal"), tags=(tag,),
        )
        if command is not None:
            hover_fill = self.colors["primary_soft"] if fill == "#FFFFFF" else "#F3F8FD"
            self.tag_bind(tag, "<Button-1>", lambda _e, action=command: action())
            self.tag_bind(tag, "<Enter>", lambda _e, item=shape, color=hover_fill: self._hover(item, color, True))
            self.tag_bind(tag, "<Leave>", lambda _e, item=shape, color=fill: self._hover(item, color, False))

    def _hover(self, shape: int, fill: str, active: bool) -> None:
        self.itemconfigure(shape, fill=fill)
        self.configure(cursor="hand2" if active else "")


class BusinessHubApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.colors = {
            "bg": "#FFFFFF", "surface": "#FFFFFF", "surface_alt": "#F6F6F7", "border": "#E3E4E7",
            "text": "#222326", "muted": "#8A8D91", "primary": "#3598F5", "primary_hover": "#2389EB",
            "primary_soft": "#EAF4FE", "success": "#198754", "success_soft": "#E9F7EF",
            "warning": "#A85D00", "warning_soft": "#FFF4DF", "info": "#175CD3", "info_soft": "#EFF8FF",
            "thermo_red": "#D71920", "thermo_red_hover": "#B91219", "thermo_red_soft": "#FDECEE",
        }
        self.nav_buttons: dict[str, RoundedButton] = {}
        self.status_var = tk.StringVar(value="Ready")
        self._setup_window()
        self._build_shell()
        self.show_home()

    def _setup_window(self) -> None:
        self.root.title(f"{APP_TITLE} - {APP_VERSION}")
        self.root.geometry("1320x850")
        self.root.minsize(1080, 700)
        self.root.configure(bg=self.colors["bg"])
        try: self.root.state("zoomed")
        except tk.TclError: pass

    def _font(self, size: int, weight: str = "normal") -> tuple[str, int, str]:
        return ("Segoe UI", size, weight)

    def _build_shell(self) -> None:
        self.root.columnconfigure(1, weight=1); self.root.rowconfigure(0, weight=1)
        sidebar = tk.Frame(self.root, bg=self.colors["surface_alt"], width=265, highlightthickness=1, highlightbackground=self.colors["border"])
        sidebar.grid(row=0, column=0, sticky="nsw"); sidebar.grid_propagate(False)
        tk.Label(sidebar, text=APP_TITLE, font=self._font(15, "bold"), bg=self.colors["surface_alt"], fg=self.colors["text"]).pack(anchor="w", padx=30, pady=(30, 3))
        tk.Label(sidebar, text="Method, data and quality", wraplength=205, justify="left", font=self._font(9), bg=self.colors["surface_alt"], fg=self.colors["muted"]).pack(anchor="w", padx=30, pady=(0, 26))
        nav = tk.Frame(sidebar, bg=self.colors["surface_alt"]); nav.pack(fill="x", padx=18)
        self._add_nav(nav, "home", "Home", self.show_home)
        for journey in JOURNEYS:
            self._add_nav(nav, journey.id, journey.title, lambda jid=journey.id: self.show_journey(jid))
        footer = tk.Frame(sidebar, bg=self.colors["surface_alt"]); footer.pack(side="bottom", fill="x", padx=30, pady=26)
        tk.Label(footer, text="ADVANCED / FALLBACK", font=self._font(8, "bold"), bg=self.colors["surface_alt"], fg=self.colors["muted"]).pack(anchor="w")
        self._text_button(footer, "Open legacy Explorer", lambda: self._run_action("legacy")).pack(fill="x", pady=(7, 0))

        main = tk.Frame(self.root, bg=self.colors["bg"]); main.grid(row=0, column=1, sticky="nsew")
        main.columnconfigure(0, weight=1); main.rowconfigure(1, weight=1)
        top = tk.Frame(main, bg=self.colors["surface"], height=60, highlightthickness=1, highlightbackground=self.colors["border"])
        top.grid(row=0, column=0, sticky="ew"); top.grid_propagate(False); top.columnconfigure(0, weight=1)
        self.breadcrumb = tk.Label(top, text="Workspace / Home", font=self._font(9), bg=self.colors["surface"], fg=self.colors["muted"])
        self.breadcrumb.grid(row=0, column=0, sticky="w", padx=28, pady=19)
        tk.Label(top, text="Legacy tools are fallback only", font=self._font(8), bg=self.colors["surface"], fg=self.colors["muted"]).grid(row=0, column=1, padx=28)
        self.content = tk.Frame(main, bg=self.colors["bg"]); self.content.grid(row=1, column=0, sticky="nsew")
        self.content.columnconfigure(0, weight=1); self.content.rowconfigure(0, weight=1)
        status = tk.Frame(main, bg=self.colors["surface"], height=36, highlightthickness=1, highlightbackground=self.colors["border"])
        status.grid(row=2, column=0, sticky="ew"); status.grid_propagate(False)
        tk.Label(status, textvariable=self.status_var, font=self._font(8), bg=self.colors["surface"], fg=self.colors["muted"]).pack(anchor="w", padx=28, pady=9)

    def _add_nav(self, parent: tk.Misc, route: str, text: str, command) -> None:
        is_home = route == "home"
        button = RoundedButton(
            parent, text, command, width=215, height=43, radius=9,
            bg=self.colors["thermo_red_soft"] if is_home else self.colors["surface_alt"],
            hover_bg=self.colors["thermo_red"] if is_home else self.colors["primary_soft"],
            fg=self.colors["thermo_red"] if is_home else self.colors["muted"],
            border=self.colors["thermo_red_soft"] if is_home else self.colors["surface_alt"],
            parent_bg=self.colors["surface_alt"], font=self._font(9), anchor="w",
        )
        button.pack(fill="x", pady=1)
        self.nav_buttons[route] = button

    def _text_button(self, parent: tk.Misc, text: str, command) -> tk.Button:
        return tk.Button(parent, text=text, command=command, anchor="w", font=self._font(8), relief="flat", bd=0, padx=0, pady=4, cursor="hand2", bg=self.colors["surface_alt"], fg=self.colors["muted"], activebackground=self.colors["surface_alt"], activeforeground=self.colors["primary"])

    def _button(self, parent: tk.Misc, text: str, command, neutral: bool = False) -> RoundedButton:
        bg = self.colors["surface"] if neutral else self.colors["primary"]
        fg = self.colors["text"] if neutral else "#FFFFFF"
        hover = self.colors["surface_alt"] if neutral else self.colors["primary_hover"]
        return RoundedButton(
            parent, text, command, width=140, height=42, radius=9,
            bg=bg, hover_bg=hover, fg=fg,
            border=self.colors["border"] if neutral else self.colors["primary"],
            parent_bg=str(parent.cget("bg")), font=self._font(9, "bold"),
        )

    def _select(self, route: str) -> None:
        for key, button in self.nav_buttons.items():
            selected = key == route
            if key == "home":
                button.configure(
                    bg=self.colors["thermo_red"] if selected else self.colors["thermo_red_soft"],
                    fg="#FFFFFF" if selected else self.colors["thermo_red"],
                    font=self._font(9, "bold"),
                )
            else:
                button.configure(
                    bg=self.colors["primary"] if selected else self.colors["surface_alt"],
                    fg="#FFFFFF" if selected else self.colors["muted"],
                    font=self._font(9, "bold" if selected else "normal"),
                )

    def _page(self) -> tk.Frame:
        for child in self.content.winfo_children(): child.destroy()
        page = tk.Frame(self.content, bg=self.colors["bg"]); page.grid(row=0, column=0, sticky="nsew", padx=36, pady=30)
        page.columnconfigure(0, weight=1)
        return page

    def _heading(self, parent: tk.Misc, eyebrow: str, title: str, description: str, icon: str = "") -> None:
        tk.Label(parent, text=eyebrow.upper(), font=self._font(8, "bold"), bg=self.colors["bg"], fg=self.colors["muted"]).grid(row=0, column=0, sticky="w")
        title_row = tk.Frame(parent, bg=self.colors["bg"])
        title_row.grid(row=1, column=0, sticky="w", pady=(6, 0))
        tk.Label(title_row, text=title, font=self._font(20, "bold"), bg=self.colors["bg"], fg=self.colors["text"]).pack(side="left")
        if icon:
            tk.Label(title_row, text=icon, font=("Segoe UI Emoji", 20), bg=self.colors["bg"], fg=self.colors["text"]).pack(side="left", padx=(9, 0))
        tk.Label(parent, text=description, font=self._font(10), bg=self.colors["bg"], fg=self.colors["muted"], wraplength=900, justify="left").grid(row=2, column=0, sticky="w", pady=(7, 22))

    def show_home(self) -> None:
        self._select("home"); self.breadcrumb.configure(text="Workspace / Home")
        page = self._page()
        self._heading(
            page, "Workspace", "Choose a task",
            "Select a branch, then open the task you need. Each task starts its real workflow directly.",
            icon="🦎",
        )
        mind_map = BusinessMindMap(page, JOURNEYS, self.show_journey, self.open_center, self.colors, self._preview_home_node)
        mind_map.grid(row=3, column=0, sticky="nsew")
        page.rowconfigure(3, weight=1)
        self.status_var.set("Ready - choose a task from the business map")

    def _preview_home_node(self,kind: str,item_id: str) -> None:
        if not kind:
            self.status_var.set("Ready - choose a task from the business map");return
        if kind=="center":
            title=center_by_id(item_id).title
            self.status_var.set(f"Previewing {title} - click the highlighted task again to open")
        else:
            title=workflow_by_id(item_id).title
            self.status_var.set(f"Previewing {title} - choose a task or click the branch again")

    def show_journey(self, journey_id: str) -> None:
        journey = workflow_by_id(journey_id)
        self._select(journey_id); self.breadcrumb.configure(text=f"Workspace / {journey.title}")
        page = self._page(); self._heading(page, "Choose a task", journey.title, journey.description)
        branch = BusinessMindMap(page, (journey,), self.show_journey, self.open_center, self.colors)
        branch.grid(row=3, column=0, sticky="nsew")
        page.rowconfigure(3, weight=1)
        self.status_var.set(f"{journey.title} - choose a task")

    def open_center(self, center_id: str) -> None:
        center = center_by_id(center_id)
        self.status_var.set(f"Opening {center.title}...")
        self.root.update_idletasks()
        self._run_action(center.action)

    @staticmethod
    def _status_text(status: str) -> str:
        return {"native": "Native guided workflow available", "migrating": "Native workflow migration in progress; legacy fallback only", "partial": "One native component is available; complete center is still migrating", "planned": "Planned"}[status]

    def _run_action(self, action: str) -> None:
        try:
            if action == "method_creation": self._launch_child("run_method_report_creation.py", "Instrument Method Generation", "--asset", "method")
            elif action == "report_creation": self._launch_child("run_method_report_creation.py", "Report Template Generation", "--asset", "report")
            elif action == "raw_export": self._launch_child("run_read_analyze.py", "Batch Raw Data Export", "--task", "raw")
            elif action == "chromatograms": self._launch_child("run_read_analyze.py", "Chromatograms & Integration", "--task", "plot")
            elif action == "direct_formulas": self._launch_child("run_read_analyze.py", "Direct CM Formula Results", "--task", "formula")
            elif action == "foq_check": self._launch_child("run_foq_quality.py", "FOQ Quick Check", "--task", "foq")
            elif action == "quality_data": self._launch_child("run_foq_quality.py", "Quality Data & Database", "--task", "quality")
            elif action == "legacy": self._launch_child("run_app.py", "Legacy CMBX Explorer")
            elif action == "external_report": self._launch_child("run_external_report.py", "External Report Engine")
            elif action == "appslab": webbrowser.open(APPSLAB_URL, new=2); self.status_var.set("Opened Thermo Scientific AppsLab")
            else: raise ValueError(f"Unknown action: {action}")
        except Exception as exc:
            self.status_var.set(f"Could not open task: {exc}")
            messagebox.showerror(APP_TITLE, str(exc), parent=self.root)

    def _launch_child(self, script_name: str, label: str, *args: str) -> None:
        flags = (getattr(subprocess, "CREATE_NO_WINDOW", 0) | getattr(subprocess, "DETACHED_PROCESS", 0)) if os.name == "nt" else 0
        subprocess.Popen(child_command(script_name, None, *args), cwd=str(APP_DIR), creationflags=flags, close_fds=os.name != "nt")
        self.status_var.set(f"Opened {label} in a separate window")


def enable_dpi_awareness() -> None:
    try: ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try: ctypes.windll.user32.SetProcessDPIAware()
        except Exception: pass


def main() -> None:
    enable_dpi_awareness()
    root = tk.Tk(); BusinessHubApp(root); root.mainloop()


if __name__ == "__main__":
    main()
