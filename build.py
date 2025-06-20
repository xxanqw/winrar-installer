import os
import argparse
from logic import APP_VERSION
import sys

version_sliced = APP_VERSION.split(".")
# Build Configuration
VERSION = (int(version_sliced[0]), int(version_sliced[1]), int(version_sliced[2]), int(version_sliced[3]))
VERSION_STR = ".".join(map(str, VERSION))
COMPANY_NAME = "xxanqw"
PRODUCT_NAME = "WinRar Installer"
FILE_DESCRIPTION = "WinRar Installer dammit"
COPYRIGHT = "2024 xxanqw"

def create_version_file():
    """Create a version_info.py file for PyInstaller"""
    version_info = f'''# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers={VERSION},
    prodvers={VERSION},
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x40004,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'{COMPANY_NAME}'),
        StringStruct(u'FileDescription', u'{FILE_DESCRIPTION}'),
        StringStruct(u'ProductName', u'{PRODUCT_NAME}'),
        StringStruct(u'ProductVersion', u'{VERSION_STR}'),
        StringStruct(u'LegalCopyright', u'{COPYRIGHT}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)'''
    with open("version_info.txt", "w") as f:
        f.write(version_info)
    return "version_info.txt"

def create_admin_manifest():
    """Create manifest file for admin privileges"""
    manifest = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel level="requireAdministrator" uiAccess="false"/>
      </requestedPrivileges>
    </security>
  </trustInfo>
</assembly>'''
    with open("admin.manifest", "w") as f:
        f.write(manifest)
    return "admin.manifest"

def sign_exe(exe_path, pfx_path, password):
    """Sign the executable using a PFX certificate"""
    cmd = (
        f'signtool sign /f "{pfx_path}" /p "{password}" '
        f'/tr http://timestamp.digicert.com /td sha256 /fd sha256 "{exe_path}"'
    )
    result = os.system(cmd)
    if result != 0:
        print("Error: Signing the executable failed")
        return False
    return True

def build_with_pyinstaller(console=False, sign=False):
    """Build the application using PyInstaller"""
    version_file = create_version_file()
    manifest_file = create_admin_manifest()
    
    # Build GUI version (no console) using app_gui.py
    gui_cmd = (
        f'pyinstaller --onefile --noconsole '
        f'--icon=windows/rarcat.png '
        f'--add-data "windows/rarcat.png;windows" '
        f'--add-data "windows/rarcat-100x100.png;windows" '
        f'--version-file={version_file} '
        f'--manifest={manifest_file} '
        f'--uac-admin '
        f'--name winrar-installer '
        f'app_gui.py'
    )
    
    # Build CLI version (with console) using app_cli.py
    cli_cmd = (
        f'pyinstaller --onefile --console '
        f'--icon=windows/rarcat.png '
        f'--add-data "windows/rarcat.png;windows" '
        f'--add-data "windows/rarcat-100x100.png;windows" '
        f'--version-file={version_file} '
        f'--manifest={manifest_file} '
        f'--uac-admin '
        f'--name winrar-installer-cli '
        f'app_cli.py'
    )
    
    print("Building GUI version (no console)...")
    os.system(gui_cmd)
    
    print("Building CLI version (with console)...")
    os.system(cli_cmd)
    
    if sign:
        gui_exe = os.path.join('dist', 'winrar-installer.exe')
        cli_exe = os.path.join('dist', 'winrar-installer-cli.exe')
        pfx_path = 'certificate.pfx'
        password = ''
        
        print("Signing GUI executable...")
        if sign_exe(gui_exe, pfx_path, password):
            print("GUI executable signed successfully.")
        else:
            print("Failed to sign GUI executable.")
            
        print("Signing CLI executable...")
        if sign_exe(cli_exe, pfx_path, password):
            print("CLI executable signed successfully.")
        else:
            print("Failed to sign CLI executable.")
    
    print("\nBuild completed!")
    print("Generated files:")
    print("  - winrar-installer.exe (GUI version, no console)")
    print("  - winrar-installer-cli.exe (CLI version, with console)")
    print("\nUsage:")
    print("  - GUI: winrar-installer.exe")
    print("  - CLI: winrar-installer-cli.exe --install --version 7.11")

def main():
    parser = argparse.ArgumentParser(description='Build WinRAR Installer')
    parser.add_argument('-p', '--pyinstaller', action='store_true', help='Build with PyInstaller')
    parser.add_argument('-c', '--console', action='store_true', help='Enable console')
    parser.add_argument('-s', '--sign', action='store_true', help='Sign the executable')
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(1)

    if args.pyinstaller:
        print(f"Building with PyInstaller ({'with' if args.console else 'no'} console{' and signing' if args.sign else ''})")
        build_with_pyinstaller(console=args.console, sign=args.sign)
        cleanup(console=args.console)
    else:
        print("No valid build option selected.")
        parser.print_help()
        sys.exit(1)

def cleanup(console=False):
    """Clean up temporary build files"""
    files_to_remove = [
        "version_info.txt",
        "admin.manifest",
        "winrar-installer.spec",
        "winrar-installer-cli.spec"
    ]
    
    for file in files_to_remove:
        try:
            if os.path.exists(file):
                os.remove(file)
                print(f"Removed {file}")
        except Exception as e:
            print(f"Could not remove {file}: {e}")

if __name__ == "__main__":
    main()