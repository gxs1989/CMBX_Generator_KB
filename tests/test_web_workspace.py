from __future__ import annotations

import io
import json
import time
import zipfile
from pathlib import Path

from fastapi.testclient import TestClient

from generation_project import AssetGenerationResult
from web_workspace.app import create_app
from web_workspace.config import SHAREPOINT_SHORTCUT_NAME, WebWorkspaceConfig
import web_workspace.app as web_app
from web_workspace.foq import load_database_sources


def _config(tmp_path: Path) -> WebWorkspaceConfig:
    return WebWorkspaceConfig(
        state_root=tmp_path / "state",
        shared_root=tmp_path / "shared",
        worker_count=1,
        dev_user="test.user",
        admin_users=("test.user",),
    )


def _minimal_cmbx() -> bytes:
    header = """<?xml version="1.0" encoding="utf-8"?>
<ChromeleonArchive ArchiveVersion="2.0" ChromeleonVersion="7.3">
  <ChromeleonElement Id="seq-1" Name="Web Test Sequence" ItemType="Dionex.Chromeleon.Data.Sequence">
    <ChromeleonElement Id="inj-1" Name="Injection 1" ItemType="Dionex.Chromeleon.Data.Injection">
      <ChromeleonElement Id="sig-1" Name="UV_VIS_1" ItemType="Dionex.Chromeleon.Data.Signal" />
      <ChromeleonElement Id="audit-1" Name="Audit Trail" ItemType="Dionex.Chromeleon.Data.AuditTrail" />
    </ChromeleonElement>
  </ChromeleonElement>
</ChromeleonArchive>"""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("header.xml", header)
    return buffer.getvalue()


def _minimal_method_md() -> bytes:
    return b"""# Minimal Web Method

```tsv
Time\tCommand\tValue\tComment
{Initial Time}\tInstrument Setup\t\t
0.000\tColumnComp.CC.TempCtrl\tOn\t
1.000\tEnd\t\t
```
"""


def test_environment_config_prefers_synced_sharepoint_shortcut(tmp_path: Path, monkeypatch) -> None:
    one_drive = tmp_path / "OneDrive - Company"
    shortcut = one_drive / SHAREPOINT_SHORTCUT_NAME
    shortcut.mkdir(parents=True)
    monkeypatch.setenv("OneDriveCommercial", str(one_drive))
    monkeypatch.delenv("CMBX_WEB_SHARED_ROOT", raising=False)
    monkeypatch.setenv("CMBX_WEB_STATE_ROOT", str(tmp_path / "state"))

    assert WebWorkspaceConfig.from_environment().shared_root == shortcut


def test_health_and_static_home(tmp_path: Path) -> None:
    with TestClient(create_app(_config(tmp_path))) as client:
        health = client.get("/api/health")
        assert health.status_code == 200
        assert health.json()["user"]["user"] == "test.user"
        assert health.json()["user"]["role"] == "admin"
        page = client.get("/")
        assert page.status_code == 200
        assert "CMBX Workspace" in page.text
        assert 'id="singleChartFontSize"' in page.text
        assert "9 pt" in page.text
        assert 'id="singleChartRatio"' in page.text
        assert "3:2" in page.text
        script = client.get("/static/app.js?v=20260804-leak-analyzer-v8")
        assert script.status_code == 200
        assert "copyLeakChart" in script.text
        assert "ClipboardItem" in script.text
        assert "decimals:0" in script.text
        assert "decimals:2" in script.text
        assert "legacyCopyChart" in script.text


def test_home_map_root_has_clearance_above_connector() -> None:
    stylesheet = (Path(__file__).parents[1] / "web_workspace" / "static" / "app.css").read_text(encoding="utf-8")
    assert ".workflow-map { --map-gap: 18px; position: relative; max-width: 1120px; padding-top: 14px; }" in stylesheet
    assert "transform: translateY(-10px)" in stylesheet


def test_upload_rejects_non_cmbx(tmp_path: Path) -> None:
    with TestClient(create_app(_config(tmp_path))) as client:
        response = client.post(
            "/api/artifacts/upload",
            files={"file": ("notes.txt", b"not a package", "text/plain")},
        )
        assert response.status_code == 400
        assert "Only .cmbx" in response.json()["detail"]


