# CMBX Web Workspace Server Deployment

## Purpose

This guide installs the repository as a self-contained LAN Web server on an
approved internal Windows computer. The installer creates an isolated Python
environment, installs pinned packages, deploys the knowledge vault and required
FOQ assets, and installs the bundled Chromeleon runtime dependency closure.

## Package Contents

| Item | Location | Purpose |
|---|---|---|
| Server installer | `Install_CMBX_Web_Server.bat` | One-time host setup |
| Server launcher | `Start_CMBX_Web_Workspace.bat` | Starts the service and opens the local UI |
| Server stop command | `Stop_CMBX_Web_Server.bat` | Stops the background service |
| Python dependencies | `requirements-server.txt` | Pinned Web and analysis packages |
| Offline wheelhouse | `deployment/wheelhouse/` | Local Windows/Python 3.11 package installation |
| Offline prerequisite installers | `deployment/installers/` | Python 3.11, VC++ runtime and SQL Server ODBC Driver 18 |
| Chromeleon runtime | `deployment/runtime/chromeleon-runtime.zip` | CMBX, raw/audit, method/report and FormulaOne runtime |
| Runtime manifest | `deployment/runtime/RUNTIME_MANIFEST.json` | File versions, hashes and source record |
| FOQ/runtime assets | `deployment/assets/` | Mapping and CM 7.2/7.3 carrier packages |
| Knowledge vault | `knowledge_vault/` | Version-controlled operational and engineering KB |
| Simple launchers | `launcher/` | Install, start, stop and preflight entry points |

The Chromeleon runtime bundle is approved for internal Thermo Fisher use only.
It is not a public redistributable and is not a replacement for a licensed
Chromeleon installation.

## New Server Setup

1. Clone or download the complete repository to a short local path, for example
   `C:\CMBX_Workspace`.
2. Right-click `launcher\安装依赖.bat` and choose **Run as administrator**.
3. The installer locates or installs bundled Python 3.11, creates `.venv`, installs the
   pinned server dependencies from the included wheelhouse, deploys CM and FOQ assets, deploys the KB, and
   installs ODBC Driver 18 when needed, and opens TCP port 8765 for Domain/Private networks.
4. Run `launcher\打开CMBX Web工作台.bat`; it starts the service and opens the
   local browser automatically.
5. Startup creates `launcher\CMBX Web LAN Entry.url` with a stable computer-name
   address such as `http://SERVER-NAME:8765/`. Share that shortcut with another
   computer on the same company network. No IP lookup is required.

`launcher\CMBX Web Server Address.txt` is refreshed on every start and also records
the current IP addresses as fallbacks when corporate DNS cannot resolve the
computer name.

The server runs in a hidden background process. Logs and the PID file are under
`C:\ProgramData\CMBX Web Service`. Stopping the terminal does not stop the
server; use `launcher\停止CMBX Web服务器.bat`.

## Machine-Specific Configuration

Uploaded and generated assets are kept under
`%LOCALAPPDATA%\CMBX Web Workspace\assets`; compiler jobs use the adjacent short
`work` directory. This avoids Windows path-limit failures caused by the long synced
SharePoint shortcut. Set `CMBX_WEB_LOCAL_ROOT` in `server.env.ps1` only when another
short local disk is required. Do not point it at OneDrive or a network share.

The installer deliberately does not copy passwords, DSN credentials, personal
API keys, or browser sessions. Configure these after first administrator login:

- create and authorize user accounts in **Admin**;
- configure workspace or personal AI credentials;
- configure production/QCLab DSN paths and credentials;
- connect the SharePoint/OneDrive shortcut
  `CIC HPCS V&V-CMBX Workstation - CMBX` if shared artifact storage is required.

Python `pyodbc` and the official Microsoft ODBC Driver 18 offline installer are
included. The installer installs Driver 18 only when Driver 17/18 is absent.

## Runtime Resolution

The installer extracts the approved CM closure to:

```text
C:\ProgramData\CMBX Web Service\runtime\chromeleon
```

The launcher sets `CMBX_CHROMELEON_BIN` before importing the application. Runtime
resolution then falls back through the ProgramData bundle, repository deployment
folder, legacy dependency folder, and a local Chromeleon installation. This
supports CMBX structure decoding, raw data, audit trails, instrument methods,
report formulas, and FormulaOne workbook operations without hardcoded host paths.

## Preflight and Troubleshooting

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Test_CMBX_Web_Server.ps1
```

The preflight checks Python imports, CM decoding DLLs, FormulaOne, the x86 .NET
compiler, FOQ mapping and CM 7.2 carrier assets. If LAN clients cannot connect,
run `Configure_CMBX_Web_LAN.ps1` as administrator and confirm the current URL
printed by `Start_CMBX_Web_Workspace.bat`.

The server host must remain powered on. Starting Windows does not automatically
start the service; launch it manually as requested by the current operating
model.
