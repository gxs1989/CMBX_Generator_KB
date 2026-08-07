from __future__ import annotations

import getpass
import hashlib
import os
import re
import shutil
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import Body, Depends, FastAPI, File, HTTPException, Query, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .config import WebWorkspaceConfig
from .inventory import build_inventory, read_inventory
from .jobs import JobManager
from .store import WorkspaceStore
from .foq import database_public_status, inspect_sources, metric_catalog, run_check
from .method_ai import (
    AIProviderSettings,
    PROVIDER_DEFAULTS,
    generate_method_markdown,
    generate_report_markdown,
    public_provider_defaults,
)
from .auth import hash_password, new_session_token, token_digest, verify_password
from .analysis import (
    build_catalog,
    chromatogram_payload,
    evaluate_direct_formulas,
    export_raw_zip,
    leak_sensor_catalog,
    leak_sensor_analysis,
    quality_catalog,
    quality_query,
    scan_direct_formulas,
)
from .foq import load_database_source
from foq_quality_service import default_mapping_path
from generation_project import (
    AssetGenerationRequest,
    configuration_requirements,
    generate_asset,
    preflight_asset,
    recommended_online_kb_files_for_modules,
)
from web_ai_package import PromptOptimization, base_prompt, create_web_ai_zip, load_ai_config, optimize_prompt
from windows_credentials import protect_secret, unprotect_secret
from sequence_package_builder import (
    MultiSequencePackageRequest,
    SequenceInjectionRequest,
    build_multi_sequence_package,
)


APP_VERSION = "0.5.0"
DEFAULT_WORKSPACE_ID = "shared"
SAFE_NAME = re.compile(r"[^A-Za-z0-9._ -]+")
SESSION_COOKIE = "cmbx_session"

PERMISSION_CATALOG = [
    {"id": "instrument_method_generation", "label": "Instrument Method Generation", "group": "Design & Generate", "default": True, "description": "Open the guided Method workflow."},
    {"id": "method_generate", "label": "GPT automatic", "group": "Design & Generate", "parent": "instrument_method_generation", "default": True},
    {"id": "method_manual_web_ai", "label": "Manual Web AI", "group": "Design & Generate", "parent": "instrument_method_generation", "default": False},
    {"id": "method_deepseek", "label": "DeepSeek automatic", "group": "Design & Generate", "parent": "instrument_method_generation", "default": False},
    {"id": "report_generate", "label": "Report Template Generation", "group": "Design & Generate", "default": True, "description": "Prepare Report MD and compile report-template CMBX."},
    {"id": "report_manual_web_ai", "label": "Manual Web AI", "group": "Design & Generate", "parent": "report_generate", "default": False},
    {"id": "sequence_generate", "label": "Sequence Generation", "group": "Design & Generate", "default": True, "description": "Assemble multiple Method MD files and one shared Report MD into a candidate sequence CMBX."},
    {"id": "hplc_applications", "label": "HPLC Applications & Workflows", "group": "Design & Generate", "default": False, "description": "Reserved for the planned application workflow."},
    {"id": "raw_export", "label": "Batch Raw Data Export", "group": "Chromatograms & Results", "default": True, "description": "Filter and export raw channel data."},
    {"id": "chromatogram_plot", "label": "Chromatograms & Integration", "group": "Chromatograms & Results", "default": True, "description": "Plot selected chromatograms."},
    {"id": "chromatogram_integrate", "label": "External integration", "group": "Chromatograms & Results", "parent": "chromatogram_plot", "default": True},
    {"id": "direct_cm_formula", "label": "Direct CM Formula Results", "group": "Chromatograms & Results", "default": True, "description": "Batch-evaluate supported Direct CM formulas."},
    {"id": "foq_check", "label": "FOQ Quick Check", "group": "Quality Control & Database", "default": True, "description": "Compare FOQ metrics with specifications and history."},
    {"id": "database_read", "label": "Quality Data & Database", "group": "Quality Control & Database", "default": True, "description": "Read historical quality data and QC trends."},
    {"id": "database_write", "label": "Controlled database write", "group": "Quality Control & Database", "parent": "database_read", "default": False},
    {"id": "single_verification", "label": "Single Verification", "group": "Single Verification", "default": True, "description": "Run focused development checks directly from CMBX evidence."},
    {"id": "leak_sensor_analysis", "label": "Leak Sensor Analysis", "group": "Single Verification", "parent": "single_verification", "default": True, "description": "Run the established raw-curve leak sensor analysis against CMBX LeakDiff channels."},
]
DEFAULT_PERMISSIONS = [item["id"] for item in PERMISSION_CATALOG if item["default"]]


def _safe_segment(value: str, fallback: str = "item") -> str:
    cleaned = SAFE_NAME.sub("_", Path(value).name).strip(" ._")
    return (cleaned or fallback)[:120]


def _short_file_name(value: str, fallback: str = "asset.bin", max_stem: int = 48) -> str:
    safe = Path(_safe_segment(value, fallback))
    suffix = safe.suffix[:12]
    stem = safe.stem[:max_stem] or Path(fallback).stem
    return f"{stem}{suffix}"


def _public_artifact(record: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in record.items() if key != "storage_path"}


def _migrate_desktop_gpt_setting(store: WorkspaceStore, config: WebWorkspaceConfig) -> bool:
    """Initialize the designated Web owner from the existing desktop AI setting once."""
    owner = config.desktop_ai_owner.strip().lower()
    if not owner or owner not in set(config.admin_users):
        return False
    existing = store.get_ai_setting(owner, "gpt")
    if existing and str(existing.get("encrypted_api_key") or "").strip():
        return False
    desktop = load_ai_config()
    api_key = str(desktop.get("api_key") or "").strip()
    if not api_key:
        return False
    defaults = PROVIDER_DEFAULTS["gpt"]
    store.save_ai_setting(
        owner,
        "gpt",
        str((existing or {}).get("base_url") or desktop.get("base_url") or defaults["base_url"]).strip(),
        str((existing or {}).get("model") or desktop.get("model") or defaults["model"]).strip(),
        protect_secret(api_key),
    )
    return True