def test_personal_md_library_upload_preflight_and_delete(tmp_path: Path) -> None:
    with TestClient(create_app(_config(tmp_path))) as client:
        uploaded = client.post(
            "/api/artifacts/md-upload?kind=method_md",
            files={"file": ("library_method.md", _minimal_method_md(), "text/markdown")},
        )
        assert uploaded.status_code == 201, uploaded.text
        artifact = uploaded.json()["artifact"]
        assert artifact["kind"] == "method_md"
        assert any(item["id"] == artifact["id"] for item in client.get("/api/artifacts?kind=method_md").json())

        checked = client.post(f"/api/artifacts/{artifact['id']}/preflight")
        assert checked.status_code == 200
        assert checked.json()["artifact"]["id"] == artifact["id"]

        deleted = client.delete(f"/api/artifacts/{artifact['id']}")
        assert deleted.status_code == 200
        assert deleted.json()["deleted"] is True
        assert client.get("/api/artifacts?kind=method_md").json() == []


def test_upload_scan_and_inventory_roundtrip(tmp_path: Path) -> None:
    with TestClient(create_app(_config(tmp_path))) as client:
        uploaded = client.post(
            "/api/artifacts/upload",
            files={"file": ("sample.cmbx", _minimal_cmbx(), "application/octet-stream")},
        )
        assert uploaded.status_code == 201
        artifact = uploaded.json()
        assert artifact["original_name"] == "sample.cmbx"
        assert "storage_path" not in artifact

        queued = client.post(f"/api/cmbx/{artifact['id']}/scan")
        assert queued.status_code == 202
        job_id = queued.json()["id"]

        job = None
        for _ in range(100):
            job = client.get(f"/api/jobs/{job_id}").json()
            if job["status"] in {"completed", "failed"}:
                break
            time.sleep(0.02)
        assert job is not None
        assert job["status"] == "completed", job

        inventory = client.get(f"/api/cmbx/{artifact['id']}/inventory")
        assert inventory.status_code == 200
        payload = inventory.json()
        assert payload["summary"]["sequences"] == 1
        assert payload["summary"]["injections"] == 1
        assert payload["summary"]["channels"] == 1
        assert payload["tree"][0]["children"][0]["name"] == "Injection 1"


def test_analysis_catalog_and_direct_formula_scan_accept_uploaded_cmbx(tmp_path: Path) -> None:
    with TestClient(create_app(_config(tmp_path))) as client:
        uploaded = client.post(
            "/api/artifacts/upload",
            files={"file": ("analysis.cmbx", _minimal_cmbx(), "application/octet-stream")},
        ).json()
        catalog = client.post("/api/analysis/catalog", json={"artifact_ids": [uploaded["id"]]})
        assert catalog.status_code == 200
        payload = catalog.json()
        assert payload["packages"][0]["name"].endswith("analysis.cmbx")
        assert payload["injections"][0]["injection"] == "Injection 1"
        assert payload["channels"][0]["channel"] == "UV_VIS_1"

        queued = client.post("/api/formulas/scan", json={"artifact_ids": [uploaded["id"]]})
        assert queued.status_code == 202
        job_id = queued.json()["id"]
        for _ in range(100):
            job = client.get(f"/api/jobs/{job_id}").json()
            if job["status"] in {"completed", "failed"}:
                break
            time.sleep(0.02)
        assert job["status"] == "completed", job
        assert job["result"]["formulas"] == []


