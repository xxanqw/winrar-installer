from PyQt6.QtWidgets import QApplication, QMessageBox
from windows import MainWindow
import platform

# Uncomment the following lines to run the application with elevated privileges
# Only if running from a script
# from elevate import elevate
# elevate()

if platform.system() == 'Windows':
    print("Welcome to WinRar Installer")
    app = QApplication([])
    window = MainWindow()
    app.exec()
else:
    error_message = "This application is only supported on Windows."
    QMessageBox.critical(None, "Error", error_message)

