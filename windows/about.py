import sys
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt
from os import path as p
from logic import APP_VERSION

window_location = p.dirname(p.abspath(__file__))

class AboutWindow(QDialog):
    def __init__(self, parent, lastmod):
        super().__init__()
        version = APP_VERSION
        version = version.lstrip('0.')
        self.setWindowTitle("About")
        self.setFixedSize(300, 150)
        self.setWindowIcon(QIcon(window_location + "/rarcat.png"))
        self.parent = parent

        app_name_layout = QVBoxLayout()
        app_img = QLabel()
        app_img.setPixmap(QPixmap(window_location + "/rarcat-100x100.png"))
        app_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_name_layout.addWidget(app_img)
        app_name = QLabel("WinRar Installer")
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_name.setStyleSheet("font-weight: bold;")
        app_name_layout.addWidget(app_name)

        description_layout = QVBoxLayout()
        description = QLabel("Made by xxanqw 🐈\nWritten on Python with PySide6")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_layout.addWidget(description)
        version = QLabel(f"Version {version}\nVerlist {lastmod}")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_layout.addWidget(version)

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(app_name_layout)
        layout.addLayout(description_layout)

        self.setLayout(layout)