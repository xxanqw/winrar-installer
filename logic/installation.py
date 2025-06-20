from PySide6.QtCore import QThread, Signal
from subprocess import run, CalledProcessError
import subprocess
from os import path as p


class InstallerThread(QThread):
    error_occurred = Signal(str)

    def __init__(self, path_to_winrar_installer):
        super().__init__()
        self.path_to_winrar_installer = path_to_winrar_installer

    def run(self):
        try:
            if not p.exists(self.path_to_winrar_installer):
                self.error_occurred.emit(
                    f"Installer file not found: {self.path_to_winrar_installer}"
                )
                return

            result = run([self.path_to_winrar_installer, "/S"], shell=True, check=True)
            print("| Installation completed!")
        except CalledProcessError as e:
            error_msg = f"Installation failed with exit code {e.returncode}"
            print(f"| {error_msg}")
            self.error_occurred.emit(error_msg)
        except Exception as e:
            error_msg = f"Installation error: {str(e)}"
            print(f"| {error_msg}")
            self.error_occurred.emit(error_msg)


def launch_winrar():
    try:
        path_to_winrar_executable = "C:\\Program Files\\WinRAR\\WinRAR.exe"
        if p.exists(path_to_winrar_executable):
            subprocess.Popen(path_to_winrar_executable)
            print("| WinRAR launched successfully!")
        else:
            print("| WinRAR executable not found!")
    except Exception as e:
        print(f"| Failed to launch WinRAR: {e}")
