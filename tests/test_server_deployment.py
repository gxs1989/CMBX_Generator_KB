from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_server_requirements_cover_web_and_analysis_runtime() -> None:
    server = (ROOT / "requirements-server.txt").read_text(encoding="utf-8")
    web = (ROOT / "requirements-web.txt").read_text(encoding="utf-8")
    assert "-r requirements-web.txt" in server
    for package in ("fastapi", "uvicorn", "httpx", "python-multipart"):
        assert package in web
    for package in ("openpyxl", "xlrd", "pyodbc"):
        assert package in server
    wheels = list((ROOT / "deployment" / "wheelhouse").glob("*.whl"))
    assert len(wheels) >= 20
    assert any(path.name.startswith("fastapi-0.116.1") for path in wheels)
    assert any(path.name.startswith("pyodbc-5.3.0-cp311") for path in wheels)


def test_chromeleon_runtime_bundle_matches_manifest() -> None:
    runtime_dir = ROOT / "deployment" / "runtime"
    manifest = json.loads((runtime_dir / "RUNTIME_MANIFEST.json").read_text(encoding="utf-8-sig"))
    expected = {item["name"]: item for item in manifest["files"]}
    assert manifest["file_count"] == len(expected) >= 80
    assert {"Dionex.DataCommon.dll", "Dionex.Controls.dll", "Dionex.RawData.dll"} <= set(expected)
    assert {
        "Formula1SideBySideActivationContext.manifest",
        "VCFI5.sxs.manifest",
        "VCFI5.OCX",
        "CM7RE.sxs.manifest",
        "CM7RE.OCX",
    } <= set(expected)

    with zipfile.ZipFile(runtime_dir / "chromeleon-runtime.zip") as archive:
        names = {
            Path(name).name
            for name in archive.namelist()
            if not name.endswith("/") and Path(name).name != "RUNTIME_MANIFEST.json"
        }
        assert names == set(expected)
        for name, item in expected.items():
            digest = hashlib.sha256(archive.read(name)).hexdigest()
            assert digest == item["sha256"]


def test_portable_assets_and_launch_contract_are_present() -> None:
    assets = ROOT / "deployment" / "assets"
    for name in (
        "FOQResultLocations_V2.83.xls",
        "TEMPERATURE_CALIBRATION_720.cmbx",
        "TEMP_HEAT_UP_DOWN_20_50_20.cmbx",
    ):
        assert (assets / name).stat().st_size > 0

    start = (ROOT / "Start_CMBX_Web_Server.ps1").read_text(encoding="utf-8")
    install = (ROOT / "Install_CMBX_Web_Server.ps1").read_text(encoding="utf-8")
    assert '.venv\\Scripts\\python.exe' in start
    assert "CMBX_CHROMELEON_BIN" in start
    assert "/api/health" in start
    assert "ProcessStartInfo" in start
    assert "requirements-server.txt" in install
    assert "chromeleon-runtime.zip" in install
    assert "10.68.182.125" not in start


def test_formulaone_uses_shared_runtime_resolver() -> None:
    for name in ("formulaone_report_exporter.py", "formulaone_workbook_writer.py"):
        source = (ROOT / name).read_text(encoding="utf-8")
        assert "resolve_chromeleon_bin" in source
