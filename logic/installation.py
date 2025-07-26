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
                error_msg = f"Installer file not found: {self.path_to_winrar_installer}"
                self.error_occurred.emit(error_msg)
                raise FileNotFoundError(error_msg)

            result = run([self.path_to_winrar_installer, "/S"], shell=True, check=True)
        except CalledProcessError as e:
            error_msg = f"Installation failed with exit code {e.returncode}"
            self.error_occurred.emit(error_msg)
            raise
        except Exception as e:
            error_msg = f"Installation error: {str(e)}"
            self.error_occurred.emit(error_msg)
            raise


def launch_winrar():
    try:
        path_to_winrar_executable = "C:\\Program Files\\WinRAR\\WinRAR.exe"
        if p.exists(path_to_winrar_executable):
            subprocess.Popen(path_to_winrar_executable)
        else:
            error_msg = "WinRAR executable not found!"
            raise FileNotFoundError(error_msg)
    except Exception as e:
        error_msg = f"Error launching WinRAR: {str(e)}"
        raise