def test_single_verification_leak_sensor_runs_as_personal_job(tmp_path: Path, monkeypatch) -> None:
    captured = {}

    def fake_catalog(paths):
        return {"traces": [{"key": "trace-1", "package": "leak.cmbx", "sequence": "S1", "injection": "Leak", "channel": "LEDBoard_LeakDiff"}], "scope": "Liquid-leak injections", "errors": []}

    def fake_analysis(paths, trace_keys, benchmark_keys):
        captured.update(paths=[str(item) for item in paths], trace_keys=trace_keys, benchmark_keys=benchmark_keys)
        return {
            "algorithm": "Leak Sensor Analyzer V1.1 raw-curve metrics",
            "summary": {"total": 1, "benchmark": 1, "better": 0, "mixed": 0, "worse": 0, "unmatched": 0},
            "rows": [{"package": "leak.cmbx", "sequence": "S1", "injection": "Leak", "evaluation": "Benchmark"}],
            "curves": [],
        }

    monkeypatch.setattr(web_app, "leak_sensor_catalog", fake_catalog)
    monkeypatch.setattr(web_app, "leak_sensor_analysis", fake_analysis)
    with TestClient(create_app(_config(tmp_path))) as client:
        artifact = client.post(
            "/api/artifacts/upload", files={"file": ("leak.cmbx", _minimal_cmbx(), "application/octet-stream")},
        ).json()
        catalog = client.post(
            "/api/single-verification/leak-sensor/catalog", json={"artifact_ids": [artifact["id"]]},
        )
        assert catalog.status_code == 200
        assert catalog.json()["traces"][0]["channel"] == "LEDBoard_LeakDiff"
        queued = client.post(
            "/api/single-verification/leak-sensor",
            json={"artifact_ids": [artifact["id"]], "trace_keys": ["trace-1"], "benchmark_keys": ["trace-1"]},
        )
        assert queued.status_code == 202, queued.text
        for _ in range(100):
            job = client.get(f"/api/jobs/{queued.json()['id']}").json()
            if job["status"] in {"completed", "failed"}:
                break
            time.sleep(0.02)
        assert job["status"] == "completed", job
        assert job["result"]["summary"]["benchmark"] == 1
        assert captured["trace_keys"] == ["trace-1"]
        assert captured["benchmark_keys"] == ["trace-1"]


def test_home_exposes_all_first_release_workflows(tmp_path: Path) -> None:
    with TestClient(create_app(_config(tmp_path))) as client:
        page = client.get("/").text
        for view in ("report", "raw", "chrom", "formula", "quality", "single"):
            assert f'data-view="{view}"' in page
        capabilities = client.get("/api/capabilities").json()
        assert "batch_raw_export" in capabilities["available"]
        assert "report_generation" in capabilities["available"]
        assert "quality_database_read" in capabilities["available"]


def test_admin_status_reports_separate_roots(tmp_path: Path) -> None:
    config = _config(tmp_path)
    with TestClient(create_app(config)) as client:
        response = client.get("/api/admin/status")
        assert response.status_code == 200
        storage = response.json()["storage"]
        assert storage["state_root"] == str(config.state_root)
        assert storage["shared_root"] == str(config.shared_root)


def test_admin_is_not_available_to_an_unlisted_user(tmp_path: Path) -> None:
    config = WebWorkspaceConfig(
        state_root=tmp_path / "state",
        shared_root=tmp_path / "shared",
        dev_user="other.user",
        admin_users=("xiaoshu.guan",),
    )
    with TestClient(create_app(config)) as client:
        health = client.get("/api/health").json()
        assert health["user"]["role"] == "analyst"
        response = client.get("/api/admin/status")
        assert response.status_code == 403


def test_direct_lan_client_is_always_an_analyst(tmp_path: Path) -> None:
    config = _config(tmp_path)
    with TestClient(create_app(config), client=("10.68.182.99", 50000)) as client:
        health = client.get("/api/health").json()
        assert health["user"]["role"] == "analyst"
        assert health["user"]["source"] == "lan_direct"
        assert client.get("/api/admin/status").status_code == 403


def test_foq_config_and_home_entry_are_available(tmp_path: Path, monkeypatch) -> None:
    mapping = tmp_path / "FOQResultLocations.xls"
    mapping.write_bytes(b"mapping-placeholder")
    monkeypatch.setattr(web_app, "default_mapping_path", lambda: mapping)
    with TestClient(create_app(_config(tmp_path))) as client:
        page = client.get("/")
        assert 'data-view="foq"' in page.text
        config = client.get("/api/foq/config")
        assert config.status_code == 200
        assert config.json()["mapping_available"] is True


