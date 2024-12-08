from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QIcon
from windows import MainWindow
from logic import APP_VERSION
import platform
import os.path as p

""" 
Uncomment the following lines to run the application with elevated privileges
Only if running from a script
↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
"""
# from elevate import elevate
# elevate()

version = APP_VERSION
version = version.lstrip('0.')

if platform.system() == 'Windows':
    window_location = p.dirname(p.abspath(__file__))
    print("Welcome to WinRar Installer")
    app = QApplication([])
    app.setStyle("Fusion")
    app.setApplicationName("WinRar Installer")
    app.setApplicationDisplayName("WinRar Installer")
    app.setApplicationVersion(version)
    app.setWindowIcon(QIcon(window_location + "/windows/rarcat.png"))

    window = MainWindow()
    app.exec()
else:
    error_message = "This application is only supported on Windows."
    QMessageBox.critical(None, "Error", error_message)
