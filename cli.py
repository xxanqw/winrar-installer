import argparse
import tempfile
import requests
import subprocess
import shutil
import os
import os.path as p
from colorama import init, Fore, Back, Style
from logic import APP_VERSION, get_versions, get_languages, get_lang_dict, launch_winrar

init(autoreset=True)


def create_argument_parser():
    parser = argparse.ArgumentParser(
        description="🗜️  WinRAR Installer - Install WinRAR with built-in activation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  winrar-installer.exe                           # 🖥️  Launch GUI
  winrar-installer.exe --cli                     # 📋 Show available commands
  winrar-installer.exe --cli --install           # 🚀 Install latest English version
  winrar-installer.exe --cli --install --version 7.11 --language Ukrainian
  winrar-installer.exe --cli --list-versions     # 📋 List all available versions
  winrar-installer.exe --cli --list-languages    # 🌍 List all available languages
  winrar-installer.exe --cli --beta              # 🧪 Show beta versions
        """,
    )

    parser.add_argument("--cli", action="store_true", help="Run in command line mode")
    parser.add_argument(
        "--install", action="store_true", help="Install WinRAR (CLI mode only)"
    )
    parser.add_argument(
        "--version", type=str, help="Specify WinRAR version to install (e.g., 7.11)"
    )
    parser.add_argument(
        "--language",
        type=str,
        default="English",
        help="Specify language (default: English)",
    )
    parser.add_argument("--beta", action="store_true", help="Use beta versions")
    parser.add_argument(
        "--no-launch",
        action="store_true",
        help="Do not launch WinRAR after installation",
    )
    parser.add_argument(
        "--list-versions", action="store_true", help="List all available versions"
    )
    parser.add_argument(
        "--list-languages", action="store_true", help="List all available languages"
    )

    return parser


def run_cli(args):
    print(f"{Fore.CYAN}🗜️  WinRAR Installer CLI v{APP_VERSION}")
    print(f"{Fore.CYAN}{'=' * 45}")

    if args.list_versions:
        print(f"{Fore.YELLOW}📋 Available versions:")
        versions = get_versions(args.beta)
        for version in versions:
            print(f"  {Fore.GREEN}✓ {version}")
        return

    if args.list_languages:
        print(f"{Fore.YELLOW}🌍 Available languages:")
        languages = get_languages()
        for language in languages:
            print(f"  {Fore.GREEN}✓ {language}")
        return

    if not args.install:
        print(f"{Fore.YELLOW}💡 Available commands:")
        print(f"  {Fore.CYAN}--install           {Fore.WHITE}Install WinRAR")
        print(f"  {Fore.CYAN}--list-versions     {Fore.WHITE}List available versions")
        print(f"  {Fore.CYAN}--list-languages    {Fore.WHITE}List available languages")
        print(f"\n{Fore.MAGENTA}💭 Use --help for more details")
        return

    versions = get_versions(args.beta)
    languages = get_languages()

    version = args.version or versions[0]
    if version not in versions:
        print(f"{Fore.RED}❌ Error: Version '{version}' not available")
        print(f"{Fore.YELLOW}📋 Available versions: {', '.join(versions)}")
        return

    if args.language not in languages:
        print(f"{Fore.RED}❌ Error: Language '{args.language}' not available")
        print(f"{Fore.YELLOW}🌍 Available languages: {', '.join(languages)}")
        return

    print(
        f"{Fore.GREEN}🚀 Installing WinRAR {Fore.YELLOW}{version} {Fore.GREEN}({Fore.CYAN}{args.language}{Fore.GREEN})"
    )
    print(f"{Fore.YELLOW}⏰ This may take a few minutes...")

    lang_dict = get_lang_dict()
    lang_code = lang_dict.get(args.language, "")
    ver_clean = version.replace(".", "")

    if args.beta:
        url = f"https://www.rarlab.com/rar/winrar-x64-{ver_clean}{lang_code}.exe"
    else:
        url = f"https://www.rarlab.com/rar/winrar-x64-{ver_clean}{lang_code}.exe"

    temp_dir = tempfile.gettempdir()
    download_path = f"{temp_dir}\\winrar-x64-{ver_clean}{lang_code}.exe"

    print(f"{Fore.BLUE}📥 Downloading WinRAR...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0

        with open(download_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        bar_length = 30
                        filled_length = int(bar_length * progress // 100)
                        bar = "█" * filled_length + "░" * (bar_length - filled_length)
                        print(
                            f"\r{Fore.CYAN}📊 Progress: {Fore.YELLOW}[{bar}] {progress:.1f}%",
                            end="",
                            flush=True,
                        )

        print(f"\n{Fore.GREEN}✅ Download completed!")

    except requests.RequestException as e:
        print(f"\n{Fore.RED}❌ Error downloading WinRAR: {e}")
        return

    print(f"{Fore.BLUE}⚙️  Installing WinRAR...")
    try:
        result = subprocess.run([download_path, "/S"], check=True, capture_output=True)
        print(f"{Fore.GREEN}✅ WinRAR installation completed!")

    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}❌ Error installing WinRAR: {e}")
        return

    print(f"{Fore.BLUE}🔑 Downloading activation key...")
    try:
        key_url = "https://fs.xserv.pp.ua/files/rarreg.key"
        key_path = f"{temp_dir}\\rarreg.key"

        response = requests.get(key_url)
        response.raise_for_status()

        with open(key_path, "wb") as f:
            f.write(response.content)

        winrar_path = "C:\\Program Files\\WinRAR"
        if p.exists(winrar_path):
            key_dest = f"{winrar_path}\\rarreg.key"
            if p.exists(key_dest):
                os.remove(key_dest)
            shutil.move(key_path, winrar_path)
            print(f"{Fore.GREEN}✅ Activation key installed!")
        else:
            print(f"{Fore.YELLOW}⚠️  Warning: WinRAR installation directory not found")

    except Exception as e:
        print(f"{Fore.RED}❌ Error installing activation key: {e}")

    try:
        if p.exists(download_path):
            os.remove(download_path)
            print(f"{Fore.BLUE}🧹 Temporary files cleaned up")
    except:
        pass

    if not args.no_launch:
        print(f"{Fore.BLUE}🚀 Launching WinRAR...")
        try:
            launch_winrar()
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️  Could not launch WinRAR: {e}")

    print(f"{Fore.GREEN}{Style.BRIGHT}🎉 Installation completed successfully!")
