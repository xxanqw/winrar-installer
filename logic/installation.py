from PySide6.QtCore import QThread
from subprocess import run
import subprocess
from os import path as p

class InstallerThread(QThread):
    def __init__(self, path_to_winrar_installer):
        super().__init__()
        self.path_to_winrar_installer = path_to_winrar_installer

    def run(self):
        run([self.path_to_winrar_installer, '/S'], shell=True, check=True)
        print("| Installation completed!")

def launch_winrar():
    path_to_winrar_executable = "C:\\Program Files\\WinRAR\\WinRAR.exe"  
    subprocess.Popen(path_to_winrar_executable)