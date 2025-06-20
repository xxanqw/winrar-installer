from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QIcon
from windows import MainWindow
from logic import APP_VERSION
import platform
import os.path as p
import sys

# from elevate import elevate
# elevate()


def run_gui():
    window_location = p.dirname(p.abspath(__file__))
    print("Welcome to WinRAR Installer")
    app = QApplication([])
    app.setStyle("Fusion")
    app.setApplicationName("WinRAR Installer")
    app.setApplicationDisplayName("WinRAR Installer")
    app.setApplicationVersion(APP_VERSION)
    app.setWindowIcon(QIcon(window_location + "/windows/rarcat.png"))

    window = MainWindow()
    app.exec()


def main():

    if platform.system() != "Windows":
        error_message = "This application is only supported on Windows."
        QMessageBox.critical(None, "Error", error_message)
        sys.exit(1)

    arch, _ = platform.architecture()
    if arch != "64bit":
        error_message = "This application supports only 64-bit Windows."
        QMessageBox.critical(None, "Error", error_message)
        sys.exit(1)

    run_gui()


if __name__ == "__main__":
    main()
