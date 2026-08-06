# Portable Web Server Deployment Assets

This directory contains the non-secret assets required to install CMBX Web
Workspace on another approved internal Windows computer.

- `runtime/chromeleon-runtime.zip`: minimal dependency closure used by CMBX
  decoding, raw/audit access, and FormulaOne report operations.
- `runtime/RUNTIME_MANIFEST.json`: source versions and SHA-256 hashes.
- `assets/`: FOQ mapping and CM 7.2/7.3 carrier packages deployed to the
  ProgramData workspace by the installer.
- `wheelhouse/`: pinned Windows/Python 3.11 wheels used for offline application
  dependency installation.
- `installers/`: official offline Python 3.11, Microsoft Visual C++ runtime, and
  SQL Server ODBC Driver installers used only when the target host is missing them.

The Chromeleon runtime bundle is for approved internal Thermo Fisher use. It is
not a substitute for a licensed Chromeleon installation and must not be
published as a public standalone runtime.
