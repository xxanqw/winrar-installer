import os
import argparse
from logic import APP_VERSION

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

def build_with_pyinstaller(console=False):
    """Build the application using PyInstaller"""
    version_file = create_version_file()
    manifest_file = create_admin_manifest()
    cmd = (f'pyinstaller --onefile {"--console" if console else "--noconsole"} '
           f'--icon=windows/rarcat.png '
           f'--add-data "windows/rarcat.png;windows" '
           f'--add-data "windows/rarcat-100x100.png;windows" '
           f'--version-file={version_file} '
           f'--manifest={manifest_file} '
           f'--uac-admin '
           f'--name winrar-installer{'-debug' if console else ''} '
           f'app.py')
    os.system(cmd)

def main():
    parser = argparse.ArgumentParser(description='Build WinRAR Installer')
    parser.add_argument('-p', '--pyinstaller', action='store_true', help='Build with PyInstaller')
    parser.add_argument('-c', '--console', action='store_true', help='Enable console')
    args = parser.parse_args()

    if args.pyinstaller:
        print(f"Building with PyInstaller ({'with' if args.console else 'no'} console)")
        build_with_pyinstaller(console=args.console)
        cleanup(console=args.console)

def cleanup(console):
    os.remove("version_info.txt")
    os.remove("admin.manifest")
    os.remove(f"winrar-installer{'-debug' if console else ''}.spec")

if __name__ == "__main__":
    main()
    print("Build complete!!!!!!!!!💕😘❤️❤️❤️")