def test_foq_scope_inspection_uses_persistent_job(tmp_path: Path, monkeypatch) -> None:
    mapping = tmp_path / "FOQResultLocations.xls"
    mapping.write_bytes(b"mapping-placeholder")
    monkeypatch.setattr(web_app, "default_mapping_path", lambda: mapping)

    def fake_inspection(records, mapping_path, progress):
        progress(1, 2, "running", "Reading sequences")
        progress(2, 2, "validating", "FOQ scope ready")
        return {"sequences": [], "metrics": [], "mapping_path": str(mapping_path), "errors": []}

    monkeypatch.setattr(web_app, "inspect_sources", fake_inspection)
    with TestClient(create_app(_config(tmp_path))) as client:
        artifact = client.post(
            "/api/artifacts/upload",
            files={"file": ("sample.cmbx", _minimal_cmbx(), "application/octet-stream")},
        ).json()
        response = client.post("/api/foq/inspect", json={"artifact_ids": [artifact["id"]]})
        assert response.status_code == 202
        job_id = response.json()["id"]
        for _ in range(100):
            job = client.get(f"/api/jobs/{job_id}").json()
            if job["status"] in {"completed", "failed"}:
                break
            time.sleep(0.02)
        assert job["status"] == "completed", job
        assert job["task_type"] == "foq_scope_inspection"
        assert job["result"]["mapping_path"] == str(mapping)


def test_database_source_registry_supports_multiple_filedsns(tmp_path: Path) -> None:
    registry = tmp_path / "database_sources.json"
    registry.write_text(
        json.dumps(
            {
                "default_source": "production",
                "sources": [
                    {"id": "production", "label": "Production history", "dsn": "production.dsn", "username": "reader"},
                    {"id": "qclab", "label": "QCLab", "dsn": "qclab.dsn", "database": "QCLab", "username": "qc"},
                ],
            }
        ),
        encoding="utf-8",
    )
    sources, default_source = load_database_sources(registry)
    assert default_source == "production"
    assert [item[0] for item in sources] == ["production", "qclab"]
    assert sources[0][2].dsn == "production.dsn"
    assert sources[1][2].database == "QCLab"


def test_foq_client_keeps_full_result_for_history_chart() -> None:
    script = (Path(__file__).parents[1] / "web_workspace" / "static" / "app.js").read_text(encoding="utf-8")
    assert "state.foq.result = result;" in script
    assert "result?.history_samples" in script


def test_foq_client_provides_copyable_metric_and_tcc_summary_outputs() -> None:
    static = Path(__file__).parents[1] / "web_workspace" / "static"
    page = (static / "index.html").read_text(encoding="utf-8")
    script = (static / "app.js").read_text(encoding="utf-8")
    assert 'id="foqOutputLayout"' in page
    assert "Selected chart metric" in page
    assert "TCC QC Summary - Xiaoshu" in page
    assert "const TCC_QC_SUMMARY_COLUMNS" in script
    assert 'label:"Heat Up Time", aliases:["HeatUp_Time_20to50"]' in script
    assert 'label:"Accruacy 85", aliases:["TempAcc85"]' in script
    assert "navigator.clipboard.writeText" in script
    assert 'type:"text/tab-separated-values;charset=utf-8"' in script


def test_method_md_preflight_returns_renderable_rows(tmp_path: Path) -> None:
    with TestClient(create_app(_config(tmp_path))) as client:
        page = client.get("/")
        assert 'data-view="method"' in page.text
        response = client.post(
            "/api/method/preflight",
            files={"file": ("minimal_method.md", _minimal_method_md(), "text/markdown")},
        )
        assert response.status_code == 201, response.text
        payload = response.json()
        assert payload["preflight"]["ready"] is True
        assert [row["Kind"] for row in payload["preflight"]["rows"]] == ["Stage", "Command", "End"]
        assert payload["artifact"]["kind"] == "method_md"


