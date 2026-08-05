# CMBX Workspace V1.42 Offline Server Package

## Install on another Windows computer

1. Extract the package to a short local path, preferably `C:\CMBX_Workspace`.
2. Right-click `launcher\安装依赖.bat` and choose **Run as administrator**.
3. After preflight passes, run `launcher\启动CMBX Web服务器.bat`.
4. Open the printed local URL on the server, or the printed LAN URL on another company-network computer.
5. Use `launcher\检查CMBX Web服务器.bat` for diagnostics and `launcher\停止CMBX Web服务器.bat` to stop the service.

## Included dependencies

- Python 3.11.9 offline installer.
- Pinned Python 3.11 Windows wheelhouse.
- Microsoft Visual C++ x64 runtime installer.
- Microsoft ODBC Driver 18 for SQL Server installer.
- Approved internal Chromeleon/CMBX runtime, including FormulaOne SxS/OCX components.
- FOQ mapping and CM 7.2/7.3 method carrier assets.
- Version-controlled Markdown knowledge vault.

The installer creates `.venv` and deploys runtime state under `C:\ProgramData\CMBX Web Service`. It does not require a pre-existing Python or Chromeleon installation for the bundled application workflows.

## Not copied from the development computer

Passwords, database credentials, API keys, user accounts, browser sessions, production write approval, and personal SharePoint synchronization paths are intentionally excluded. Configure these through Admin on the target server.

## Operating notes

- The server computer must remain powered on for LAN users.
- Startup remains manual after Windows restart.
- Default TCP port: `8765`.
- Internal Chromeleon runtime files must remain within approved Thermo Fisher use.
