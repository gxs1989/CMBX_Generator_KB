from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class WorkspaceStore:
    def __init__(self, database_path: Path):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_path, timeout=30)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def _initialize(self) -> None:
        with self.connect() as connection:
            connection.executescript(
                """
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS workspaces (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    owner TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS artifacts (
                    id TEXT PRIMARY KEY,
                    workspace_id TEXT NOT NULL,
                    owner TEXT NOT NULL,
                    kind TEXT NOT NULL,
                    original_name TEXT NOT NULL,
                    sha256 TEXT NOT NULL,
                    size_bytes INTEGER NOT NULL,
                    storage_path TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(workspace_id) REFERENCES workspaces(id)
                );
                CREATE INDEX IF NOT EXISTS idx_artifacts_workspace ON artifacts(workspace_id, created_at);
                CREATE INDEX IF NOT EXISTS idx_artifacts_sha ON artifacts(sha256);
                CREATE TABLE IF NOT EXISTS jobs (
                    id TEXT PRIMARY KEY,
                    workspace_id TEXT NOT NULL,
                    owner TEXT NOT NULL,
                    task_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    progress_current INTEGER NOT NULL DEFAULT 0,
                    progress_total INTEGER NOT NULL DEFAULT 1,
                    stage TEXT NOT NULL DEFAULT '',
                    message TEXT NOT NULL DEFAULT '',
                    input_json TEXT NOT NULL DEFAULT '{}',
                    result_json TEXT NOT NULL DEFAULT '{}',
                    error TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL,
                    started_at TEXT,
                    finished_at TEXT
                );
                CREATE INDEX IF NOT EXISTS idx_jobs_created ON jobs(created_at DESC);
                CREATE TABLE IF NOT EXISTS user_ai_settings (
                    user_id TEXT NOT NULL,
                    provider TEXT NOT NULL,
                    base_url TEXT NOT NULL,
                    model TEXT NOT NULL,
                    encrypted_api_key TEXT NOT NULL DEFAULT '',
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY(user_id, provider)
                );
                CREATE TABLE IF NOT EXISTS method_api_usage (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    usage_day TEXT NOT NULL,
                    provider TEXT NOT NULL,
                    job_id TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_method_api_usage_user_day
                    ON method_api_usage(user_id, usage_day);
                CREATE TABLE IF NOT EXISTS access_requests (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    request_type TEXT NOT NULL,
                    quota_day TEXT NOT NULL,
                    requested_uses INTEGER NOT NULL DEFAULT 1,
                    reason TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL DEFAULT 'pending',
                    decided_by TEXT NOT NULL DEFAULT '',
                    decision_note TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL,
                    decided_at TEXT
                );
                CREATE INDEX IF NOT EXISTS idx_access_requests_status
                    ON access_requests(status, created_at DESC);
                CREATE TABLE IF NOT EXISTS developer_accounts (
                    email TEXT PRIMARY KEY,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'developer',
                    daily_api_limit INTEGER NOT NULL DEFAULT 10,
                    permissions_json TEXT NOT NULL DEFAULT '[]',
                    enabled INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS auth_sessions (
                    token_hash TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    display_name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    source TEXT NOT NULL,
                    daily_api_limit INTEGER,
                    permissions_json TEXT NOT NULL DEFAULT '[]',
                    created_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_auth_sessions_expiry ON auth_sessions(expires_at);
                """
            )
            connection.execute(
                "UPDATE jobs SET status='failed', error='Service restarted before the job completed', "
                "finished_at=? WHERE status IN ('queued','preparing','running','validating')",
                (utc_now(),),
            )
            connection.execute("DELETE FROM auth_sessions WHERE expires_at<=?", (utc_now(),))

    def get_developer_account(self, email: str) -> dict[str, Any] | None:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT * FROM developer_accounts WHERE email=?", (email.strip().lower(),)
            ).fetchone()
        if not row:
            return None
        result = dict(row)
        result["permissions"] = json.loads(result.pop("permissions_json") or "[]")
        result["enabled"] = bool(result["enabled"])
        return result

    def save_developer_account(
        self, email: str, password_hash: str | None, role: str, daily_api_limit: int,
        permissions: list[str], enabled: bool = True,
    ) -> dict[str, Any]:
        email = email.strip().lower()
        existing = self.get_developer_account(email)
        secret = password_hash or (existing or {}).get("password_hash", "")
        if not secret:
            raise ValueError("A password is required for a new developer account")
        now = utc_now()
        with self.connect() as connection:
            connection.execute(
                """INSERT INTO developer_accounts(
                       email,password_hash,role,daily_api_limit,permissions_json,enabled,created_at,updated_at
                   ) VALUES(?,?,?,?,?,?,?,?)
                   ON CONFLICT(email) DO UPDATE SET password_hash=excluded.password_hash,
                     role=excluded.role,daily_api_limit=excluded.daily_api_limit,
                     permissions_json=excluded.permissions_json,enabled=excluded.enabled,
                     updated_at=excluded.updated_at""",
                (email, secret, role, max(0, int(daily_api_limit)), json.dumps(permissions),
                 1 if enabled else 0, (existing or {}).get("created_at", now), now),
            )
        return self.get_developer_account(email) or {}

    def list_developer_accounts(self) -> list[dict[str, Any]]:
        with self.connect() as connection:
            rows = connection.execute("SELECT * FROM developer_accounts ORDER BY email").fetchall()
        result = []
        for row in rows:
            item = dict(row)
            item.pop("password_hash", None)
            item["permissions"] = json.loads(item.pop("permissions_json") or "[]")
            item["enabled"] = bool(item["enabled"])
            result.append(item)
        return result

    def create_session(
        self, token_hash: str, user_id: str, display_name: str, role: str, source: str,
        daily_api_limit: int | None, permissions: list[str], hours: int = 12,
    ) -> None:
        now = datetime.now(timezone.utc)
        with self.connect() as connection:
            connection.execute(
                """INSERT INTO auth_sessions(token_hash,user_id,display_name,role,source,
                       daily_api_limit,permissions_json,created_at,expires_at)
                   VALUES(?,?,?,?,?,?,?,?,?)""",
                (token_hash, user_id.lower(), display_name, role, source, daily_api_limit,
                 json.dumps(permissions), now.isoformat(timespec="seconds"),
                 (now + timedelta(hours=hours)).isoformat(timespec="seconds")),
            )

    def get_session(self, token_hash: str) -> dict[str, Any] | None:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT * FROM auth_sessions WHERE token_hash=? AND expires_at>?",
                (token_hash, utc_now()),
            ).fetchone()
        if not row:
            return None
        result = dict(row)
        result["permissions"] = json.loads(result.pop("permissions_json") or "[]")
        return result

    def delete_session(self, token_hash: str) -> None:
        with self.connect() as connection:
            connection.execute("DELETE FROM auth_sessions WHERE token_hash=?", (token_hash,))

    def delete_user_sessions(self, user_id: str) -> None:
        with self.connect() as connection:
            connection.execute("DELETE FROM auth_sessions WHERE user_id=?", (user_id.strip().lower(),))

    def ensure_workspace(self, workspace_id: str, name: str, owner: str) -> dict[str, Any]:
        with self.connect() as connection:
            connection.execute(
                "INSERT OR IGNORE INTO workspaces(id,name,owner,created_at) VALUES(?,?,?,?)",
                (workspace_id, name, owner, utc_now()),
            )
            row = connection.execute("SELECT * FROM workspaces WHERE id=?", (workspace_id,)).fetchone()
        return dict(row)

    def list_workspaces(self) -> list[dict[str, Any]]:
        with self.connect() as connection:
            rows = connection.execute("SELECT * FROM workspaces ORDER BY created_at").fetchall()
        return [dict(row) for row in rows]

    def add_artifact(self, record: dict[str, Any]) -> dict[str, Any]:
        with self.connect() as connection:
            connection.execute(
                """INSERT INTO artifacts(
                    id,workspace_id,owner,kind,original_name,sha256,size_bytes,storage_path,created_at
                ) VALUES(?,?,?,?,?,?,?,?,?)""",
                (
                    record["id"], record["workspace_id"], record["owner"], record["kind"],
                    record["original_name"], record["sha256"], record["size_bytes"],
                    record["storage_path"], record.get("created_at", utc_now()),
                ),
            )
        return self.get_artifact(record["id"])

    def get_artifact(self, artifact_id: str) -> dict[str, Any] | None:
        with self.connect() as connection:
            row = connection.execute("SELECT * FROM artifacts WHERE id=?", (artifact_id,)).fetchone()
        return dict(row) if row else None

    def list_artifacts(self, workspace_id: str | None = None) -> list[dict[str, Any]]:
        with self.connect() as connection:
            if workspace_id:
                rows = connection.execute(
                    "SELECT * FROM artifacts WHERE workspace_id=? ORDER BY created_at DESC", (workspace_id,)
                ).fetchall()
            else:
                rows = connection.execute("SELECT * FROM artifacts ORDER BY created_at DESC").fetchall()
        return [dict(row) for row in rows]

    def delete_artifact(self, artifact_id: str) -> bool:
        with self.connect() as connection:
            cursor = connection.execute("DELETE FROM artifacts WHERE id=?", (artifact_id,))
        return cursor.rowcount > 0

    def create_job(self, record: dict[str, Any]) -> dict[str, Any]:
        with self.connect() as connection:
            connection.execute(
                """INSERT INTO jobs(
                    id,workspace_id,owner,task_type,status,progress_current,progress_total,
                    stage,message,input_json,result_json,error,created_at
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    record["id"], record["workspace_id"], record["owner"], record["task_type"],
                    record.get("status", "queued"), 0, 1, "queued", record.get("message", ""),
                    json.dumps(record.get("input", {}), ensure_ascii=False), "{}", "", utc_now(),
                ),
            )
        return self.get_job(record["id"])

    def update_job(self, job_id: str, **changes: Any) -> dict[str, Any] | None:
        if not changes:
            return self.get_job(job_id)
        allowed = {
            "status", "progress_current", "progress_total", "stage", "message",
            "result_json", "error", "started_at", "finished_at",
        }
        values: list[Any] = []
        assignments: list[str] = []
        for key, value in changes.items():
            if key not in allowed:
                continue
            if key == "result_json" and not isinstance(value, str):
                value = json.dumps(value, ensure_ascii=False)
            assignments.append(f"{key}=?")
            values.append(value)
        if assignments:
            values.append(job_id)
            with self.connect() as connection:
                connection.execute(f"UPDATE jobs SET {', '.join(assignments)} WHERE id=?", values)
        return self.get_job(job_id)

    def get_job(self, job_id: str) -> dict[str, Any] | None:
        with self.connect() as connection:
            row = connection.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
        return self._decode_job(row) if row else None

    def list_jobs(self, limit: int = 100) -> list[dict[str, Any]]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT * FROM jobs ORDER BY created_at DESC LIMIT ?", (max(1, min(limit, 500)),)
            ).fetchall()
        return [self._decode_job(row) for row in rows]

    def get_ai_setting(self, user_id: str, provider: str) -> dict[str, Any] | None:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT * FROM user_ai_settings WHERE user_id=? AND provider=?",
                (user_id.lower(), provider.lower()),
            ).fetchone()
        return dict(row) if row else None

    def save_ai_setting(
        self,
        user_id: str,
        provider: str,
        base_url: str,
        model: str,
        encrypted_api_key: str | None = None,
    ) -> dict[str, Any]:
        user_id = user_id.lower()
        provider = provider.lower()
        existing = self.get_ai_setting(user_id, provider)
        secret = existing.get("encrypted_api_key", "") if existing and encrypted_api_key is None else (encrypted_api_key or "")
        with self.connect() as connection:
            connection.execute(
                """INSERT INTO user_ai_settings(user_id,provider,base_url,model,encrypted_api_key,updated_at)
                   VALUES(?,?,?,?,?,?)
                   ON CONFLICT(user_id,provider) DO UPDATE SET
                     base_url=excluded.base_url, model=excluded.model,
                     encrypted_api_key=excluded.encrypted_api_key, updated_at=excluded.updated_at""",
                (user_id, provider, base_url, model, secret, utc_now()),
            )
        return self.get_ai_setting(user_id, provider) or {}

    def method_usage_summary(self, user_id: str, usage_day: str, base_limit: int = 3) -> dict[str, Any]:
        user_id = user_id.lower()
        with self.connect() as connection:
            used = connection.execute(
                "SELECT COUNT(*) FROM method_api_usage WHERE user_id=? AND usage_day=?",
                (user_id, usage_day),
            ).fetchone()[0]
            granted = connection.execute(
                """SELECT COALESCE(SUM(requested_uses),0) FROM access_requests
                   WHERE user_id=? AND quota_day=? AND request_type='method_api_quota' AND status='approved'""",
                (user_id, usage_day),
            ).fetchone()[0]
            pending = connection.execute(
                """SELECT COUNT(*) FROM access_requests
                   WHERE user_id=? AND quota_day=? AND request_type='method_api_quota' AND status='pending'""",
                (user_id, usage_day),
            ).fetchone()[0]
        limit = max(0, int(base_limit)) + int(granted or 0)
        return {
            "day": usage_day,
            "base_limit": int(base_limit),
            "granted_uses": int(granted or 0),
            "limit": limit,
            "used": int(used),
            "remaining": max(0, limit - int(used)),
            "pending_requests": int(pending),
        }

    def claim_method_api_usage(
        self,
        usage_id: str,
        user_id: str,
        usage_day: str,
        provider: str,
        base_limit: int = 3,
    ) -> dict[str, Any]:
        user_id = user_id.lower()
        with self.connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            used = connection.execute(
                "SELECT COUNT(*) FROM method_api_usage WHERE user_id=? AND usage_day=?",
                (user_id, usage_day),
            ).fetchone()[0]
            granted = connection.execute(
                """SELECT COALESCE(SUM(requested_uses),0) FROM access_requests
                   WHERE user_id=? AND quota_day=? AND request_type='method_api_quota' AND status='approved'""",
                (user_id, usage_day),
            ).fetchone()[0]
            limit = max(0, int(base_limit)) + int(granted or 0)
            if int(used) >= limit:
                raise PermissionError("Daily Method API generation quota is exhausted. Submit an access request.")
            connection.execute(
                "INSERT INTO method_api_usage(id,user_id,usage_day,provider,created_at) VALUES(?,?,?,?,?)",
                (usage_id, user_id, usage_day, provider.lower(), utc_now()),
            )
        return self.method_usage_summary(user_id, usage_day, base_limit)

    def attach_usage_job(self, usage_id: str, job_id: str) -> None:
        with self.connect() as connection:
            connection.execute("UPDATE method_api_usage SET job_id=? WHERE id=?", (job_id, usage_id))

    def create_access_request(self, record: dict[str, Any]) -> dict[str, Any]:
        with self.connect() as connection:
            connection.execute(
                """INSERT INTO access_requests(
                    id,user_id,request_type,quota_day,requested_uses,reason,status,created_at
                ) VALUES(?,?,?,?,?,?,?,?)""",
                (
                    record["id"], record["user_id"].lower(), record.get("request_type", "method_api_quota"),
                    record["quota_day"], max(1, int(record.get("requested_uses", 1))),
                    record.get("reason", ""), "pending", utc_now(),
                ),
            )
        return self.get_access_request(record["id"]) or {}

    def get_access_request(self, request_id: str) -> dict[str, Any] | None:
        with self.connect() as connection:
            row = connection.execute("SELECT * FROM access_requests WHERE id=?", (request_id,)).fetchone()
        return dict(row) if row else None

    def list_access_requests(self, status: str = "") -> list[dict[str, Any]]:
        with self.connect() as connection:
            if status:
                rows = connection.execute(
                    "SELECT * FROM access_requests WHERE status=? ORDER BY created_at DESC", (status,)
                ).fetchall()
            else:
                rows = connection.execute("SELECT * FROM access_requests ORDER BY created_at DESC").fetchall()
        return [dict(row) for row in rows]

    def decide_access_request(
        self, request_id: str, status: str, decided_by: str, decision_note: str = ""
    ) -> dict[str, Any] | None:
        if status not in {"approved", "rejected"}:
            raise ValueError("Decision must be approved or rejected")
        with self.connect() as connection:
            connection.execute(
                """UPDATE access_requests SET status=?,decided_by=?,decision_note=?,decided_at=?
                   WHERE id=? AND status='pending'""",
                (status, decided_by.lower(), decision_note, utc_now(), request_id),
            )
        return self.get_access_request(request_id)

    def list_method_usage(self, usage_day: str) -> list[dict[str, Any]]:
        with self.connect() as connection:
            rows = connection.execute(
                """SELECT user_id,provider,COUNT(*) AS used FROM method_api_usage
                   WHERE usage_day=? GROUP BY user_id,provider ORDER BY user_id,provider""",
                (usage_day,),
            ).fetchall()
        return [dict(row) for row in rows]

    @staticmethod
    def _decode_job(row: sqlite3.Row) -> dict[str, Any]:
        result = dict(row)
        for key in ("input_json", "result_json"):
            try:
                result[key.removesuffix("_json")] = json.loads(result.pop(key) or "{}")
            except json.JSONDecodeError:
                result[key.removesuffix("_json")] = {}
        return result