def test_method_ai_package_and_generation_jobs(tmp_path: Path, monkeypatch) -> None:
    kb = tmp_path / "TCC_METHOD_SPEC.md"
    kb.write_text("# Method SPEC\n", encoding="utf-8")
    monkeypatch.setattr(web_app, "recommended_online_kb_files_for_modules", lambda *args, **kwargs: [kb])

    def fake_generate(request, preflight):
        project = request.output_root / "fake_project"
        project.mkdir(parents=True)
        output = project / "outputs" / "generated_method.cmbx"
        output.parent.mkdir()
        output.write_bytes(_minimal_cmbx())
        manifest = project / "project.json"
        manifest.write_text("{}", encoding="utf-8")
        return AssetGenerationResult(project, output, manifest)

    monkeypatch.setattr(web_app, "generate_asset", fake_generate)
    with TestClient(create_app(_config(tmp_path))) as client:
        package = client.post(
            "/api/method/ai-package",
            json={"modules": ["TCC"], "request": "hold 40 C", "small_context": False, "optimize": False},
        )
        assert package.status_code == 201, package.text
        assert package.json()["files"] == [kb.name]
        assert client.get(package.json()["download_url"]).status_code == 200

        imported = client.post(
            "/api/method/preflight",
            files={"file": ("minimal_method.md", _minimal_method_md(), "text/markdown")},
        ).json()
        queued = client.post(
            "/api/method/generate",
            json={
                "artifact_id": imported["artifact"]["id"],
                "asset_name": "Web_Minimal_Method",
                "target_cm_version": "7.2 compatible",
                "family": "TCC",
                "intent": "test",
            },
        )
        assert queued.status_code == 202, queued.text
        for _ in range(100):
            job = client.get(f"/api/jobs/{queued.json()['id']}").json()
            if job["status"] in {"completed", "failed"}:
                break
            time.sleep(0.02)
        assert job["status"] == "completed", job
        assert client.get(job["result"]["download_url"]).status_code == 200


def _iis_config(tmp_path: Path) -> WebWorkspaceConfig:
    return WebWorkspaceConfig(
        state_root=tmp_path / "state",
        shared_root=tmp_path / "shared",
        worker_count=1,
        trust_proxy_user=True,
        admin_users=("xiaoshu.guan@thermofisher.com",),
        method_api_daily_limit=3,
    )


