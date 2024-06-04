import sys
from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import QApplication
from subprocess import run
import subprocess

class InstallerThread(QThread):
    def __init__(self, path_to_winrar_installer):
        super().__init__()
        self.path_to_winrar_installer = path_to_winrar_installer

    def run(self):
        run([self.path_to_winrar_installer, '/S'], shell=True, check=True)
        print("Installation completed!")

def launch_winrar(self, arch):
    if arch == "x32":
        path_to_winrar_executable = "C:\\Program Files (x86)\\WinRAR\\WinRAR.exe"
    elif arch == "x64":
        path_to_winrar_executable = "C:\\Program Files\\WinRAR\\WinRAR.exe"
        
    subprocess.Popen(path_to_winrar_executable)