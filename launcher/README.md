# CMBX Workspace Launchers

## New web server computer

1. Right-click `安装依赖.bat` and choose **Run as administrator**.
2. Run `启动CMBX Web服务器.bat`.
3. Use the displayed local or LAN URL. The default port is `8765`.
4. Run `检查CMBX Web服务器.bat` if startup or access fails.
5. Run `停止CMBX Web服务器.bat` before maintenance.

The installer creates an isolated `.venv`, installs pinned dependencies from the bundled offline wheelhouse, and deploys the approved Chromeleon/FormulaOne runtime. A local Chromeleon installation is not required for the bundled CMBX read/generation functions.

Database credentials, API keys, user accounts, SharePoint synchronization paths, firewall policy, and production write permissions are machine-specific and must be configured on the target server.
