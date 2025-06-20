<p align="center">
    <img src="https://cdn.xserv.pp.ua/images/github/winrar-installer/winrar.png" alt="Extra simple WinRar Installer"/>
</p>

<h1 align="center">Simple WinRAR Installer</h1>


## 🚀 Installation

### PowerShell (Recommended)

#### GUI Mode (Default)
Run this command in your PowerShell terminal:

```powershell
irm https://shorty.pp.ua/winrar | iex
```

#### CLI Mode with Parameters
For automated installations and advanced usage:

```powershell
# Install latest English version
iex "& {$(irm https://shorty.pp.ua/winrar)} -Install"

# Install specific version and language
iex "& {$(irm https://shorty.pp.ua/winrar)} -Install -Version '7.11' -Language 'Ukrainian'"

# Install beta version without launching
iex "& {$(irm https://shorty.pp.ua/winrar)} -Install -Beta -NoLaunch"

# List available versions
iex "& {$(irm https://shorty.pp.ua/winrar)} -ListVersions"

# List available languages
iex "& {$(irm https://shorty.pp.ua/winrar)} -ListLanguages"

# Show help
iex "& {$(irm https://shorty.pp.ua/winrar)} -Help"
```

#### PowerShell Parameters
| Parameter | Description | Example |
|-----------|-------------|---------|
| `-Install` | Install WinRAR | `-Install` |
| `-Version` | Specify version | `-Version '7.11'` |
| `-Language` | Specify language (default: English) | `-Language 'Russian'` |
| `-Beta` | Use beta versions | `-Beta` |
| `-NoLaunch` | Don't launch after install | `-NoLaunch` |
| `-ListVersions` | Show available versions | `-ListVersions` |
| `-ListLanguages` | Show available languages | `-ListLanguages` |
| `-GUI` | Force GUI mode | `-GUI` |
| `-Help` | Show help information | `-Help` |

### Traditional

- **GUI Version**: Download `winrar-installer.exe` from [Releases](https://github.com/xxanqw/winrar-installer/releases/latest)
- **CLI Version**: Download `winrar-installer-cli.exe` from [Releases](https://github.com/xxanqw/winrar-installer/releases/latest)
- Or use direct links:
  - [GUI Version](https://github.com/xxanqw/winrar-installer/releases/latest/download/winrar-installer.exe) (No console window)
  - [CLI Version](https://github.com/xxanqw/winrar-installer/releases/latest/download/winrar-installer-cli.exe) (Console support)


## 🖥️ Usage (GUI)

<p align="center">
    <img src="https://github.com/user-attachments/assets/05352e90-1aff-4015-858c-aea48bb7c76f" alt="Showcase" width="600"/>
</p>


## ⚡ Usage (CLI)

The CLI version provides a colorful, emoji-enhanced command-line experience with full console support.

| Command             | Description                         | Example                                                                 |
|---------------------|-------------------------------------|-------------------------------------------------------------------------|
| `--install`         | Install WinRAR                      | `winrar-installer-cli.exe --install`                                   |
| `--version <ver>`   | Specify WinRAR version to install   | `winrar-installer-cli.exe --install --version 7.11`                    |
| `--language <lang>` | Specify language (default: English) | `winrar-installer-cli.exe --install --language Ukrainian`              |
| `--beta`            | Use beta versions                   | `winrar-installer-cli.exe --install --beta`                            |
| `--no-launch`       | Do not launch WinRAR after install  | `winrar-installer-cli.exe --install --no-launch`                       |
| `--list-versions`   | List all available versions         | `winrar-installer-cli.exe --list-versions`                             |
| `--list-languages`  | List all available languages        | `winrar-installer-cli.exe --list-languages`                            |

**Examples:**

```bash
# Install latest English version
winrar-installer-cli.exe --install

# Install specific version and language
winrar-installer-cli.exe --install --version 7.11 --language Ukrainian

# List all available versions
winrar-installer-cli.exe --list-versions

# List all available languages
winrar-installer-cli.exe --list-languages

# Install beta version without launching
winrar-installer-cli.exe --install --beta --version 7.12b1 --no-launch
```

## 🛠️ Building from Source

> **Note**  
> Requires **Python 3.9+** (project set up for 3.13.3 by default).  
> [UV](https://docs.astral.sh/uv/getting-started/installation/) is needed for dependency management and running scripts.

### 1. Clone the Repository

```bash
git clone https://github.com/xxanqw/winrar-installer.git
cd winrar-installer
```

### 2. Install Dependencies

```bash
uv sync --all-extras
```

### 3. Build the Executable

The build system now creates **two separate executables** optimized for their specific use cases:

- **Basic Build (both GUI and CLI versions):**
    ```bash
    uv run build.py -p
    ```

- **Build and Sign Both Executables:**
    ```bash
    uv run build.py -p -s
    ```

#### 📦 Build Output

| File | Purpose | Console | Description |
|------|---------|---------|-------------|
| `winrar-installer.exe` | GUI | No | Clean GUI experience, no console window |
| `winrar-installer-cli.exe` | CLI | Yes | Full console support with colors and emojis |

> [!NOTE] 
> - Signed builds require a `certificate.pfx` file in the project root  
> - Output `.exe` files will be in the `dist/` folder  
> - Both executables include version info, admin manifest, and bundled resources

