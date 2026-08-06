# Bundled Offline Installers

These installers are included so an approved internal Windows server can be provisioned without downloading application prerequisites during setup.

| File | Version | Publisher | SHA-256 |
|---|---|---|---|
| `python-3.11.9-amd64.exe` | 3.11.9 | Python Software Foundation | `5ee42c4eee1e6b4464bb23722f90b45303f79442df63083f05322f1785f5fdde` |
| `VC_redist.x64.exe` | 14.51.36247.0 | Microsoft | `843068991daaa1f73ad9f6239bce4d0f6a07a51f18c37ea2a867e9beca71295c` |
| `msodbcsql18-x64.msi` | 18.6.2.1 | Microsoft | `20314529110da3365a252164a657bdc837a18be5839105aa5f5acf0a8d2f4b82` |

Running `launcher\安装依赖.bat` installs these prerequisites only when they are missing. Installation of Microsoft ODBC Driver 18 accepts the Microsoft ODBC license terms via the documented `IACCEPTMSODBCSQLLICENSETERMS=YES` MSI property.

The installers retain their publishers' licenses. They are not part of the public application source license and are intended only for approved internal deployment.