def test_personal_ai_key_is_encrypted_and_never_returned(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(web_app, "protect_secret", lambda value: f"protected:{value}")
    with TestClient(create_app(_iis_config(tmp_path))) as client:
        headers = {"x-remote-user": "analyst.one@thermofisher.com"}
        saved = client.put(
            "/api/account/ai-settings/deepseek",
            headers=headers,
            json={"api_key": "secret-key", "base_url": "https://api.deepseek.com/v1", "model": "deepseek-chat"},
        )
        assert saved.status_code == 200, saved.text
        assert saved.json()["api_key_configured"] is True
        assert "secret-key" not in saved.text
        listed = client.get("/api/account/ai-settings", headers=headers)
        assert listed.status_code == 200
        assert "secret-key" not in listed.text


def test_desktop_gpt_key_is_migrated_only_to_configured_owner(tmp_path: Path, monkeypatch) -> None:
    config = _iis_config(tmp_path)
    monkeypatch.setattr(
        web_app,
        "load_ai_config",
        lambda: {
            "base_url": "https://desktop.example/v1",
            "model": "gpt-desktop",
            "api_key": "desktop-secret",
        },
    )
    monkeypatch.setattr(web_app, "protect_secret", lambda value: f"protected:{value}")
    with TestClient(create_app(config)) as client:
        admin = {"x-remote-user": "xiaoshu.guan@thermofisher.com"}
        analyst = {"x-remote-user": "analyst.one@thermofisher.com"}
        admin_settings = client.get("/api/account/ai-settings", headers=admin).json()
        analyst_settings = client.get("/api/account/ai-settings", headers=analyst).json()
        gpt_admin = next(item for item in admin_settings["providers"] if item["provider"] == "gpt")
        gpt_analyst = next(item for item in analyst_settings["providers"] if item["provider"] == "gpt")
        assert gpt_admin["api_key_configured"] is True
        assert gpt_admin["model"] == "gpt-desktop"
        assert gpt_analyst["api_key_configured"] is True
        assert gpt_analyst["credential_source"] == "workspace"
        saved = client.app.state.store.get_ai_setting("xiaoshu.guan@thermofisher.com", "gpt")
        assert saved["encrypted_api_key"] == "protected:desktop-secret"
        assert "desktop-secret" not in str(admin_settings)


def test_login_required_developer_account_and_admin_account_management(tmp_path: Path) -> None:
    config = WebWorkspaceConfig(
        state_root=tmp_path / "state",
        shared_root=tmp_path / "shared",
        worker_count=1,
        admin_users=("xiaoshu.guan@thermofisher.com",),
        desktop_ai_owner="xiaoshu.guan@thermofisher.com",
        require_login=True,
        developer_daily_limit=10,
    )
    with TestClient(create_app(config), client=("10.68.178.99", 50000)) as client:
        assert client.get("/api/health").status_code == 401
        options = client.get("/api/auth/options").json()
        assert options["authenticated"] is False
        assert options["windows_available"] is False
        logged_in = client.post(
            "/api/auth/developer-login",
            json={"email": "xiaoshu.guan@thermofisher.com", "password": "000000"},
        )
        assert logged_in.status_code == 200, logged_in.text
        assert logged_in.json()["user"]["role"] == "admin"
        created = client.post(
            "/api/admin/developer-accounts",
            json={
                "email": "developer.one@thermofisher.com",
                "password": "000000",
                "role": "developer",
                "daily_api_limit": 12,
                "permissions": ["method_generate", "foq_check"],
                "enabled": True,
            },
        )
        assert created.status_code == 200, created.text
        assert created.json()["daily_api_limit"] == 12
        assert "password_hash" not in created.text
        assert client.post("/api/auth/logout").status_code == 200
        developer = client.post(
            "/api/auth/developer-login",
            json={"email": "developer.one@thermofisher.com", "password": "000000"},
        )
        assert developer.status_code == 200
        assert developer.json()["user"]["role"] == "developer"
        quota = client.get("/api/account/method-quota").json()
        assert quota["base_limit"] == 12
        assert client.get("/api/admin/status").status_code == 403


def test_developer_session_uses_current_permissions_without_relogin(tmp_path: Path) -> None:
    config = WebWorkspaceConfig(
        state_root=tmp_path / "state",
        shared_root=tmp_path / "shared",
        worker_count=1,
        admin_users=("xiaoshu.guan@thermofisher.com",),
        desktop_ai_owner="xiaoshu.guan@thermofisher.com",
        require_login=True,
    )
    with TestClient(create_app(config), client=("10.68.178.99", 50000)) as client:
        store = client.app.state.store
        store.save_developer_account(
            "permission.refresh@thermofisher.com", web_app.hash_password("000000"),
            "developer", 3, ["instrument_method_generation"], True,
        )
        logged_in = client.post(
            "/api/auth/developer-login",
            json={"email": "permission.refresh@thermofisher.com", "password": "000000"},
        )
        assert logged_in.status_code == 200
        assert client.get("/api/method/config").json()["allowed_routes"]["gpt"] is False

        store.save_developer_account(
            "permission.refresh@thermofisher.com", None,
            "developer", 7, ["instrument_method_generation", "method_generate"], True,
        )
        refreshed = client.get("/api/method/config")
        assert refreshed.status_code == 200
        assert refreshed.json()["allowed_routes"]["gpt"] is True
        assert refreshed.json()["quota"]["base_limit"] == 7


def test_first_lan_visit_creates_basic_analyst_account(tmp_path: Path) -> None:
    config = WebWorkspaceConfig(
        state_root=tmp_path / "state",
        shared_root=tmp_path / "shared",
        worker_count=1,
        admin_users=("xiaoshu.guan@thermofisher.com",),
        desktop_ai_owner="xiaoshu.guan@thermofisher.com",
        require_login=True,
        method_api_daily_limit=3,
        allow_developer_self_registration=True,
        developer_bootstrap_password="000000",
    )
    with TestClient(create_app(config), client=("10.68.178.77", 50000)) as client:
        options = client.get("/api/auth/options").json()
        assert options["developer_self_registration"] is True
        logged_in = client.post(
            "/api/auth/developer-login",
            json={"email": "first.user@thermofisher.com", "password": "000000"},
        )
        assert logged_in.status_code == 200, logged_in.text
        identity = logged_in.json()["user"]
        assert identity["role"] == "analyst"
        assert identity["daily_api_limit"] == 3
        assert "method_generate" in identity["permissions"]
        account = client.app.state.store.get_developer_account("first.user@thermofisher.com")
        assert account is not None
        assert account["role"] == "analyst"


def test_first_lan_visit_rejects_invalid_email_or_password(tmp_path: Path) -> None:
    config = WebWorkspaceConfig(
        state_root=tmp_path / "state",
        shared_root=tmp_path / "shared",
        worker_count=1,
        require_login=True,
        allow_developer_self_registration=True,
        developer_bootstrap_password="000000",
    )
    with TestClient(create_app(config), client=("10.68.178.77", 50000)) as client:
        assert client.post(
            "/api/auth/developer-login", json={"email": "not-an-email", "password": "000000"}
        ).status_code == 401
        assert client.post(
            "/api/auth/developer-login",
            json={"email": "first.user@thermofisher.com", "password": "wrong"},
        ).status_code == 401


def test_method_api_quota_request_and_admin_approval(tmp_path: Path) -> None:
    with TestClient(create_app(_iis_config(tmp_path))) as client:
        analyst = {"x-remote-user": "analyst.one@thermofisher.com"}
        admin = {"x-remote-user": "xiaoshu.guan@thermofisher.com"}
        for index in range(3):
            with client.app.state.store.connect() as connection:
                connection.execute(
                    "INSERT INTO method_api_usage(id,user_id,usage_day,provider,created_at) VALUES(?,?,?,?,datetime('now'))",
                    (f"use-{index}", "analyst.one@thermofisher.com", time.strftime("%Y-%m-%d"), "gpt"),
                )
        quota = client.get("/api/account/method-quota", headers=analyst).json()
        assert quota["used"] == 3
        assert quota["remaining"] == 0
        requested = client.post(
            "/api/account/access-requests", headers=analyst, json={"requested_uses": 2, "reason": "validation work"}
        )
        assert requested.status_code == 201, requested.text
        request_id = requested.json()["id"]
        assert client.get("/api/admin/access-requests", headers=analyst).status_code == 403
        approved = client.post(
            f"/api/admin/access-requests/{request_id}/decision",
            headers=admin,
            json={"decision": "approved", "note": "approved"},
        )
        assert approved.status_code == 200, approved.text
        quota = client.get("/api/account/method-quota", headers=analyst).json()
        assert quota["limit"] == 5
        assert quota["remaining"] == 2


def test_automatic_method_generation_uses_ai_then_compiles(tmp_path: Path, monkeypatch) -> None:
    kb = tmp_path / "TCC_METHOD_SPEC.md"
    kb.write_text("# Method SPEC\n", encoding="utf-8")
    monkeypatch.setattr(web_app, "recommended_online_kb_files_for_modules", lambda *args, **kwargs: [kb])
    monkeypatch.setattr(web_app, "protect_secret", lambda value: f"protected:{value}")
    monkeypatch.setattr(web_app, "unprotect_secret", lambda value: value.removeprefix("protected:"))
    monkeypatch.setattr(web_app, "generate_method_markdown", lambda *args, **kwargs: _minimal_method_md().decode())
    monkeypatch.setattr(web_app, "generate_report_markdown", lambda *args, **kwargs: "# AI Report Template\n")

    def fake_generate(request, preflight):
        project = request.output_root / "auto_project"
        project.mkdir(parents=True)
        output = project / "outputs" / "auto_method.cmbx"
        output.parent.mkdir()
        output.write_bytes(_minimal_cmbx())
        manifest = project / "project.json"
        manifest.write_text("{}", encoding="utf-8")
        return AssetGenerationResult(project, output, manifest)

    monkeypatch.setattr(web_app, "generate_asset", fake_generate)
    with TestClient(create_app(_iis_config(tmp_path))) as client:
        headers = {"x-remote-user": "analyst.one@thermofisher.com"}
        configured = client.put(
            "/api/account/ai-settings/gpt",
            headers=headers,
            json={"api_key": "test-key", "base_url": "https://api.openai.com/v1", "model": "gpt-5.5"},
        )
        assert configured.status_code == 200
        queued = client.post(
            "/api/method/auto-generate",
            headers=headers,
            json={
                "provider": "gpt", "modules": ["TCC"], "request": "hold 40 C",
                "asset_name": "Automatic Method", "target_cm_version": "7.2 compatible",
            },
        )
        assert queued.status_code == 202, queued.text
        for _ in range(100):
            job = client.get(f"/api/jobs/{queued.json()['id']}", headers=headers).json()
            if job["status"] in {"completed", "failed"}:
                break
            time.sleep(0.02)
        assert job["status"] == "completed", job
        assert job["result"]["cmbx_generated"] is True
        assert client.get(job["result"]["download_url"], headers=headers).status_code == 200

        md_only = client.post(
            "/api/method/auto-generate",
            headers=headers,
            json={
                "provider": "gpt", "modules": ["TCC"], "request": "hold 60 C",
                "asset_name": "MD Only", "target_cm_version": "7.2 compatible", "md_only": True,
            },
        )
        assert md_only.status_code == 202, md_only.text
        for _ in range(100):
            md_job = client.get(f"/api/jobs/{md_only.json()['id']}", headers=headers).json()
            if md_job["status"] in {"completed", "failed"}:
                break
            time.sleep(0.02)
        assert md_job["status"] == "completed", md_job
        assert md_job["result"]["cmbx_generated"] is False
        assert md_job["result"]["md_only"] is True
        assert client.get(md_job["result"]["method_md_download_url"], headers=headers).status_code == 200
        report_package = client.post(
            "/api/report/ai-package", headers=headers,
            json={
                "modules": ["TCC"], "request": "Create the matching report",
                "method_md_artifact_id": md_job["result"]["method_md_artifact"]["id"],
            },
        )
        assert report_package.status_code == 403
        report_job = client.post(
            "/api/report/auto-generate", headers=headers,
            json={
                "modules": ["TCC"], "request": "Create the matching report",
                "method_md_artifact_id": md_job["result"]["method_md_artifact"]["id"],
            },
        )
        assert report_job.status_code == 202, report_job.text
        for _ in range(100):
            generated_report = client.get(f"/api/jobs/{report_job.json()['id']}", headers=headers).json()
            if generated_report["status"] in {"completed", "failed"}:
                break
            time.sleep(0.02)
        assert generated_report["status"] == "completed", generated_report
        assert generated_report["result"]["report_md_artifact"]["kind"] == "report_md"


def test_module_permissions_and_user_cmbx_isolation(tmp_path: Path, monkeypatch) -> None:
    kb = tmp_path / "REPORT_SPEC.md"
    kb.write_text("# Report SPEC\n", encoding="utf-8")
    monkeypatch.setattr(web_app, "recommended_online_kb_files_for_modules", lambda *args, **kwargs: [kb])
    with TestClient(create_app(_iis_config(tmp_path))) as client:
        user_a = {"x-remote-user": "user.a@thermofisher.com"}
        user_b = {"x-remote-user": "user.b@thermofisher.com"}
        admin = {"x-remote-user": "xiaoshu.guan@thermofisher.com"}

        config = client.get("/api/method/config", headers=user_a)
        assert config.status_code == 200
        assert config.json()["allowed_routes"] == {"manual": False, "gpt": True, "deepseek": False}
        assert client.post("/api/method/ai-package", headers=user_a, json={"modules": ["TCC"]}).status_code == 403
        assert client.post(
            "/api/method/auto-generate", headers=user_a,
            json={"provider": "deepseek", "modules": ["TCC"], "request": "test"},
        ).status_code == 403

        permission_catalog = client.get("/api/admin/developer-accounts", headers=admin).json()["known_permissions"]
        roots = [item for item in permission_catalog if not item.get("parent")]
        assert len(roots) == 9
        assert {item["group"] for item in roots} == {
            "Design & Generate", "Chromatograms & Results", "Quality Control & Database", "Single Verification",
        }
        assert any(item["id"] == "instrument_method_generation" for item in roots)
        assert any(item["id"] == "chromatogram_integrate" for item in permission_catalog)
        assert any(item["id"] == "method_manual_web_ai" and not item["default"] for item in permission_catalog)
        assert any(item["id"] == "report_manual_web_ai" and not item["default"] for item in permission_catalog)
        assert any(item["id"] == "single_verification" and item["default"] for item in permission_catalog)
        assert any(
            item["id"] == "leak_sensor_analysis"
            and item["parent"] == "single_verification"
            and item["default"]
            for item in permission_catalog
        )

        uploaded = client.post(
            "/api/artifacts/upload", headers=user_a,
            files={"file": ("private.cmbx", _minimal_cmbx(), "application/octet-stream")},
        ).json()
        assert len(client.get("/api/artifacts", headers=user_a).json()) == 1
        assert client.get("/api/artifacts", headers=user_b).json() == []
        denied = client.post(
            "/api/analysis/catalog", headers=user_b, json={"artifact_ids": [uploaded["id"]]},
        )
        assert denied.status_code == 403

        linked = client.post(
            "/api/report/ai-package", headers=user_a,
            json={"modules": ["TCC"], "method_md_artifact_id": "does-not-exist"},
        )
        assert linked.status_code == 403
