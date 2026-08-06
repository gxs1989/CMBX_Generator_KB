from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


SHAREPOINT_SHORTCUT_NAME = "CIC HPCS V&V-CMBX Workstation - CMBX"


def _default_shared_root(state_root: Path) -> Path:
    for variable in ("OneDriveCommercial", "OneDrive"):
        one_drive = os.environ.get(variable, "").strip()
        if not one_drive:
            continue
        shortcut = Path(one_drive) / SHAREPOINT_SHORTCUT_NAME
        if shortcut.is_dir():
            return shortcut
    return state_root / "shared"


@dataclass(frozen=True)
class WebWorkspaceConfig:
    state_root: Path
    shared_root: Path
    local_root: Path | None = None
    max_upload_bytes: int = 2 * 1024 * 1024 * 1024
    worker_count: int = 2
    trust_proxy_user: bool = False
    dev_user: str = ""
    admin_users: tuple[str, ...] = ()
    method_api_daily_limit: int = 3
    desktop_ai_owner: str = "xiaoshu.guan@thermofisher.com"
    require_login: bool = False
    developer_daily_limit: int = 10
    allow_developer_self_registration: bool = False
    developer_bootstrap_password: str = "000000"
    windows_login_enabled: bool = False

    @classmethod
    def from_environment(cls) -> "WebWorkspaceConfig":
        program_data = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData"))
        state_root = Path(
            os.environ.get("CMBX_WEB_STATE_ROOT", "")
            or program_data / "CMBX Web Service"
        )
        shared_root_value = os.environ.get("CMBX_WEB_SHARED_ROOT", "").strip()
        shared_root = Path(shared_root_value) if shared_root_value else _default_shared_root(state_root)
        local_root_value = os.environ.get("CMBX_WEB_LOCAL_ROOT", "").strip()
        local_app_data = Path(os.environ.get("LOCALAPPDATA", "").strip() or state_root)
        local_root = Path(local_root_value) if local_root_value else local_app_data / "CMBX Web Workspace"
        return cls(
            state_root=state_root,
            shared_root=shared_root,
            local_root=local_root,
            max_upload_bytes=int(os.environ.get("CMBX_WEB_MAX_UPLOAD_BYTES", 2 * 1024 * 1024 * 1024)),
            worker_count=max(1, int(os.environ.get("CMBX_WEB_WORKERS", "2"))),
            trust_proxy_user=os.environ.get("CMBX_WEB_TRUST_PROXY_USER", "0") == "1",
            dev_user=os.environ.get("CMBX_WEB_DEV_USER", ""),
            admin_users=tuple(
                value.strip().lower()
                for value in os.environ.get(
                    "CMBX_WEB_ADMIN_USERS", "xiaoshu.guan@thermofisher.com"
                ).split(";")
                if value.strip()
            ),
            method_api_daily_limit=max(0, int(os.environ.get("CMBX_WEB_METHOD_API_DAILY_LIMIT", "3"))),
            desktop_ai_owner=os.environ.get(
                "CMBX_WEB_DESKTOP_AI_OWNER", "xiaoshu.guan@thermofisher.com"
            ).strip().lower(),
            require_login=os.environ.get("CMBX_WEB_REQUIRE_LOGIN", "1") == "1",
            developer_daily_limit=max(0, int(os.environ.get("CMBX_WEB_DEVELOPER_DAILY_LIMIT", "10"))),
            allow_developer_self_registration=os.environ.get(
                "CMBX_WEB_ALLOW_DEVELOPER_SELF_REGISTRATION", "0"
            ) == "1",
            developer_bootstrap_password=os.environ.get(
                "CMBX_WEB_DEVELOPER_BOOTSTRAP_PASSWORD", "000000"
            ),
            windows_login_enabled=os.environ.get("CMBX_WEB_WINDOWS_LOGIN_ENABLED", "0") == "1",
        )

    @property
    def database_path(self) -> Path:
        return self.state_root / "state" / "web_workspace.db"

    @property
    def inventory_root(self) -> Path:
        return self.state_root / "cache" / "inventory"

    @property
    def temp_root(self) -> Path:
        return self.state_root / "temp"

    @property
    def log_root(self) -> Path:
        return self.state_root / "logs"

    @property
    def local_storage_root(self) -> Path:
        # Explicit test/config instances remain isolated under their state root.
        return self.local_root or self.state_root / "local"

    @property
    def asset_root(self) -> Path:
        return self.local_storage_root / "assets"

    @property
    def work_root(self) -> Path:
        return self.local_storage_root / "work"

    def ensure_directories(self) -> None:
        for path in (
            self.database_path.parent,
            self.inventory_root,
            self.temp_root,
            self.log_root,
            self.asset_root,
            self.work_root,
            self.shared_root / "01_Inbox",
            self.shared_root / "02_Workspaces",
            self.shared_root / "03_Generated",
            self.shared_root / "04_Analysis",
            self.shared_root / "05_Approved",
            self.shared_root / "90_Archive",
        ):
            path.mkdir(parents=True, exist_ok=True)
