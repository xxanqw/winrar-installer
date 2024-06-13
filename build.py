import os
import sys


def main():
    parameters = sys.argv[1:]
        
    if "-v" in parameters:
        print("Build with console enabled")
        os.system("nuitka --onefile --follow-imports --enable-plugin=pyqt6 -o winrar-installer-debug --output-dir=build --windows-uac-admin --windows-icon-from-ico=./windows/rarcat.png --include-data-files=./windows/rarcat.png=windows/rarcat.png --include-data-files=./windows/rarcat-100x100.png=windows/rarcat-100x100.png --deployment --company-name=xxanqw --product-name=\"WinRar Installer (With Console)\" --product-version=0.1.0.4 --file-description=\"WinRar Installer dammit\" --copyright=\"©️2024 xxanqw\" app.py")
    else:
        print("Build with console disabled (default)")
        os.system("nuitka --onefile --follow-imports --enable-plugin=pyqt6 -o winrar-installer --output-dir=build --windows-uac-admin --windows-icon-from-ico=./windows/rarcat.png --include-data-files=./windows/rarcat.png=windows/rarcat.png --include-data-files=./windows/rarcat-100x100.png=windows/rarcat-100x100.png --disable-console --deployment --company-name=xxanqw --product-name=\"WinRar Installer\" --product-version=0.1.0.4 --file-description=\"WinRar Installer dammit\" --copyright=\"©️2024 xxanqw\" app.py")
    
if __name__ == "__main__":
    main()