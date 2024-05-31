import sys
from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import QApplication
from subprocess import run

class InstallerThread(QThread):
    def __init__(self, path_to_winrar_installer):
        super().__init__()
        self.path_to_winrar_installer = path_to_winrar_installer

    def run(self):
        # Replace 'path_to_winrar_installer' with the actual path to the WinRAR installer
        run([self.path_to_winrar_installer, '/S'], shell=True, check=True)
        print("Installation completed!")