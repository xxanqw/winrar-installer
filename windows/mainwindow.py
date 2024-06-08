from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QCheckBox
from PyQt6.QtGui import QPixmap, QAction, QIcon
from PyQt6.QtCore import Qt
from logic import Downloader, InstallerThread, get_versions, launch_winrar, get_languages, get_lastmod
from .about import AboutWindow
from os import path as p
import tempfile
import requests
from PyQt6.QtWidgets import QMessageBox

window_location = p.dirname(p.abspath(__file__))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WinRar Installer")
        self.setFixedSize(600, 400)
        self.setWindowIcon(QIcon(window_location + "/xxanqw.jpg"))

        self.toolbar = self.addToolBar("Toolbar")
        self.toolbar.setMovable(False)

        self.open_action = QAction("About", self)
        self.open_action.setShortcut("Ctrl+I")
        self.toolbar.addAction(self.open_action)

        self.open_action.triggered.connect(self.open_about_window)

        self.title_layout = QVBoxLayout()
        self.title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.image = QLabel()
        self.image.setPixmap(QPixmap(window_location + "/xxanqw.jpg"))
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_layout.addWidget(self.image)
        self.title = QLabel("Welcome to WinRar Installer")
        self.title.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.description = QLabel("This is a simple installer for WinRar.\nAlready with activation key.")
        self.description.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.title_layout.addWidget(self.title)
        self.title_layout.addWidget(self.description)


        self.chooser_layout = QHBoxLayout()
        self.chooser_label = QLabel("Language:")
        self.chooser_layout.addWidget(self.chooser_label)
        self.langdropdown = QComboBox()
        self.langdropdown.setFixedWidth(120)
        languages = get_languages()
        for language in languages:
            self.langdropdown.addItem(language)
        self.chooser_layout.addWidget(self.langdropdown)
        self.verchooser_label = QLabel("Version:")
        self.chooser_layout.addWidget(self.verchooser_label)
        self.verdropdown = QComboBox()
        self.verdropdown.setFixedWidth(55)
        versions = get_versions()
        for version in versions:
            self.verdropdown.addItem(version)
        self.chooser_layout.addWidget(self.verdropdown)
        self.arch_choose_label = QLabel("Architecture:")
        self.chooser_layout.addWidget(self.arch_choose_label)
        self.archdropdown = QComboBox()
        self.archdropdown.addItem("x64")
        self.archdropdown.addItem("x32")
        self.chooser_layout.addWidget(self.archdropdown)
        self.launch_checkbox = QCheckBox("Launch after installation")
        self.launch_checkbox.setChecked(True)
        self.chooser_layout.addWidget(self.launch_checkbox)

        self.lastmod = get_lastmod()

        self.install_layout = QVBoxLayout()
        self.install_layout.addLayout(self.chooser_layout)
        self.install_button = QPushButton("Install")
        self.install_button.clicked.connect(self.install)
        self.install_layout.addWidget(self.install_button)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.title_layout)
        self.layout.addLayout(self.install_layout)


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
        self.archdropdown.setDisabled(True)

        self.temp = tempfile.gettempdir()
        version = self.verdropdown.currentText()
        self.arch = self.archdropdown.currentText()
        self.lang = self.langdropdown.currentText()
        self.ver = version.replace(".", "")
        if self.lang == "English":
            self.lang = ""
        elif self.lang == "Ukrainian":
            self.lang = "uk"
        url = f"https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-{self.arch}-{self.ver}{self.lang}.exe"
        downpath = f"{self.temp}\\winrar-{self.arch}-{self.ver}{self.lang}.exe"
        self.downloader = Downloader(url, downpath)
        self.downloader.start()
        print("Downloading WinRar...")
        print("Version:", version)
        print("Architecture:", self.arch)
        print("Language:", self.lang)
        print("URL:", url)
        print("Temp:", self.temp)
        self.downloader.finished.connect(self.install_part_two)

    def install_part_two(self):
        path = f"{self.temp}\\winrar-{self.arch}-{self.ver}{self.lang}.exe"
        self.installer = InstallerThread(path)
        self.installer.start()
        self.installer.finished.connect(self.install_the_last_one)


    def install_the_last_one(self):
        key_url = "https://fs.xserv.pp.ua/files/rarreg.key"
        if self.arch == "x64":
            key_path = "C:/Program Files/WinRar/rarreg.key"
        elif self.arch == "x32":
            key_path = "C:/Program Files (x86)/WinRar/rarreg.key"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        response = requests.get(key_url, headers=headers)

        with open(key_path, 'wb') as f:
            f.write(response.content)

        print("rarreg.key downloaded successfully.")
        if self.launch_checkbox.isChecked():
            print("Launching WinRar...")
            launch_winrar(self.arch)
            
        self.reenable()

    def reenable(self):
        self.install_button.setDisabled(False)
        self.langdropdown.setDisabled(False)
        self.verdropdown.setDisabled(False)
        self.archdropdown.setDisabled(False)
        print("Installation completed!")
        info_message = QMessageBox()
        info_message.setIcon(QMessageBox.Icon.Information)
        info_message.setWindowTitle("Installation Completed")
        info_message.setText("WinRar installation completed successfully!")
        info_message.setWindowIcon(QIcon(window_location + "/xxanqw.jpg"))
        info_message.exec()