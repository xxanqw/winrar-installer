import os
import sys


def main():
    parameters = sys.argv[1:]
        
    if "-v" in parameters:
        print("Build with console enabled")
        os.system("nuitka --onefile --follow-imports --enable-plugin=pyqt6 -o winrar-installer-debug --output-dir=build --windows-uac-admin --windows-icon-from-ico=./windows/xxanqw.jpg --include-data-files=./windows/xxanqw.jpg=windows/xxanqw.jpg --deployment --company-name=xxanqw --product-name=\"WinRar Installer (With Console)\" --product-version=0.1.0.3 app.py")
    else:
        print("Build with console disabled (default)")
        os.system("nuitka --onefile --follow-imports --enable-plugin=pyqt6 -o winrar-installer --output-dir=build --windows-uac-admin --windows-icon-from-ico=./windows/xxanqw.jpg --include-data-files=./windows/xxanqw.jpg=windows/xxanqw.jpg --disable-console --deployment --company-name=xxanqw --product-name=\"WinRar Installer\" --product-version=0.1.0.3 app.py")
    
if __name__ == "__main__":
    main()