import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton

class PathChooser:
    def __init__(self):
        self.file_dialog = QFileDialog()
        self.file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        self.file_dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)

    def choose_path(self):
        if self.file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_path = self.file_dialog.selectedFiles()[0] + "/WinRar"
            selected_path = selected_path.replace("/", "\\")
            selected_path = selected_path.replace("\\\\", "\\")
            return selected_path