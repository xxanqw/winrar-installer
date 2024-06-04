import sys
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
from os import path as p

window_location = p.dirname(p.abspath(__file__))

class AboutWindow(QDialog):
    def __init__(self):
        super().__init__()
        version = "1.0.1"
        build = "27"
        self.setWindowTitle("About")
        self.setFixedSize(300, 300)
        self.setWindowIcon(QIcon(window_location + "/xxanqw.jpg"))

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image = QLabel()
        image.setPixmap(QPixmap(window_location + "/xxanqw.jpg"))
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(image)
        label = QLabel("Made by xxanqw in 2024\nWritten on Python with PyQt6")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        version = QLabel(f"Version {version} (build {build})\n\n{sys.platform}")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)


        
        self.setLayout(layout)