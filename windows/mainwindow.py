from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QCheckBox, QFormLayout, QHBoxLayout
from PySide6.QtGui import QPixmap, QAction
from PySide6.QtCore import Qt
from logic import Downloader, InstallerThread, get_versions, launch_winrar, get_languages, get_lastmod, get_lang_dict
from .about import AboutWindow
from os import path as p, remove
import tempfile
import shutil
from PySide6.QtWidgets import QMessageBox
from webbrowser import open
from typing import Literal

window_location = p.dirname(p.abspath(__file__))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(450, 400)
        self.lang_dict = get_lang_dict()

        self.toolbar = self.addToolBar("Toolbar")
        self.toolbar.setMovable(False)

        self.about_action = QAction("About", self)
        self.about_action.setShortcut("Ctrl+I")
        self.toolbar.addAction(self.about_action)
        self.github_action = QAction("GitHub", self)
        self.github_action.setShortcut("Ctrl+G")
        self.toolbar.addAction(self.github_action)

        self.about_action.triggered.connect(self.open_about_window)
        self.github_action.triggered.connect(lambda: open("https://github.com/xxanqw/winrar-installer"))

        self.another_title_layout = QHBoxLayout()
        self.title_layout = QVBoxLayout()
        self.title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignLeft)
        self.title_layout.setSpacing(10)
        self.another_title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image = QLabel()
        self.image.setPixmap(QPixmap(window_location + "/rarcat-100x100.png"))
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignRight)
        self.another_title_layout.addWidget(self.image)
        self.title = QLabel("Welcome to WinRar Installer")
        self.title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.description = QLabel("This is a simple installer for WinRar.\nAlready with activation key.")
        self.description.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.title_layout.addWidget(self.title)
        self.title_layout.addWidget(self.description)
        self.another_title_layout.addLayout(self.title_layout)

        self.options_layout = QFormLayout()
        self.options_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.langdropdown = QComboBox()
        self.langdropdown.setFixedWidth(120)
        languages = get_languages()
        for language in languages:
            self.langdropdown.addItem(language)
        self.langdropdown.currentIndexChanged.connect(self.version_change)
        self.options_layout.addRow("Language:", self.langdropdown)

        self.verdropdown = QComboBox()
        self.verdropdown.setFixedWidth(120)
        self.versions = get_versions()
        for version in self.versions:
            self.verdropdown.addItem(version)
        self.options_layout.addRow("Version:", self.verdropdown)

        self.show_betas_checkbox = QCheckBox("Show Betas")
        self.show_betas_checkbox.stateChanged.connect(self.show_betas)
        self.options_layout.addRow(self.show_betas_checkbox)

        self.launch_checkbox = QCheckBox("Launch after installation")
        self.launch_checkbox.setChecked(True)
        self.options_layout.addRow(self.launch_checkbox)

        self.lastmod = get_lastmod()

        self.install_layout = QVBoxLayout()
        self.install_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.install_layout.addLayout(self.options_layout)
        self.install_button = QPushButton("Install")
        self.install_button.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.install_button.setFixedHeight(40)
        self.install_button.clicked.connect(self.install)
        self.install_layout.addWidget(self.install_button)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.another_title_layout)
        self.layout.addLayout(self.install_layout)

        self.beta = False
        self.specific_lang = False

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.layout)
        self.show()

    def open_about_window(self):
        about_window = AboutWindow(self, self.lastmod)
        about_window.exec()

    def install(self):
        self.install_button.setDisabled(True)
        self.langdropdown.setDisabled(True)
        self.verdropdown.setDisabled(True)
        self.launch_checkbox.setDisabled(True)
        self.show_betas_checkbox.setDisabled(True)
        self.install_button.setText("Installing...")

        self.temp = tempfile.gettempdir()
        version = self.verdropdown.currentText()
        self.language = self.langdropdown.currentText()
        self.ver = version.replace(".", "")
        
        self.lang = self.lang_dict[self.langdropdown.currentText()]
        try:
            if self.beta:
                print("| Using beta link. (rarlab.com)")
                url = f"https://www.rarlab.com/rar/winrar-x64-{self.ver}{self.lang}.exe"
            else:
                print("(rarlab.com)")
                url = f"https://www.rarlab.com/rar/winrar-x64-{self.ver}{self.lang}.exe"
            self.downpath = f"{self.temp}\\winrar-x64-{self.ver}{self.lang}.exe"
            self.downloader = Downloader(url, self.downpath)
            self.downloader.start()
            lines = [
                ("Downloading WinRar...", ""),
                ("Version:", version),
                ("Language:", self.language),
                ("URL:", url),
                ("Temp:", self.temp),
            ]

            line_contents = [f"| {label} {value}" for label, value in lines]

            for line in line_contents:
                print(f"{line}{' '}")
        except Exception as e:
            self.message("Error", f"An error occurred: {e}", "error")
            self.reenable()
            return
            
        self.downloader.finished.connect(self.install_part_two)

    def install_part_two(self):
        path = f"{self.temp}\\winrar-x64-{self.ver}{self.lang}.exe"
        try:
            self.installer = InstallerThread(path)
            self.installer.start()
        except Exception as e:
            self.message("Error", f"An error occurred: {e}", "error")
            self.reenable()
            return
        self.installer.finished.connect(self.install_the_last_one)


    def install_the_last_one(self):
        try:
            self.downloader = Downloader("https://fs.xserv.pp.ua/files/rarreg.key", f"{self.temp}\\rarreg.key")
            self.downloader.start()
        except Exception as e:
            self.message("Error", f"An error occurred: {e}", "error")
            self.reenable()
            return
        self.downloader.finished.connect(self.install_key)
        
    def install_key(self):
        winrar_install_path = "C:\\Program Files\\WinRAR"  # Шлях до папки інсталяції WinRar
        key_path = f"{self.temp}\\rarreg.key"
        key_path_winrar = f"{winrar_install_path}\\rarreg.key"
        
        try:
            if p.exists(winrar_install_path):
                if p.exists(key_path_winrar):
                    remove(key_path_winrar)
                shutil.move(key_path, winrar_install_path)
                print(f"| rarreg.key moved to {winrar_install_path} successfully.")
            else:
                print("| WinRar installation folder not found.")
        except Exception as e:
            self.message("Error", f"An error occurred: {e}", "error")
            self.reenable()
            return
        
        if self.launch_checkbox.isChecked():
            print("| Launching WinRar...")
            launch_winrar()
            
        self.cleanup()
        
    def cleanup(self):
        try:
            remove(self.downpath)
        except FileNotFoundError:
            pass
        
        self.reenable()

    def show_betas(self):
        if self.show_betas_checkbox.isChecked():
            self.beta = True
            self.verdropdown.clear()
            versions = get_versions(True)
            for version in versions:
                self.verdropdown.addItem(version)
            self.langdropdown.clear()
            self.langdropdown.addItem("English")
            self.langdropdown.addItem("Russian")
            self.langdropdown.addItem("Chinese Traditional")
            self.langdropdown.addItem("German")
            self.langdropdown.addItem("Indonesian")
            self.langdropdown.addItem("Portuguese")
            self.langdropdown.addItem("Portuguese Brazilian")
            self.langdropdown.addItem("Swedish")
        else:
            self.verdropdown.clear()
            versions = get_versions()
            for version in versions:
                self.verdropdown.addItem(version)
            self.langdropdown.clear()
            languages = get_languages()
            for language in languages:
                self.langdropdown.addItem(language)
            self.beta = False

    def version_change(self):
        if not self.beta:
            lang = self.lang_dict[self.langdropdown.currentText()]
            if lang == 'az' or self.lang == 'he' or self.lang == 'srbcyr':
                self.verdropdown.clear()
                vers = self.versions[2:]
                for version in vers:
                    self.verdropdown.addItem(version)
                self.specific_lang = True
            elif self.specific_lang:
                self.verdropdown.clear()
                for version in self.versions:
                    self.verdropdown.addItem(version)
                self.specific_lang = False

    def message(self, title, text, type: Literal['info', 'warning', 'error']):
        message = QMessageBox()
        if type == "info":
            message.setIcon(QMessageBox.Icon.Information)
        elif type == "warning":
            message.setIcon(QMessageBox.Icon.Warning)
        elif type == "error":
            message.setIcon(QMessageBox.Icon.Critical)
        message.setWindowTitle(title)
        message.setText(text)
        message.exec()

    def reenable(self):
        self.install_button.setDisabled(False)
        self.langdropdown.setDisabled(False)
        self.verdropdown.setDisabled(False)
        self.launch_checkbox.setDisabled(False)
        self.show_betas_checkbox.setDisabled(False)
        self.install_button.setText("Install")
        print("| Installation completed!")
        self.message("Installation completed", "WinRar has been installed successfully.", "info")