def create_app(config: WebWorkspaceConfig | None = None) -> FastAPI:
    config = config or WebWorkspaceConfig.from_environment()
    config.ensure_directories()
    store = WorkspaceStore(config.database_path)
    jobs = JobManager(store, worker_count=config.worker_count)
    static_root = Path(__file__).resolve().parent / "static"

    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        store.ensure_workspace(DEFAULT_WORKSPACE_ID, "CMBX Workstation", _local_identity(config))
        _migrate_desktop_gpt_setting(store, config)
        if (
            config.desktop_ai_owner in set(config.admin_users)
            and not store.get_developer_account(config.desktop_ai_owner)
        ):
            store.save_developer_account(
                config.desktop_ai_owner,
                hash_password("000000"),
                "admin",
                config.developer_daily_limit,
                ["*"],
                True,
            )
        yield
        jobs.shutdown()

    app = FastAPI(
        title="CMBX Workspace API",
        version=APP_VERSION,
        docs_url="/api/docs",
        redoc_url=None,
        lifespan=lifespan,
    )
    app.state.config = config
    app.state.store = store
    app.state.jobs = jobs
    app.mount("/static", StaticFiles(directory=static_root), name="static")

    def windows_identity(user: str, source: str) -> dict[str, Any]:
        normalized = user.lower()
        short_name = normalized.rsplit("\\", 1)[-1].split("@", 1)[0]
        user_id = normalized if "@" in normalized else f"{short_name}@thermofisher.com"
        aliases = {normalized, short_name, user_id}
        configured_admins = set(config.admin_users)
        is_admin = source != "lan_direct" and bool(aliases.intersection(configured_admins))
        account = store.get_developer_account(user_id)
        account_enabled = bool(account and account.get("enabled"))
        return {
            "user": user,
            "user_id": user_id,
            "role": "admin" if is_admin else (str(account["role"]) if account_enabled else "analyst"),
            "source": source,
            "daily_api_limit": int(account["daily_api_limit"]) if account_enabled else config.method_api_daily_limit,
            "permissions": ["*"] if is_admin else (
                list(account["permissions"]) if account_enabled
                else list(DEFAULT_PERMISSIONS)
            ),
        }

    def session_identity(request: Request) -> dict[str, Any] | None:
        token = request.cookies.get(SESSION_COOKIE, "").strip()
        saved = store.get_session(token_digest(token)) if token else None
        if not saved:
            return None
        if saved["source"] == "developer":
            account = store.get_developer_account(saved["user_id"])
            if not account or not account.get("enabled"):
                return None
            return {
                "user": saved["display_name"], "user_id": saved["user_id"],
                "role": account["role"], "source": saved["source"],
                "daily_api_limit": account["daily_api_limit"],
                "permissions": account["permissions"],
            }
        return {
            "user": saved["display_name"], "user_id": saved["user_id"],
            "role": saved["role"], "source": saved["source"],
            "daily_api_limit": saved["daily_api_limit"], "permissions": saved["permissions"],
        }

    def current_identity(request: Request) -> dict[str, Any]:
        if config.trust_proxy_user:
            user = request.headers.get("x-remote-user", "").strip()
            if user:
                return windows_identity(user, "iis")
        saved = session_identity(request)
        if saved:
            return saved
        client_host = request.client.host if request.client else ""
        if not config.require_login:
            if client_host in {"127.0.0.1", "::1", "localhost", "testclient"}:
                return windows_identity(config.dev_user.strip() or getpass.getuser(), "local")
            return windows_identity(f"lan-analyst-{client_host or 'unknown'}", "lan_direct")
        raise HTTPException(status_code=401, detail="Sign in is required")

    def identity_limit(identity: dict[str, Any]) -> int:
        value = identity.get("daily_api_limit")
        return config.method_api_daily_limit if value is None else max(0, int(value))

    def require_admin(identity: dict[str, Any] = Depends(current_identity)) -> dict[str, Any]:
        if identity["role"] != "admin":
            raise HTTPException(status_code=403, detail="Administrator role is required")
        return identity

    def has_permission(identity: dict[str, Any], *required: str) -> bool:
        permissions = set(identity.get("permissions", []))
        return identity["role"] == "admin" or "*" in permissions or bool(permissions.intersection(required))

    def permission_dependency(*required: str, detail: str):
        def check(identity: dict[str, Any] = Depends(current_identity)) -> dict[str, Any]:
            if not has_permission(identity, *required):
                raise HTTPException(status_code=403, detail=detail)
            return identity
        return check

    require_method_generator = permission_dependency(
        "method_generate", "method_manual_web_ai", "method_deepseek",
        detail="Instrument Method generation permission is required",
    )
    require_method_manual = permission_dependency(
        "method_manual_web_ai", detail="Manual Web AI is restricted by the administrator",
    )
    require_report_generator = permission_dependency(
        "report_generate", detail="Report Template generation permission is required",
    )
    require_report_manual = permission_dependency(
        "report_manual_web_ai", detail="Manual Report Web AI is restricted by the administrator",
    )
    require_sequence_generator = permission_dependency(
        "sequence_generate", detail="Sequence generation permission is required",
    )
    require_raw_export = permission_dependency("raw_export", detail="Raw-data export permission is required")
    require_chromatogram_plot = permission_dependency(
        "chromatogram_plot", detail="Chromatogram plotting permission is required",
    )
    require_chromatogram_integrate = permission_dependency(
        "chromatogram_integrate", detail="External integration permission is required",
    )
    require_direct_formula = permission_dependency(
        "direct_cm_formula", detail="Direct CM formula permission is required",
    )
    require_leak_sensor_analysis = permission_dependency(
        "leak_sensor_analysis", detail="Leak Sensor Analysis permission is required",
    )

    def require_foq_check(identity: dict[str, Any] = Depends(current_identity)) -> dict[str, Any]:
        permissions = set(identity.get("permissions", []))
        if identity["role"] != "admin" and "*" not in permissions and "foq_check" not in permissions:
            raise HTTPException(status_code=403, detail="FOQ Quick Check permission is required")
        return identity

    def require_database_read(identity: dict[str, Any] = Depends(current_identity)) -> dict[str, Any]:
        permissions = set(identity.get("permissions", []))
        if identity["role"] != "admin" and "*" not in permissions and "database_read" not in permissions:
            raise HTTPException(status_code=403, detail="Database read permission is required")
        return identity

    @app.get("/", include_in_schema=False)
    def index() -> FileResponse:
        return FileResponse(static_root / "index.html")

    def login_response(identity: dict[str, Any]) -> JSONResponse:
        token = new_session_token()
        store.create_session(
            token_digest(token), identity["user_id"], identity["user"], identity["role"],
            identity["source"], identity.get("daily_api_limit"), identity.get("permissions", []),
        )
        response = JSONResponse({"authenticated": True, "user": identity})
        response.set_cookie(
            SESSION_COOKIE, token, max_age=12 * 60 * 60, httponly=True,
            samesite="lax", secure=False, path="/",
        )
        return response

    @app.get("/api/auth/options")
    def auth_options(request: Request) -> dict[str, Any]:
        try:
            identity = current_identity(request)
        except HTTPException:
            identity = None
        client_host = request.client.host if request.client else ""
        return {
            "authenticated": bool(identity), "user": identity,
            "windows_available": bool(
                config.windows_login_enabled
                and (config.trust_proxy_user or client_host in {"127.0.0.1", "::1", "localhost", "testclient"})
            ),
            "developer_available": True,
            "developer_self_registration": config.allow_developer_self_registration,
        }

    @app.post("/api/auth/windows-login")
    def windows_login(request: Request) -> JSONResponse:
        if not config.windows_login_enabled:
            raise HTTPException(status_code=404, detail="Windows sign-in is disabled")
        if config.trust_proxy_user:
            user = request.headers.get("x-remote-user", "").strip()
            if not user:
                raise HTTPException(status_code=401, detail="IIS did not provide a Windows identity")
            return login_response(windows_identity(user, "iis"))
        client_host = request.client.host if request.client else ""
        if client_host not in {"127.0.0.1", "::1", "localhost", "testclient"}:
            raise HTTPException(status_code=403, detail="Windows sign-in is available through IIS or on the service host")
        return login_response(windows_identity(config.dev_user.strip() or getpass.getuser(), "local_windows"))

    @app.post("/api/auth/developer-login")
    def developer_login(payload: dict[str, Any] = Body(...)) -> JSONResponse:
        email = str(payload.get("email") or "").strip().lower()
        password = str(payload.get("password") or "")
        account = store.get_developer_account(email)
        if (
            account is None
            and config.allow_developer_self_registration
            and password == config.developer_bootstrap_password
            and re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email)
        ):
            account = store.save_developer_account(
                email,
                hash_password(password),
                "analyst",
                config.method_api_daily_limit,
                list(DEFAULT_PERMISSIONS),
                True,
            )
        if not account or not account["enabled"] or not verify_password(password, account["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid or disabled developer account")
        return login_response({
            "user": email, "user_id": email, "role": account["role"], "source": "developer",
            "daily_api_limit": account["daily_api_limit"], "permissions": account["permissions"],
        })

    @app.post("/api/auth/logout")
    def logout(request: Request) -> JSONResponse:
        token = request.cookies.get(SESSION_COOKIE, "").strip()
        if token:
            store.delete_session(token_digest(token))
        response = JSONResponse({"authenticated": False})
        response.delete_cookie(SESSION_COOKIE, path="/")
        return response

    @app.get("/api/health")
    def health(identity: dict[str, str] = Depends(current_identity)) -> dict[str, Any]:
        return {
            "status": "ok",
            "version": APP_VERSION,
            "user": identity,
            "time": datetime.now().astimezone().isoformat(timespec="seconds"),
        }

    @app.get("/api/capabilities")
    def capabilities(_identity: dict[str, str] = Depends(current_identity)) -> dict[str, Any]:
        return {
            "available": [
                "cmbx_upload",
                "cmbx_inventory",
                "persistent_jobs",
                "admin_health",
                "foq_quick_check",
                "method_manual_generation",
                "method_api_generation",
                "method_api_quota_approval",
                "batch_raw_export",
                "chromatogram_compare",
                "external_integration",
                "direct_cm_formulas",
                "report_generation",
                "sequence_generation",
                "quality_database_read",
            ],
            "next": ["hplc_applications", "controlled_database_write"],
            "permissions": list(_identity.get("permissions", [])),
        }

    @app.get("/api/workspaces")
    def list_workspaces(_identity: dict[str, str] = Depends(current_identity)) -> list[dict[str, Any]]:
        return store.list_workspaces()

    @app.get("/api/artifacts")
    def list_artifacts(
        workspace_id: str = Query(DEFAULT_WORKSPACE_ID),
        kind: str = Query(""),
        identity: dict[str, str] = Depends(current_identity),
    ) -> list[dict[str, Any]]:
        items = store.list_artifacts(workspace_id)
        items = [item for item in items if item["owner"].lower() == identity["user"].lower()]
        if kind:
            items = [item for item in items if item["kind"] == kind]
        return [_public_artifact(item) for item in items]

    @app.post("/api/artifacts/upload", status_code=201)
    async def upload_artifact(
        file: UploadFile = File(...),
        workspace_id: str = Query(DEFAULT_WORKSPACE_ID),
        identity: dict[str, str] = Depends(current_identity),
    ) -> dict[str, Any]:
        original_name = _safe_segment(file.filename or "upload.cmbx", "upload.cmbx")
        if Path(original_name).suffix.lower() != ".cmbx":
            raise HTTPException(status_code=400, detail="Only .cmbx files are accepted in this workflow")
        store.ensure_workspace(workspace_id, workspace_id, identity["user"])
        artifact_id = uuid.uuid4().hex
        temporary = config.temp_root / f"{artifact_id}.upload"
        digest = hashlib.sha256()
        size = 0
        try:
            with temporary.open("wb") as handle:
                while chunk := await file.read(1024 * 1024):
                    size += len(chunk)
                    if size > config.max_upload_bytes:
                        raise HTTPException(status_code=413, detail="CMBX file exceeds the configured upload limit")
                    digest.update(chunk)
                    handle.write(chunk)
            owner_segment = _safe_segment(identity["user"].replace("\\", "_"), "user")
            date_segment = datetime.now().strftime("%Y-%m-%d")
            destination_dir = config.asset_root / "cmbx_source" / owner_segment / date_segment
            destination_dir.mkdir(parents=True, exist_ok=True)
            destination = destination_dir / f"{artifact_id[:8]}_{_short_file_name(original_name, 'upload.cmbx')}"
            shutil.move(str(temporary), destination)
        except Exception:
            temporary.unlink(missing_ok=True)
            raise
        finally:
            await file.close()
        record = store.add_artifact(
            {
                "id": artifact_id,
                "workspace_id": workspace_id,
                "owner": identity["user"],
                "kind": "cmbx_source",
                "original_name": original_name,
                "sha256": digest.hexdigest(),
                "size_bytes": size,
                "storage_path": str(destination),
            }
        )
        return _public_artifact(record)

    @app.post("/api/artifacts/md-upload", status_code=201)
    async def upload_managed_md(
        file: UploadFile = File(...),
        kind: str = Query(...),
        workspace_id: str = Query(DEFAULT_WORKSPACE_ID),
        identity: dict[str, Any] = Depends(current_identity),
    ) -> dict[str, Any]:
        if kind not in {"method_md", "report_md"}:
            raise HTTPException(status_code=400, detail="MD kind must be method_md or report_md")
        required_permissions = (
            ("instrument_method_generation", "method_generate", "sequence_generate")
            if kind == "method_md"
            else ("report_generate", "sequence_generate")
        )
        if not has_permission(identity, *required_permissions):
            raise HTTPException(status_code=403, detail="This MD library is not authorized for the account")
        original_name = _safe_segment(file.filename or f"{kind}.md", f"{kind}.md")
        if Path(original_name).suffix.lower() not in {".md", ".markdown"}:
            raise HTTPException(status_code=400, detail="Choose a Markdown file")
        store.ensure_workspace(workspace_id, workspace_id, identity["user"])
        owner_segment = _safe_segment(identity["user"].replace("\\", "_"), "user")
        folder_name = "Method_MD" if kind == "method_md" else "Report_MD"
        folder = config.asset_root / kind / owner_segment / datetime.now().strftime("%Y-%m-%d")
        folder.mkdir(parents=True, exist_ok=True)
        destination = folder / f"{uuid.uuid4().hex[:8]}_{_short_file_name(original_name, f'{kind}.md')}"
        limit = 20 * 1024 * 1024 if kind == "method_md" else 30 * 1024 * 1024
        try:
            with destination.open("wb") as handle:
                size = 0
                while chunk := await file.read(1024 * 1024):
                    size += len(chunk)
                    if size > limit:
                        raise HTTPException(status_code=413, detail="Markdown file exceeds the upload limit")
                    handle.write(chunk)
        except Exception:
            destination.unlink(missing_ok=True)
            raise
        finally:
            await file.close()
        checked = preflight_asset("method" if kind == "method_md" else "report", destination)
        artifact = register_file_artifact(
            destination, owner=identity["user"], kind=kind,
            workspace_id=workspace_id, original_name=original_name,
        )
        preflight = method_preflight_payload(checked) if kind == "method_md" else report_preflight_payload(checked)
        return {"artifact": _public_artifact(artifact), "preflight": preflight}

    @app.post("/api/artifacts/{artifact_id}/preflight")
    def preflight_managed_md(
        artifact_id: str,
        identity: dict[str, Any] = Depends(current_identity),
    ) -> dict[str, Any]:
        artifact = store.get_artifact(artifact_id)
        if not artifact or artifact["kind"] not in {"method_md", "report_md"}:
            raise HTTPException(status_code=404, detail="Managed MD artifact not found")
        if artifact["owner"].lower() != identity["user"].lower():
            raise HTTPException(status_code=403, detail="This MD belongs to another user")
        asset_type = "method" if artifact["kind"] == "method_md" else "report"
        checked = preflight_asset(asset_type, artifact_local_path(artifact))
        preflight = method_preflight_payload(checked) if asset_type == "method" else report_preflight_payload(checked)
        return {"artifact": _public_artifact(artifact), "preflight": preflight}

    @app.delete("/api/artifacts/{artifact_id}")
    def delete_managed_artifact(
        artifact_id: str,
        identity: dict[str, Any] = Depends(current_identity),
    ) -> dict[str, bool]:
        artifact = store.get_artifact(artifact_id)
        if not artifact or artifact["kind"] not in {"cmbx_source", "method_md", "report_md"}:
            raise HTTPException(status_code=404, detail="Managed file not found")
        if artifact["owner"].lower() != identity["user"].lower() and identity["role"] != "admin":
            raise HTTPException(status_code=403, detail="This file belongs to another user")
        path = artifact_local_path(artifact)
        allowed_roots = [config.shared_root.resolve(), config.state_root.resolve(), config.asset_root.resolve()]
        resolved = path.resolve()
        if not any(resolved == root or root in resolved.parents for root in allowed_roots):
            raise HTTPException(status_code=409, detail="Managed path is outside the controlled storage roots")
        path.unlink(missing_ok=True)
        store.delete_artifact(artifact_id)
        return {"deleted": True}

    @app.post("/api/cmbx/{artifact_id}/scan", status_code=202)
    def scan_cmbx(
        artifact_id: str,
        identity: dict[str, str] = Depends(current_identity),
    ) -> dict[str, Any]:
        artifact = store.get_artifact(artifact_id)
        if not artifact or artifact["kind"] != "cmbx_source":
            raise HTTPException(status_code=404, detail="CMBX artifact not found")
        if artifact["owner"].lower() != identity["user"].lower():
            raise HTTPException(status_code=403, detail="This CMBX belongs to another user")
        source_path = artifact_local_path(artifact)
        inventory_path = config.inventory_root / f"{artifact['sha256']}.json"

        def run(progress):
            if inventory_path.exists():
                progress(1, 1, "validating", "Using cached inventory")
                payload = read_inventory(inventory_path)
            else:
                payload = build_inventory(source_path, inventory_path, progress)
            return {
                "artifact_id": artifact_id,
                "inventory_url": f"/api/cmbx/{artifact_id}/inventory",
                "summary": payload["summary"],
            }

        return jobs.submit(
            workspace_id=artifact["workspace_id"],
            owner=identity["user"],
            task_type="cmbx_inventory",
            input_payload={"artifact_id": artifact_id, "sha256": artifact["sha256"]},
            function=run,
        )

    @app.get("/api/cmbx/{artifact_id}/inventory")
    def get_inventory(
        artifact_id: str,
        identity: dict[str, str] = Depends(current_identity),
    ) -> dict[str, Any]:
        artifact = store.get_artifact(artifact_id)
        if not artifact:
            raise HTTPException(status_code=404, detail="CMBX artifact not found")
        if artifact["owner"].lower() != identity["user"].lower():
            raise HTTPException(status_code=403, detail="This CMBX belongs to another user")
        inventory_path = config.inventory_root / f"{artifact['sha256']}.json"
        if not inventory_path.exists():
            raise HTTPException(status_code=409, detail="Inventory is not ready; scan the CMBX first")
        return read_inventory(inventory_path)

    def artifact_records(artifact_ids: list[str], identity: dict[str, Any]) -> list[dict[str, Any]]:
        records = []
        for artifact_id in dict.fromkeys(artifact_ids):
            artifact = store.get_artifact(artifact_id)
            if not artifact or artifact["kind"] != "cmbx_source":
                raise HTTPException(status_code=404, detail=f"CMBX artifact not found: {artifact_id}")
            if artifact["owner"].lower() != identity["user"].lower():
                raise HTTPException(status_code=403, detail="This CMBX belongs to another user")
            records.append(artifact)
        if not records:
            raise HTTPException(status_code=400, detail="Choose at least one CMBX source")
        return records

    def owned_method_md_records(payload: dict[str, Any], identity: dict[str, Any]) -> list[dict[str, Any]]:
        requested = [str(value) for value in payload.get("method_md_artifact_ids", []) if str(value)]
        legacy = str(payload.get("method_md_artifact_id") or "")
        if legacy and legacy not in requested:
            requested.append(legacy)
        records: list[dict[str, Any]] = []
        for artifact_id in dict.fromkeys(requested):
            artifact = store.get_artifact(artifact_id)
            if not artifact or artifact["kind"] != "method_md":
                raise HTTPException(status_code=404, detail=f"Method MD basis was not found: {artifact_id}")
            if artifact["owner"].lower() != identity["user"].lower():
                raise HTTPException(status_code=403, detail="A selected Method MD belongs to another user")
            records.append(artifact)
        if not records:
            raise HTTPException(status_code=400, detail="Choose at least one Method MD basis")
        return records

    def register_file_artifact(
        path: Path,
        *,
        owner: str,
        kind: str,
        workspace_id: str = DEFAULT_WORKSPACE_ID,
        original_name: str | None = None,
    ) -> dict[str, Any]:
        if not path.is_file():
            raise FileNotFoundError(f"Generated asset is missing: {path}")
        artifact_id = uuid.uuid4().hex
        asset_root = config.asset_root.resolve()
        source = path.resolve()
        if source == asset_root or asset_root in source.parents:
            stored_path = source
        else:
            owner_segment = _safe_segment(owner.replace("\\", "_"), "user")[:32]
            suffix = path.suffix.lower() or ".bin"
            stored_dir = config.asset_root / kind / owner_segment
            stored_dir.mkdir(parents=True, exist_ok=True)
            stored_path = stored_dir / f"{artifact_id}{suffix}"
            temporary = stored_path.with_suffix(stored_path.suffix + ".part")
            shutil.copy2(path, temporary)
            temporary.replace(stored_path)
        digest = hashlib.sha256()
        with stored_path.open("rb") as handle:
            while chunk := handle.read(1024 * 1024):
                digest.update(chunk)
        record = store.add_artifact(
            {
                "id": artifact_id,
                "workspace_id": workspace_id,
                "owner": owner,
                "kind": kind,
                "original_name": original_name or path.name,
                "sha256": digest.hexdigest(),
                "size_bytes": stored_path.stat().st_size,
                "storage_path": str(stored_path),
            }
        )
        return record

    def artifact_local_path(artifact: dict[str, Any]) -> Path:
        """Return a short managed copy, including for records created before local storage."""
        source = Path(str(artifact["storage_path"]))
        asset_root = config.asset_root.resolve()
        if source.is_file():
            resolved_source = source.resolve()
            if resolved_source == asset_root or asset_root in resolved_source.parents:
                return resolved_source
        owner_segment = _safe_segment(str(artifact["owner"]).replace("\\", "_"), "user")[:32]
        original = Path(str(artifact.get("original_name") or source.name))
        suffix = original.suffix.lower() or source.suffix or ".bin"
        short_stem = _safe_segment(original.stem, "asset")[:48]
        destination = config.asset_root / str(artifact["kind"]) / owner_segment / f"{str(artifact['id'])[:8]}_{short_stem}{suffix}"
        if destination.is_file() and destination.stat().st_size == int(artifact.get("size_bytes") or 0):
            return destination
        if not source.is_file():
            if destination.is_file():
                return destination
            raise FileNotFoundError(
                f"Managed asset is unavailable: {artifact.get('original_name') or artifact['id']}"
            )
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.resolve() == destination.resolve():
            return destination
        temporary = destination.with_suffix(destination.suffix + f".{uuid.uuid4().hex[:8]}.part")
        shutil.copy2(source, temporary)
        temporary.replace(destination)
        return destination

    def new_local_work_root(prefix: str) -> Path:
        return config.work_root / f"{_safe_segment(prefix, 'job')[:12]}_{uuid.uuid4().hex[:12]}"

    def artifact_paths(records: list[dict[str, Any]]) -> list[str]:
        return [str(artifact_local_path(item)) for item in records]

    def method_preflight_payload(result) -> dict[str, Any]:
        issues = [
            {
                "severity": str(getattr(item, "severity", "warning")),
                "code": str(getattr(item, "code", "METHOD")),
                "row": str(getattr(item, "row", "-")),
                "message": str(getattr(item, "message", item)),
            }
            for item in result.method_issues
        ]
        return {
            "ready": result.ready,
            "source_sha256": result.source_sha256,
            "rows": result.method_rows,
            "issues": issues,
            "errors": result.errors,
            "warnings": result.warnings,
            "configuration": configuration_requirements(result.method_rows) if result.method_rows else [],
        }

    def report_preflight_payload(result) -> dict[str, Any]:
        spec = result.report_spec
        return {
            "ready": result.ready,
            "source_sha256": result.source_sha256,
            "errors": result.errors,
            "warnings": result.warnings,
            "summary": {
                "title": str(getattr(spec, "template_name", "")),
                "sheets": len(getattr(spec, "sheets", []) or []),
                "cm_formulas": len(getattr(spec, "patches", []) or []),
                "workbook_cells": len(getattr(spec, "workbook_patches", []) or []),
                "dynamic_tables": len(getattr(spec, "dynamic_tables", []) or []),
            } if spec else {},
        }

    @app.get("/api/method/config")
    def method_config(identity: dict[str, str] = Depends(current_identity)) -> dict[str, Any]:
        modules: set[str] = set()
        for context in ("02_Full_Context", "03_Small_Context"):
            root = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "CMBX Data Explorer Workspace" / "KB" / "KB_Online_GPT" / context
            if root.is_dir():
                modules.update(
                    item.name for item in root.iterdir()
                    if item.is_dir() and item.name.lower() != "report" and (item / "Method").is_dir()
                )
        return {
            "modules": sorted(modules),
            "target_versions": ["7.2 compatible", "7.3"],
            "workflow": ["Prepare web AI", "Import and preview", "Generate CMBX"],
            "providers": public_provider_defaults(),
            "allowed_routes": {
                "manual": has_permission(identity, "method_manual_web_ai"),
                "gpt": has_permission(identity, "method_generate"),
                "deepseek": has_permission(identity, "method_deepseek"),
            },
            "quota": store.method_usage_summary(
                identity["user_id"], datetime.now().date().isoformat(), identity_limit(identity)
            ),
        }

    def effective_ai_setting(user_id: str, provider: str) -> dict[str, Any]:
        provider = provider.lower()
        defaults = PROVIDER_DEFAULTS.get(provider)
        if not defaults:
            raise HTTPException(status_code=400, detail="Unsupported AI provider")
        personal = store.get_ai_setting(user_id, provider) or {}
        owner_id = config.desktop_ai_owner.strip().lower()
        workspace = store.get_ai_setting(owner_id, provider) or {} if owner_id else {}
        if str(personal.get("encrypted_api_key") or "").strip():
            saved = personal
            credential_source = "personal"
        elif str(workspace.get("encrypted_api_key") or "").strip():
            saved = workspace
            credential_source = "workspace"
        else:
            saved = personal
            credential_source = "none"
        return {**saved, "credential_source": credential_source}

    def public_ai_setting(user_id: str, provider: str) -> dict[str, Any]:
        provider = provider.lower()
        defaults = PROVIDER_DEFAULTS.get(provider)
        if not defaults:
            raise HTTPException(status_code=400, detail="Unsupported AI provider")
        saved = effective_ai_setting(user_id, provider)
        return {
            "provider": provider,
            "label": defaults["label"],
            "base_url": saved.get("base_url") or defaults["base_url"],
            "model": saved.get("model") or defaults["model"],
            "api_key_configured": bool(saved.get("encrypted_api_key")),
            "credential_source": saved.get("credential_source", "none"),
        }

    @app.get("/api/account/ai-settings")
    def account_ai_settings(identity: dict[str, str] = Depends(current_identity)) -> dict[str, Any]:
        return {
            "providers": [public_ai_setting(identity["user_id"], provider) for provider in PROVIDER_DEFAULTS],
            "quota": store.method_usage_summary(
                identity["user_id"], datetime.now().date().isoformat(), identity_limit(identity)
            ),
        }

    @app.put("/api/account/ai-settings/{provider}")
    def save_account_ai_settings(
        provider: str,
        payload: dict[str, Any] = Body(...),
        identity: dict[str, str] = Depends(current_identity),
    ) -> dict[str, Any]:
        provider = provider.lower()
        defaults = PROVIDER_DEFAULTS.get(provider)
        if not defaults:
            raise HTTPException(status_code=400, detail="Unsupported AI provider")
        base_url = str(payload.get("base_url") or defaults["base_url"]).strip().rstrip("/")
        model = str(payload.get("model") or defaults["model"]).strip()
        if not base_url.startswith(("https://", "http://")) or not model:
            raise HTTPException(status_code=400, detail="A valid API base URL and model are required")
        encrypted_key: str | None = None
        if bool(payload.get("clear_api_key")):
            encrypted_key = ""
        elif str(payload.get("api_key") or "").strip():
            encrypted_key = protect_secret(str(payload["api_key"]).strip())
        store.save_ai_setting(identity["user_id"], provider, base_url, model, encrypted_key)
        return public_ai_setting(identity["user_id"], provider)

    @app.get("/api/account/method-quota")
    def account_method_quota(identity: dict[str, str] = Depends(current_identity)) -> dict[str, Any]:
        return store.method_usage_summary(
            identity["user_id"], datetime.now().date().isoformat(), identity_limit(identity)
        )

    @app.post("/api/account/access-requests", status_code=201)
    def request_method_access(
        payload: dict[str, Any] = Body(...),
        identity: dict[str, str] = Depends(current_identity),
    ) -> dict[str, Any]:
        day = datetime.now().date().isoformat()
        summary = store.method_usage_summary(identity["user_id"], day, identity_limit(identity))
        if summary["pending_requests"]:
            raise HTTPException(status_code=409, detail="A quota request is already pending for today")
        return store.create_access_request(
            {
                "id": uuid.uuid4().hex,
                "user_id": identity["user_id"],
                "quota_day": day,
                "requested_uses": min(20, max(1, int(payload.get("requested_uses") or 1))),
                "reason": str(payload.get("reason") or "").strip()[:1000],
            }
        )

    @app.post("/api/method/ai-package", status_code=201)
    def create_method_ai_package(
        payload: dict[str, Any] = Body(...),
        identity: dict[str, Any] = Depends(require_method_manual),
    ) -> dict[str, Any]:
        modules = tuple(dict.fromkeys(str(value).strip() for value in payload.get("modules", []) if str(value).strip()))
        if not modules:
            raise HTTPException(status_code=400, detail="Choose at least one module")
        small_context = bool(payload.get("small_context"))
        files = recommended_online_kb_files_for_modules("method", modules, small_context=small_context)
        if not files:
            raise HTTPException(status_code=400, detail="No Method SPEC/KB files were found for the selected modules")
        request_text = str(payload.get("request") or "")
        if bool(payload.get("optimize")):
            prompt = optimize_prompt("method", modules, request_text)
        else:
            prompt = PromptOptimization(base_prompt("method", modules, request_text), False, "Prompt packaged without API optimization.")
        date_segment = datetime.now().strftime("%Y-%m-%d")
        owner_segment = _safe_segment(identity["user"].replace("\\", "_"), "user")
        destination_dir = config.asset_root / "method_ai_package" / owner_segment / date_segment
        destination = destination_dir / f"{uuid.uuid4().hex[:8]}_Instrument_Method_AI_Package.zip"
        try:
            create_web_ai_zip(
                destination,
                asset_type="method",
                modules=modules,
                files=files,
                prompt=prompt,
                small_context=small_context,
            )
        except (FileNotFoundError, ValueError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        artifact = register_file_artifact(destination, owner=identity["user"], kind="method_ai_package")
        return {
            "artifact": _public_artifact(artifact),
            "download_url": f"/api/artifacts/{artifact['id']}/download",
            "files": [path.name for path in files],
            "prompt": prompt.prompt,
            "prompt_detail": prompt.detail,
            "used_ai": prompt.used_ai,
        }

    @app.post("/api/method/preflight", status_code=201)
    async def preflight_method_md(
        file: UploadFile = File(...),
        workspace_id: str = Query(DEFAULT_WORKSPACE_ID),
        identity: dict[str, Any] = Depends(require_method_manual),
    ) -> dict[str, Any]:
        original_name = _safe_segment(file.filename or "method.md", "method.md")
        if Path(original_name).suffix.lower() not in {".md", ".markdown"}:
            raise HTTPException(status_code=400, detail="Choose a Markdown method file")
        store.ensure_workspace(workspace_id, workspace_id, identity["user"])
        owner_segment = _safe_segment(identity["user"].replace("\\", "_"), "user")
        date_segment = datetime.now().strftime("%Y-%m-%d")
        destination_dir = config.asset_root / "method_md" / owner_segment / date_segment
        destination_dir.mkdir(parents=True, exist_ok=True)
        destination = destination_dir / f"{uuid.uuid4().hex[:8]}_{_short_file_name(original_name, 'method.md')}"
        size = 0
        try:
            with destination.open("wb") as handle:
                while chunk := await file.read(1024 * 1024):
                    size += len(chunk)
                    if size > 20 * 1024 * 1024:
                        raise HTTPException(status_code=413, detail="Method MD exceeds the 20 MB limit")
                    handle.write(chunk)
        except Exception:
            destination.unlink(missing_ok=True)
            raise
        finally:
            await file.close()
        result = preflight_asset("method", destination)
        artifact = register_file_artifact(
            destination,
            owner=identity["user"],
            kind="method_md",
            workspace_id=workspace_id,
            original_name=original_name,
        )
        return {"artifact": _public_artifact(artifact), "preflight": method_preflight_payload(result)}

    @app.post("/api/method/auto-generate", status_code=202)
    def auto_generate_method(
        payload: dict[str, Any] = Body(...),
        identity: dict[str, Any] = Depends(require_method_generator),
    ) -> dict[str, Any]:
        provider = str(payload.get("provider") or "").lower()
        if provider not in PROVIDER_DEFAULTS:
            raise HTTPException(status_code=400, detail="Choose GPT or DeepSeek for automatic generation")
        if provider == "gpt" and not has_permission(identity, "method_generate"):
            raise HTTPException(status_code=403, detail="GPT automatic generation permission is required")
        if provider == "deepseek" and not has_permission(identity, "method_deepseek"):
            raise HTTPException(status_code=403, detail="DeepSeek automatic generation is restricted by the administrator")
        modules = tuple(dict.fromkeys(str(value).strip() for value in payload.get("modules", []) if str(value).strip()))
        if not modules:
            raise HTTPException(status_code=400, detail="Choose at least one module")
        requirement = str(payload.get("request") or "").strip()
        if not requirement:
            raise HTTPException(status_code=400, detail="Enter the test requirement for automatic generation")
        saved = effective_ai_setting(identity["user_id"], provider)
        defaults = PROVIDER_DEFAULTS[provider]
        api_key = unprotect_secret(str(saved.get("encrypted_api_key") or ""))
        if not api_key:
            raise HTTPException(status_code=409, detail=f"Configure your {defaults['label']} API key first")
        settings = AIProviderSettings(
            provider=provider,
            base_url=str(saved.get("base_url") or defaults["base_url"]),
            model=str(saved.get("model") or defaults["model"]),
            api_key=api_key,
        )
        kb_files = recommended_online_kb_files_for_modules(
            "method", modules, small_context=bool(payload.get("small_context"))
        )
        if not kb_files:
            raise HTTPException(status_code=400, detail="No Method SPEC/KB files were found for the selected modules")
        usage_day = datetime.now().date().isoformat()
        usage_id = uuid.uuid4().hex
        try:
            store.claim_method_api_usage(
                usage_id, identity["user_id"], usage_day, provider, identity_limit(identity)
            )
        except PermissionError as exc:
            raise HTTPException(status_code=429, detail=str(exc)) from exc

        asset_name = _safe_segment(str(payload.get("asset_name") or "AI_Instrument_Method"), "AI_Instrument_Method")
        target_version = str(payload.get("target_cm_version") or "7.2 compatible")
        md_only = bool(payload.get("md_only"))
        owner_segment = _safe_segment(identity["user"].replace("\\", "_"), "user")
        date_segment = datetime.now().strftime("%Y-%m-%d")
        method_dir = config.asset_root / "method_md" / owner_segment / date_segment
        output_root = new_local_work_root("method_ai")

        def run(progress):
            progress(1, 6, "preparing", f"Loading {len(kb_files)} Method SPEC/KB file(s)")
            generated_md = generate_method_markdown(requirement, modules, kb_files, settings)
            progress(2, 6, "running", f"{defaults['label']} returned Method Markdown")
            method_dir.mkdir(parents=True, exist_ok=True)
            source_path = method_dir / f"{uuid.uuid4().hex[:8]}_AI_method.md"
            source_path.write_text(generated_md, encoding="utf-8")
            md_artifact = register_file_artifact(
                source_path,
                owner=identity["user"],
                kind="method_md",
                original_name=f"{asset_name}.md",
            )
            progress(3, 6, "validating", "Running Method MD structural preflight")
            checked = preflight_asset("method", source_path)
            preflight_payload = method_preflight_payload(checked)
            if not checked.ready or md_only:
                progress(6, 6, "validating", "AI Method MD is ready for review")
                return {
                    "cmbx_generated": False,
                    "method_md_artifact": _public_artifact(md_artifact),
                    "method_md_download_url": f"/api/artifacts/{md_artifact['id']}/download",
                    "preflight": preflight_payload,
                    "provider": provider,
                    "model": settings.model,
                    "md_only": md_only,
                }
            progress(4, 6, "running", "Compiling standalone instrument method CMBX")
            generated = generate_asset(
                AssetGenerationRequest(
                    asset_type="method",
                    asset_name=asset_name,
                    family=" + ".join(modules),
                    intent=requirement,
                    target_cm_version=target_version,
                    source_md=source_path,
                    output_root=output_root,
                ),
                checked,
            )
            progress(5, 6, "validating", "Registering generated CMBX")
            output_artifact = register_file_artifact(
                generated.output_cmbx,
                owner=identity["user"],
                kind="generated_method_cmbx",
                original_name=f"{asset_name}_method.cmbx",
            )
            progress(6, 6, "validating", "AI Method MD and candidate CMBX are ready")
            return {
                "cmbx_generated": True,
                "method_md_artifact": _public_artifact(md_artifact),
                "method_md_download_url": f"/api/artifacts/{md_artifact['id']}/download",
                "artifact": _public_artifact(output_artifact),
                "download_url": f"/api/artifacts/{output_artifact['id']}/download",
                "preflight": preflight_payload,
                "provider": provider,
                "model": settings.model,
                "md_only": False,
            }

        job = jobs.submit(
            workspace_id=DEFAULT_WORKSPACE_ID,
            owner=identity["user"],
            task_type="instrument_method_ai_generation",
            input_payload={
                "provider": provider,
                "model": settings.model,
                "modules": modules,
                "asset_name": asset_name,
                "usage_id": usage_id,
                "md_only": md_only,
            },
            function=run,
        )
        store.attach_usage_job(usage_id, job["id"])
        return {**job, "quota": store.method_usage_summary(
            identity["user_id"], usage_day, identity_limit(identity)
        )}

    @app.post("/api/method/generate", status_code=202)
    def generate_method_cmbx(
        payload: dict[str, Any] = Body(...),
        identity: dict[str, Any] = Depends(require_method_generator),
    ) -> dict[str, Any]:
        artifact = store.get_artifact(str(payload.get("artifact_id") or ""))
        if not artifact or artifact["kind"] != "method_md":
            raise HTTPException(status_code=404, detail="Method MD artifact not found")
        if artifact["owner"].lower() != identity["user"].lower() and identity["role"] != "admin":
            raise HTTPException(status_code=403, detail="This Method MD belongs to another user")
        asset_name = _safe_segment(str(payload.get("asset_name") or Path(artifact["original_name"]).stem), "Instrument_Method")
        target_version = str(payload.get("target_cm_version") or "7.2 compatible")
        source_path = artifact_local_path(artifact)
        owner_segment = _safe_segment(identity["user"].replace("\\", "_"), "user")
        date_segment = datetime.now().strftime("%Y-%m-%d")
        output_root = new_local_work_root("method")

        def run(progress):
            progress(1, 4, "preparing", "Rechecking Method MD")
            checked = preflight_asset("method", source_path)
            if not checked.ready:
                raise ValueError("Method MD no longer passes preflight")
            progress(2, 4, "running", "Compiling standalone instrument method")
            generated = generate_asset(
                AssetGenerationRequest(
                    asset_type="method",
                    asset_name=asset_name,
                    family=str(payload.get("family") or ""),
                    intent=str(payload.get("intent") or ""),
                    target_cm_version=target_version,
                    source_md=source_path,
                    output_root=output_root,
                ),
                checked,
            )
            progress(3, 4, "validating", "Registering generated CMBX")
            output_artifact = register_file_artifact(
                generated.output_cmbx,
                owner=identity["user"],
                kind="generated_method_cmbx",
                workspace_id=artifact["workspace_id"],
                original_name=f"{asset_name}_method.cmbx",
            )
            progress(4, 4, "validating", "Instrument method CMBX is registered")
            return {
                "artifact": _public_artifact(output_artifact),
                "download_url": f"/api/artifacts/{output_artifact['id']}/download",
                "manifest_name": generated.manifest.name,
                "project_name": asset_name,
            }

        return jobs.submit(
            workspace_id=artifact["workspace_id"],
            owner=identity["user"],
            task_type="instrument_method_generation",
            input_payload={"method_md_artifact_id": artifact["id"], "asset_name": asset_name, "target_cm_version": target_version},
            function=run,
        )

    @app.get("/api/report/config")
    def report_config(identity: dict[str, Any] = Depends(require_report_generator)) -> dict[str, Any]:
        modules: set[str] = set()
        root = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "CMBX Data Explorer Workspace" / "KB" / "KB_Online_GPT" / "02_Full_Context" / "Report"
        if root.is_dir():
            modules.update(item.name for item in root.iterdir() if item.is_dir())
        return {
            "modules": sorted(modules),
            "target_versions": ["7.2 compatible", "7.3"],
            "manual_web_ai": has_permission(identity, "report_manual_web_ai"),
            "quota": store.method_usage_summary(
                identity["user_id"], datetime.now().date().isoformat(), identity_limit(identity)
            ),
        }

    @app.post("/api/report/ai-package", status_code=201)
    def create_report_ai_package(
        payload: dict[str, Any] = Body(...),
        identity: dict[str, Any] = Depends(require_report_manual),
    ) -> dict[str, Any]:
        modules = tuple(dict.fromkeys(str(value).strip() for value in payload.get("modules", []) if str(value).strip()))
        if not modules:
            raise HTTPException(status_code=400, detail="Choose at least one module")
        files = recommended_online_kb_files_for_modules("report", modules, small_context=bool(payload.get("small_context")))
        if not files:
            raise HTTPException(status_code=400, detail="No Report SPEC/KB files were found for the selected modules")
        method_bases = owned_method_md_records(payload, identity)
        files = [*files, *(artifact_local_path(item) for item in method_bases)]
        request_text = str(payload.get("request") or "")
        prompt = optimize_prompt("report", modules, request_text) if bool(payload.get("optimize")) else PromptOptimization(
            base_prompt("report", modules, request_text), False, "Prompt packaged without API optimization."
        )
        owner_segment = _safe_segment(identity["user"].replace("\\", "_"), "user")
        destination = config.asset_root / "report_ai_package" / owner_segment / f"{uuid.uuid4().hex[:8]}_Report_AI_Package.zip"
        create_web_ai_zip(destination, asset_type="report", modules=modules, files=files, prompt=prompt, small_context=bool(payload.get("small_context")))
        artifact = register_file_artifact(destination, owner=identity["user"], kind="report_ai_package")
        return {
            "artifact": _public_artifact(artifact),
            "download_url": f"/api/artifacts/{artifact['id']}/download",
            "files": [path.name for path in files],
            "prompt": prompt.prompt,
            "method_bases": [_public_artifact(item) for item in method_bases],
        }

    @app.post("/api/report/preflight", status_code=201)
    async def preflight_report_md(
        file: UploadFile = File(...),
        workspace_id: str = Query(DEFAULT_WORKSPACE_ID),
        identity: dict[str, Any] = Depends(require_report_manual),
    ) -> dict[str, Any]:
        original_name = _safe_segment(file.filename or "report.md", "report.md")
        if Path(original_name).suffix.lower() not in {".md", ".markdown"}:
            raise HTTPException(status_code=400, detail="Choose a Markdown report file")
        owner_segment = _safe_segment(identity["user"].replace("\\", "_"), "user")
        folder = config.asset_root / "report_md" / owner_segment / datetime.now().strftime("%Y-%m-%d")
        folder.mkdir(parents=True, exist_ok=True)
        destination = folder / f"{uuid.uuid4().hex[:8]}_{_short_file_name(original_name, 'report.md')}"
        try:
            with destination.open("wb") as handle:
                size = 0
                while chunk := await file.read(1024 * 1024):
                    size += len(chunk)
                    if size > 30 * 1024 * 1024:
                        raise HTTPException(status_code=413, detail="Report MD exceeds the 30 MB limit")
                    handle.write(chunk)
        except Exception:
            destination.unlink(missing_ok=True)
            raise
        finally:
            await file.close()
        checked = preflight_asset("report", destination)
        artifact = register_file_artifact(destination, owner=identity["user"], kind="report_md", workspace_id=workspace_id, original_name=original_name)
        return {"artifact": _public_artifact(artifact), "preflight": report_preflight_payload(checked)}

    @app.post("/api/report/auto-generate", status_code=202)
    def auto_generate_report(
        payload: dict[str, Any] = Body(...),
        identity: dict[str, Any] = Depends(require_report_generator),
    ) -> dict[str, Any]:
        method_artifacts = owned_method_md_records(payload, identity)
        modules = tuple(dict.fromkeys(
            str(value).strip() for value in payload.get("modules", []) if str(value).strip()
        ))
        if not modules:
            raise HTTPException(status_code=400, detail="Choose at least one related module")
        requirement = str(payload.get("request") or "").strip()
        if not requirement:
            raise HTTPException(status_code=400, detail="Enter the report requirement")
        provider = "gpt"
        saved = effective_ai_setting(identity["user_id"], provider)
        defaults = PROVIDER_DEFAULTS[provider]
        api_key = unprotect_secret(str(saved.get("encrypted_api_key") or ""))
        if not api_key:
            raise HTTPException(status_code=409, detail="Configure your GPT API key first")
        settings = AIProviderSettings(
            provider=provider,
            base_url=str(saved.get("base_url") or defaults["base_url"]),
            model=str(saved.get("model") or defaults["model"]),
            api_key=api_key,
        )
        kb_files = recommended_online_kb_files_for_modules(
            "report", modules, small_context=bool(payload.get("small_context"))
        )
        if not kb_files:
            raise HTTPException(status_code=400, detail="No Report SPEC/KB files were found for the selected modules")
        usage_day = datetime.now().date().isoformat()
        usage_id = uuid.uuid4().hex
        try:
            store.claim_method_api_usage(
                usage_id, identity["user_id"], usage_day, provider, identity_limit(identity)
            )
        except PermissionError as exc:
            raise HTTPException(status_code=429, detail=str(exc)) from exc
        owner_segment = _safe_segment(identity["user"].replace("\\", "_"), "user")
        report_dir = config.asset_root / "report_md" / owner_segment / datetime.now().strftime("%Y-%m-%d")
        asset_name = _safe_segment(str(payload.get("asset_name") or "AI_Report_Template"), "AI_Report_Template")

        def run(progress):
            progress(1, 4, "preparing", "Loading Method MD and Report SPEC/KB")
            method_markdowns = [
                (
                    str(item["original_name"]),
                    artifact_local_path(item).read_text(encoding="utf-8", errors="replace"),
                )
                for item in method_artifacts
            ]
            generated_md = generate_report_markdown(requirement, modules, kb_files, method_markdowns, settings)
            progress(2, 4, "running", "GPT returned Report Markdown")
            report_dir.mkdir(parents=True, exist_ok=True)
            source_path = report_dir / f"{uuid.uuid4().hex[:8]}_AI_report.md"
            source_path.write_text(generated_md, encoding="utf-8")
            artifact = register_file_artifact(
                source_path, owner=identity["user"], kind="report_md", original_name=f"{asset_name}.md"
            )
            progress(3, 4, "validating", "Running Report MD structural preflight")
            checked = preflight_asset("report", source_path)
            progress(4, 4, "validating", "Report MD is ready for review")
            return {
                "report_md_artifact": _public_artifact(artifact),
                "report_md_download_url": f"/api/artifacts/{artifact['id']}/download",
                "preflight": report_preflight_payload(checked),
                "provider": provider,
                "model": settings.model,
            }

        job = jobs.submit(
            workspace_id=DEFAULT_WORKSPACE_ID,
            owner=identity["user"],
            task_type="report_template_ai_generation",
            input_payload={
                "modules": modules,
                "method_md_artifact_ids": [item["id"] for item in method_artifacts],
                "usage_id": usage_id,
            },
            function=run,
        )
        store.attach_usage_job(usage_id, job["id"])
        return job

    @app.post("/api/report/generate", status_code=202)
    def generate_report_cmbx(
        payload: dict[str, Any] = Body(...),
        identity: dict[str, Any] = Depends(require_report_generator),
    ) -> dict[str, Any]:
        artifact = store.get_artifact(str(payload.get("artifact_id") or ""))
        if not artifact or artifact["kind"] != "report_md":
            raise HTTPException(status_code=404, detail="Report MD artifact not found")
        if artifact["owner"].lower() != identity["user"].lower() and identity["role"] != "admin":
            raise HTTPException(status_code=403, detail="This Report MD belongs to another user")
        source_path = artifact_local_path(artifact)
        asset_name = _safe_segment(str(payload.get("asset_name") or Path(artifact["original_name"]).stem), "Report_Template")
        owner_segment = _safe_segment(identity["user"].replace("\\", "_"), "user")
        output_root = new_local_work_root("report")

        def run(progress):
            progress(1, 4, "preparing", "Rechecking Report MD")
            checked = preflight_asset("report", source_path)
            if not checked.ready:
                raise ValueError("Report MD no longer passes preflight: " + "; ".join(checked.errors))
            progress(2, 4, "running", "Compiling standalone report template")
            generated = generate_asset(AssetGenerationRequest(
                asset_type="report", asset_name=asset_name, family=str(payload.get("family") or ""),
                intent=str(payload.get("intent") or ""), target_cm_version=str(payload.get("target_cm_version") or "7.2 compatible"),
                source_md=source_path, output_root=output_root,
            ), checked)
            progress(3, 4, "validating", "Registering generated report CMBX")
            output_artifact = register_file_artifact(generated.output_cmbx, owner=identity["user"], kind="generated_report_cmbx", original_name=f"{asset_name}_report.cmbx")
            progress(4, 4, "validating", "Report template CMBX is registered")
            return {"artifact": _public_artifact(output_artifact), "download_url": f"/api/artifacts/{output_artifact['id']}/download", "manifest_name": generated.manifest.name}

        return jobs.submit(workspace_id=artifact["workspace_id"], owner=identity["user"], task_type="report_template_generation", input_payload={"report_md_artifact_id": artifact["id"], "asset_name": asset_name}, function=run)

    def sequence_method_name(artifact: dict[str, Any]) -> str:
        return _safe_segment(Path(str(artifact.get("original_name") or "Method")).stem, "Generated Method")[:80]

    def sequence_report_name(artifact: dict[str, Any], checked: Any | None = None) -> str:
        result = checked or preflight_asset("report", artifact_local_path(artifact))
        spec = getattr(result, "report_spec", None)
        return _safe_segment(
            str(getattr(spec, "template_name", "") or Path(str(artifact.get("original_name") or "Report")).stem),
            "Generated Report",
        )[:80]

    @app.get("/api/sequence/config")
    def sequence_config(identity: dict[str, Any] = Depends(require_sequence_generator)) -> dict[str, Any]:
        methods = [
            {**_public_artifact(item), "asset_name": sequence_method_name(item)} for item in store.list_artifacts(DEFAULT_WORKSPACE_ID)
            if item["owner"].lower() == identity["user"].lower() and item["kind"] == "method_md"
        ]
        reports = [
            {**_public_artifact(item), "asset_name": sequence_report_name(item)} for item in store.list_artifacts(DEFAULT_WORKSPACE_ID)
            if item["owner"].lower() == identity["user"].lower() and item["kind"] == "report_md"
        ]
        carrier = Path(__file__).resolve().parents[1] / "assets" / "sequence_carrier_native_test2.cmbx"
        return {
            "method_md": methods,
            "report_md": reports,
            "max_injections": 10,
            "method_slots": 10,
            "processing_method_optional": True,
            "processing_method_default": "",
            "carrier_available": carrier.exists(),
            "carrier_family": "TCC",
            "target_versions": ["7.3 candidate"],
        }

    @app.post("/api/sequence/preflight")
    def sequence_preflight(
        payload: dict[str, Any] = Body(...),
        identity: dict[str, Any] = Depends(require_sequence_generator),
    ) -> dict[str, Any]:
        rows = list(payload.get("injections") or [])
        if not rows:
            raise HTTPException(status_code=400, detail="Add at least one Injection")
        if len(rows) > 10:
            raise HTTPException(status_code=400, detail="The controlled TCC carrier supports at most 10 Injections")
        target_version = str(payload.get("target_cm_version") or "7.3 candidate")
        if target_version != "7.3 candidate":
            raise HTTPException(status_code=400, detail=f"No controlled sequence carrier is available for {target_version}")
        carrier_errors: list[str] = []
        method_records: list[dict[str, Any]] = []
        checks: list[dict[str, Any]] = []
        for index, row in enumerate(rows, 1):
            artifact = store.get_artifact(str(row.get("method_md_artifact_id") or ""))
            if not artifact or artifact["kind"] != "method_md":
                raise HTTPException(status_code=404, detail=f"Injection {index}: Method MD not found")
            if artifact["owner"].lower() != identity["user"].lower():
                raise HTTPException(status_code=403, detail="A selected Method MD belongs to another user")
            checked = preflight_asset("method", artifact_local_path(artifact))
            method_records.append(artifact)
            checks.append({
                "injection": str(row.get("injection_name") or f"Injection {index}"),
                "method": sequence_method_name(artifact),
                "ready": checked.ready,
                "errors": list(checked.errors),
                "warnings": list(checked.warnings),
            })
        report = store.get_artifact(str(payload.get("report_md_artifact_id") or ""))
        if not report or report["kind"] != "report_md":
            raise HTTPException(status_code=404, detail="Choose one shared Report MD")
        if report["owner"].lower() != identity["user"].lower():
            raise HTTPException(status_code=403, detail="The selected Report MD belongs to another user")
        report_check = preflight_asset("report", artifact_local_path(report))
        resolved_report_name = sequence_report_name(report, report_check)
        ready = all(item["ready"] for item in checks) and report_check.ready and not carrier_errors
        return {
            "ready": ready,
            "methods": checks,
            "report": {
                "name": resolved_report_name,
                "ready": report_check.ready,
                "errors": list(report_check.errors),
                "warnings": list(report_check.warnings),
            },
            "processing_method": "blank",
            "carrier": {
                "ready": not carrier_errors,
                "name": "CM-native test2 carrier",
                "max_injections": 10,
                "method_slots": 10,
                "errors": carrier_errors,
            },
            "target_cm_version": target_version,
            "warnings": [
                "Processing Method is intentionally blank; IRC and integration actions are not included.",
                "The first multi-Injection writer uses a controlled TCC CM 7.3 carrier and requires Chromeleon runtime verification.",
            ],
        }

    @app.post("/api/sequence/generate", status_code=202)
    def generate_sequence_cmbx(
        payload: dict[str, Any] = Body(...),
        identity: dict[str, Any] = Depends(require_sequence_generator),
    ) -> dict[str, Any]:
        preview = sequence_preflight(payload, identity)
        if not preview["ready"]:
            raise HTTPException(status_code=400, detail="Sequence inputs do not pass preflight")
        rows = list(payload.get("injections") or [])
        report_artifact = store.get_artifact(str(payload.get("report_md_artifact_id") or ""))
        method_artifacts = [store.get_artifact(str(row.get("method_md_artifact_id") or "")) for row in rows]
        first_method_name = sequence_method_name(method_artifacts[0])
        sequence_name = _safe_segment(f"{first_method_name}_Sequence_{datetime.now():%Y%m%d_%H%M%S}", "Generated Sequence")[:80]
        report_check = preflight_asset("report", artifact_local_path(report_artifact))
        report_name = sequence_report_name(report_artifact, report_check)
        target_version = str(payload.get("target_cm_version") or "7.3 candidate")
        owner_segment = _safe_segment(identity["user"].replace("\\", "_"), "user")
        output_root = new_local_work_root("sequence")
        carrier = Path(__file__).resolve().parents[1] / "assets" / "sequence_carrier_native_test2.cmbx"

        def run(progress):
            total = len(rows) + 5
            output_root.mkdir(parents=True, exist_ok=True)
            generated_methods = []
            generated_method_names: list[str] = []
            for index, (row, artifact) in enumerate(zip(rows, method_artifacts), 1):
                progress(index, total, "running", f"Compiling Method {index}/{len(rows)}")
                source = artifact_local_path(artifact)
                checked = preflight_asset("method", source)
                method_name = sequence_method_name(artifact)
                generated_method_names.append(method_name)
                generated_methods.append(generate_asset(AssetGenerationRequest(
                    asset_type="method", asset_name=method_name, family="TCC",
                    intent=f"Sequence {sequence_name} / {row.get('injection_name') or f'Injection {index}'}",
                    target_cm_version="7.3", source_md=source, output_root=output_root / "components",
                ), checked))
            progress(len(rows) + 1, total, "running", "Compiling shared Report Template")
            report_source = artifact_local_path(report_artifact)
            generated_report = generate_asset(AssetGenerationRequest(
                asset_type="report", asset_name=report_name, family="TCC",
                intent=f"Shared report for Sequence {sequence_name}", target_cm_version="7.3",
                source_md=report_source, output_root=output_root / "components",
            ), report_check)
            progress(len(rows) + 2, total, "running", "Writing multi-Injection sequence DataContract")
            output_cmbx = output_root / f"{sequence_name}.cmbx"
            validation = build_multi_sequence_package(MultiSequencePackageRequest(
                carrier_cmbx=carrier,
                report_cmbx=generated_report.output_cmbx,
                output_cmbx=output_cmbx,
                sequence_name=sequence_name,
                report_name=report_name,
                injections=tuple(
                    SequenceInjectionRequest(
                        injection_name=str(row.get("injection_name") or f"Injection {index}"),
                        method_cmbx=generated.output_cmbx,
                        method_name=method_name,
                    )
                    for index, (row, artifact, generated, method_name) in enumerate(
                        zip(rows, method_artifacts, generated_methods, generated_method_names), 1
                    )
                ),
                include_processing_methods=False,
            ))
            progress(len(rows) + 3, total, "validating", "Reopening sequence and checking asset bindings")
            if not validation.passed:
                raise ValueError("Sequence validation failed: " + "; ".join(validation.errors))
            output_artifact = register_file_artifact(
                output_cmbx, owner=identity["user"], kind="generated_sequence_cmbx",
                original_name=f"{sequence_name}.cmbx",
            )
            progress(total, total, "validating", "Candidate Sequence CMBX is registered")
            return {
                "artifact": _public_artifact(output_artifact),
                "download_url": f"/api/artifacts/{output_artifact['id']}/download",
                "sequence_name": validation.sequence_name,
                "injections": list(validation.injection_names),
                "instrument_methods": list(validation.instrument_methods),
                "report_template": validation.report_template,
                "processing_methods": list(validation.processing_methods),
                "warnings": list(validation.warnings),
            }

        return jobs.submit(
            workspace_id=DEFAULT_WORKSPACE_ID,
            owner=identity["user"],
            task_type="sequence_generation",
            input_payload={
                "sequence_name": sequence_name,
                "method_md_artifact_ids": [item["id"] for item in method_artifacts],
                "report_md_artifact_id": report_artifact["id"],
                "target_cm_version": target_version,
            },
            function=run,
        )

    @app.post("/api/analysis/catalog")
    def analysis_catalog(payload: dict[str, Any] = Body(...), identity: dict[str, Any] = Depends(current_identity)) -> dict[str, Any]:
        records = artifact_records([str(value) for value in payload.get("artifact_ids", [])], identity)
        return build_catalog(artifact_paths(records))

    @app.post("/api/raw/export", status_code=202)
    def raw_export(payload: dict[str, Any] = Body(...), identity: dict[str, Any] = Depends(require_raw_export)) -> dict[str, Any]:
        records = artifact_records([str(value) for value in payload.get("artifact_ids", [])], identity)
        keys = [str(value) for value in payload.get("channel_keys", [])]
        owner_segment = _safe_segment(identity["user"].replace("\\", "_"), "user")
        destination = config.shared_root / "04_Analysis" / owner_segment / datetime.now().strftime("%Y-%m-%d") / f"{uuid.uuid4().hex[:8]}_raw_data.zip"

        def run(progress):
            progress(1, 3, "preparing", "Resolving selected channels")
            summary = export_raw_zip(artifact_paths(records), keys, destination)
            progress(2, 3, "validating", "Registering raw data archive")
            artifact = register_file_artifact(destination, owner=identity["user"], kind="raw_data_export")
            progress(3, 3, "validating", "Raw data export is ready")
            return {**summary, "artifact": _public_artifact(artifact), "download_url": f"/api/artifacts/{artifact['id']}/download"}

        return jobs.submit(workspace_id=DEFAULT_WORKSPACE_ID, owner=identity["user"], task_type="batch_raw_export", input_payload={"artifact_ids": [item["id"] for item in records], "channel_count": len(keys)}, function=run)

    @app.post("/api/chromatograms/query")
    def chromatograms_query(payload: dict[str, Any] = Body(...), identity: dict[str, Any] = Depends(require_chromatogram_plot)) -> dict[str, Any]:
        perform_integration = bool(payload.get("perform_integration"))
        if perform_integration and not has_permission(identity, "chromatogram_integrate"):
            raise HTTPException(status_code=403, detail="External integration permission is required")
        records = artifact_records([str(value) for value in payload.get("artifact_ids", [])], identity)
        return chromatogram_payload(
            artifact_paths(records),
            [str(value) for value in payload.get("channel_keys", [])],
            payload.get("integration") or {},
            int(payload.get("max_points") or 2400),
            perform_integration=perform_integration,
        )

    @app.post("/api/formulas/scan", status_code=202)
    def formulas_scan(payload: dict[str, Any] = Body(...), identity: dict[str, Any] = Depends(require_direct_formula)) -> dict[str, Any]:
        records = artifact_records([str(value) for value in payload.get("artifact_ids", [])], identity)

        def run(progress):
            def relay(item):
                progress(item.completed, max(1, item.total), "running", f"{item.report}: {item.formulas_found} formula(s), ETA {round(item.eta_s or 0)} s")
            return scan_direct_formulas(artifact_paths(records), relay)

        return jobs.submit(workspace_id=DEFAULT_WORKSPACE_ID, owner=identity["user"], task_type="direct_cm_formula_scan", input_payload={"artifact_ids": [item["id"] for item in records]}, function=run)

    @app.post("/api/formulas/evaluate", status_code=202)
    def formulas_evaluate(payload: dict[str, Any] = Body(...), identity: dict[str, Any] = Depends(require_direct_formula)) -> dict[str, Any]:
        records = artifact_records([str(value) for value in payload.get("artifact_ids", [])], identity)
        requested = payload.get("formulas") or []
        if not requested:
            raise HTTPException(status_code=400, detail="Choose at least one Direct CM formula")
        return jobs.submit(
            workspace_id=DEFAULT_WORKSPACE_ID, owner=identity["user"], task_type="direct_cm_formula_evaluation",
            input_payload={"artifact_ids": [item["id"] for item in records], "formula_count": len(requested)},
            function=lambda progress: (progress(1, 2, "running", "Evaluating Direct CM formulas") or evaluate_direct_formulas(artifact_paths(records), [str(value) for value in payload.get("injection_keys", [])], requested)),
        )

    @app.post("/api/single-verification/leak-sensor/catalog")
    def single_verification_leak_sensor_catalog(
        payload: dict[str, Any] = Body(...),
        identity: dict[str, Any] = Depends(require_leak_sensor_analysis),
    ) -> dict[str, Any]:
        records = artifact_records([str(value) for value in payload.get("artifact_ids", [])], identity)
        if not records:
            raise HTTPException(status_code=400, detail="Choose at least one CMBX source")
        return leak_sensor_catalog(artifact_paths(records))

    @app.post("/api/single-verification/leak-sensor", status_code=202)
    def single_verification_leak_sensor(
        payload: dict[str, Any] = Body(...),
        identity: dict[str, Any] = Depends(require_leak_sensor_analysis),
    ) -> dict[str, Any]:
        records = artifact_records([str(value) for value in payload.get("artifact_ids", [])], identity)
        if not records:
            raise HTTPException(status_code=400, detail="Choose at least one CMBX source")
        trace_keys = [str(value) for value in payload.get("trace_keys", [])]
        benchmark_keys = [str(value) for value in payload.get("benchmark_keys", [])]
        if not benchmark_keys:
            raise HTTPException(status_code=400, detail="Choose at least one benchmark LeakDiff trace")

        def run(progress):
            progress(1, 3, "preparing", "Decoding CMBX LeakDiff raw channels")
            result = leak_sensor_analysis(
                artifact_paths(records), trace_keys, benchmark_keys,
            )
            progress(2, 3, "validating", "Comparing response metrics with benchmark curves")
            progress(3, 3, "validating", "Leak sensor verification is ready")
            return result

        return jobs.submit(
            workspace_id=DEFAULT_WORKSPACE_ID,
            owner=identity["user"],
            task_type="single_verification_leak_sensor",
            input_payload={
                "artifact_ids": [item["id"] for item in records],
                "trace_keys": trace_keys,
                "benchmark_keys": benchmark_keys,
            },
            function=run,
        )

    @app.get("/api/quality/config")
    def quality_config(_identity: dict[str, Any] = Depends(require_database_read)) -> dict[str, Any]:
        return database_public_status()

    @app.post("/api/quality/catalog")
    def quality_database_catalog(payload: dict[str, Any] = Body(...), _identity: dict[str, Any] = Depends(require_database_read)) -> dict[str, Any]:
        return quality_catalog(load_database_source(str(payload.get("source_id") or "")))

    @app.post("/api/quality/query", status_code=202)
    def quality_database_query(payload: dict[str, Any] = Body(...), identity: dict[str, Any] = Depends(require_database_read)) -> dict[str, Any]:
        source_id = str(payload.get("source_id") or "")
        table = str(payload.get("table") or "")
        if not table:
            raise HTTPException(status_code=400, detail="Choose a database table")
        return jobs.submit(
            workspace_id=DEFAULT_WORKSPACE_ID, owner=identity["user"], task_type="quality_database_query",
            input_payload={"source_id": source_id, "table": table, "metric": str(payload.get("metric") or "")},
            function=lambda progress: (progress(1, 2, "running", f"Reading {table}") or quality_query(load_database_source(source_id), table, str(payload.get("metric") or ""), {str(key): str(value) for key, value in (payload.get("filters") or {}).items()}, int(payload.get("limit") or 5000))),
        )

    @app.get("/api/artifacts/{artifact_id}/download")
    def download_artifact(
        artifact_id: str,
        identity: dict[str, str] = Depends(current_identity),
    ) -> FileResponse:
        artifact = store.get_artifact(artifact_id)
        if not artifact:
            raise HTTPException(status_code=404, detail="Artifact not found")
        if artifact["owner"].lower() != identity["user"].lower() and identity["role"] != "admin":
            raise HTTPException(status_code=403, detail="This generated asset belongs to another user")
        path = artifact_local_path(artifact)
        if not path.is_file():
            raise HTTPException(status_code=410, detail="Artifact file is no longer available")
        return FileResponse(path, filename=artifact["original_name"])

    @app.get("/api/foq/config")
    def foq_config(_identity: dict[str, Any] = Depends(require_foq_check)) -> dict[str, Any]:
        mapping = default_mapping_path()
        return {
            "mapping_path": str(mapping),
            "mapping_available": mapping.exists(),
            "database": database_public_status(),
        }

    @app.post("/api/foq/inspect", status_code=202)
    def inspect_foq(
        payload: dict[str, Any] = Body(...),
        identity: dict[str, Any] = Depends(require_foq_check),
    ) -> dict[str, Any]:
        records = artifact_records([str(value) for value in payload.get("artifact_ids", [])], identity)
        mapping = Path(str(payload.get("mapping_path") or default_mapping_path()))
        if not mapping.exists():
            raise HTTPException(status_code=400, detail=f"FOQ Location file not found: {mapping}")

        return jobs.submit(
            workspace_id=payload.get("workspace_id") or DEFAULT_WORKSPACE_ID,
            owner=identity["user"],
            task_type="foq_scope_inspection",
            input_payload={"artifact_ids": [item["id"] for item in records], "mapping_path": str(mapping)},
            function=lambda progress: inspect_sources(records, mapping, progress),
        )

    @app.post("/api/foq/metrics")
    def foq_metrics(
        payload: dict[str, Any] = Body(...),
        _identity: dict[str, Any] = Depends(require_foq_check),
    ) -> dict[str, Any]:
        mapping = Path(str(payload.get("mapping_path") or default_mapping_path()))
        if not mapping.exists():
            raise HTTPException(status_code=400, detail=f"FOQ Location file not found: {mapping}")
        devices = [str(value) for value in payload.get("devices", []) if str(value).strip()]
        return {"metrics": metric_catalog(mapping, devices), "devices": sorted(set(devices))}

    @app.post("/api/foq/run", status_code=202)
    def run_foq(
        payload: dict[str, Any] = Body(...),
        identity: dict[str, Any] = Depends(require_foq_check),
    ) -> dict[str, Any]:
        records = artifact_records([str(value) for value in payload.get("artifact_ids", [])], identity)
        mapping = Path(str(payload.get("mapping_path") or default_mapping_path()))
        if not mapping.exists():
            raise HTTPException(status_code=400, detail=f"FOQ Location file not found: {mapping}")
        selections = payload.get("selected_sequences") or {}
        metrics = payload.get("metrics") or []
        if not isinstance(selections, dict) or not selections:
            raise HTTPException(status_code=400, detail="Choose at least one eligible FOQ sequence")
        if not isinstance(metrics, list) or not metrics:
            raise HTTPException(status_code=400, detail="Choose at least one FOQ metric")

        return jobs.submit(
            workspace_id=payload.get("workspace_id") or DEFAULT_WORKSPACE_ID,
            owner=identity["user"],
            task_type="foq_quick_check",
            input_payload={
                "artifact_ids": [item["id"] for item in records],
                "selected_sequence_count": len(selections),
                "metrics": metrics,
                "history": payload.get("history") or {"enabled": False},
            },
            function=lambda progress: run_check(
                records,
                mapping,
                {str(key): [str(value) for value in values] for key, values in selections.items()},
                [str(value) for value in metrics],
                payload.get("history") or {"enabled": False},
                progress,
            ),
        )

    @app.get("/api/jobs")
    def list_jobs(
        limit: int = Query(100, ge=1, le=500),
        _identity: dict[str, str] = Depends(current_identity),
    ) -> list[dict[str, Any]]:
        return store.list_jobs(limit)

    @app.get("/api/jobs/{job_id}")
    def get_job(job_id: str, _identity: dict[str, str] = Depends(current_identity)) -> dict[str, Any]:
        job = store.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job

    @app.get("/api/admin/status")
    def admin_status(_identity: dict[str, str] = Depends(require_admin)) -> dict[str, Any]:
        disk = shutil.disk_usage(config.state_root)
        jobs_by_status: dict[str, int] = {}
        for job in store.list_jobs(500):
            jobs_by_status[job["status"]] = jobs_by_status.get(job["status"], 0) + 1
        return {
            "service": "running",
            "version": APP_VERSION,
            "active_workers": jobs.active_count(),
            "worker_limit": config.worker_count,
            "jobs": jobs_by_status,
            "storage": {
                "state_root": str(config.state_root),
                "shared_root": str(config.shared_root),
                "local_asset_root": str(config.asset_root),
                "local_work_root": str(config.work_root),
                "free_bytes": disk.free,
                "total_bytes": disk.total,
            },
            "authentication": {
                "mode": "iis_windows" if config.trust_proxy_user else "local_development",
                "admin_users_configured": len(config.admin_users),
                "developer_accounts": len(store.list_developer_accounts()),
                "login_required": config.require_login,
            },
        }

    @app.get("/api/admin/developer-accounts")
    def admin_developer_accounts(
        _identity: dict[str, Any] = Depends(require_admin),
    ) -> dict[str, Any]:
        return {
            "accounts": store.list_developer_accounts(),
            "roles": ["analyst", "developer", "admin"],
            "known_permissions": PERMISSION_CATALOG,
            "temporary_password": "000000",
        }

    @app.post("/api/admin/developer-accounts")
    def admin_save_developer_account(
        payload: dict[str, Any] = Body(...),
        _identity: dict[str, Any] = Depends(require_admin),
    ) -> dict[str, Any]:
        email = str(payload.get("email") or "").strip().lower()
        if "@" not in email or len(email) > 254:
            raise HTTPException(status_code=400, detail="Enter a valid email address")
        role = str(payload.get("role") or "developer").strip().lower()
        if role not in {"analyst", "developer", "admin"}:
            raise HTTPException(status_code=400, detail="Unsupported account role")
        permissions = [
            str(value).strip() for value in payload.get("permissions", [])
            if str(value).strip()
        ]
        known_permissions = {item["id"] for item in PERMISSION_CATALOG}
        unknown_permissions = sorted(set(permissions) - known_permissions - {"*"})
        if unknown_permissions:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown module permission(s): {', '.join(unknown_permissions)}",
            )
        password = str(payload.get("password") or "")
        try:
            account = store.save_developer_account(
                email,
                hash_password(password) if password else None,
                role,
                max(0, min(100, int(payload.get("daily_api_limit", config.developer_daily_limit)))),
                list(dict.fromkeys(permissions)),
                bool(payload.get("enabled", True)),
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        store.delete_user_sessions(email)
        account.pop("password_hash", None)
        return account

    @app.get("/api/admin/access-requests")
    def admin_access_requests(
        status: str = Query(""),
        _identity: dict[str, str] = Depends(require_admin),
    ) -> dict[str, Any]:
        day = datetime.now().date().isoformat()
        usage = store.list_method_usage(day)
        for item in usage:
            account = store.get_developer_account(item["user_id"])
            item["base_limit"] = int(account["daily_api_limit"]) if account and account["enabled"] else config.method_api_daily_limit
        return {
            "requests": store.list_access_requests(status),
            "usage_day": day,
            "usage": usage,
            "base_daily_limit": config.method_api_daily_limit,
        }

    @app.post("/api/admin/access-requests/{request_id}/decision")
    def admin_decide_access_request(
        request_id: str,
        payload: dict[str, Any] = Body(...),
        identity: dict[str, str] = Depends(require_admin),
    ) -> dict[str, Any]:
        decision = str(payload.get("decision") or "").lower()
        existing = store.get_access_request(request_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Access request not found")
        if existing["status"] != "pending":
            raise HTTPException(status_code=409, detail="This request has already been decided")
        try:
            decided = store.decide_access_request(
                request_id, decision, identity["user_id"], str(payload.get("note") or "")[:1000]
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return decided or {}

    return app


def _local_identity(config: WebWorkspaceConfig) -> str:
    return config.dev_user.strip() or getpass.getuser()
