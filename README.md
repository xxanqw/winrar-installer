![# Extra simple WinRar Installer](https://cdn.xserv.pp.ua/images/github/winrar-installer/winrar.png)

<div align="center">
    
## Installation

</div>

### PowerShell
Execute this in your PowerShell terminal and you good to go
```bash
irm https://shorty.pp.ua/winrar | iex
```
### Traditional
Go to the latest release and download .exe yourself  
Or press on this [blue](https://github.com/xxanqw/winrar-installer/releases/latest/download/winrar-installer.exe) text to download latest

<div align="center">
    
## Showcase

![Showcase](https://github.com/user-attachments/assets/05352e90-1aff-4015-858c-aea48bb7c76f)

</div>

<div align="center">

## Building

</div>

If you're on PowerShell just copy code below
```bash
# Clone repo
git clone https://github.com/xxanqw/winrar-installer.git
cd winrar-installer
# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
# Install requirements and build
pip install -r req
python build.py -p
```
Also make sure that Python and git is installed on your system
