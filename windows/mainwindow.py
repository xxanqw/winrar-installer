import sys
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QCheckBox,
    QMessageBox,
    QFrame,
    QGridLayout,
    QGroupBox,
)
from PySide6.QtGui import QPixmap, QAction, QFont
from PySide6.QtCore import Qt
from logic import (
    Downloader,
    InstallerThread,
    get_versions,
    launch_winrar,
    get_languages,
    get_lastmod,
    get_lang_dict,
)
from .about import AboutWindow
from os import path as p, remove
import tempfile
import shutil
from webbrowser import open
from typing import Literal

window_location = p.dirname(p.abspath(__file__))


def qt_exception_hook(exctype, value, traceback):
    from PySide6.QtWidgets import QApplication, QMessageBox

    app = QApplication.instance()
    if app is not None:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Application Error")
        msg.setText(f"{exctype.__name__}: {value}")
        msg.setDetailedText(
            "".join(__import__("traceback").format_exception(exctype, value, traceback))
        )
        msg.exec()
    else:
        print(f"{exctype.__name__}: {value}")
        import traceback as tb

        tb.print_exception(exctype, value, traceback)


sys.excepthook = qt_exception_hook


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(420, 340)
        self.setWindowTitle("WinRAR Installer")
        try:
            self.lang_dict = get_lang_dict()
        except Exception as e:
            raise RuntimeError("Failed to load language dictionary. Cannot continue.")

        import requests

        self.config = None
        try:
            response = requests.get(
                "https://fs.xserv.pp.ua/winrar/config.json", timeout=10
            )
            if response.status_code == 200:
                self.config = response.json()
        except requests.RequestException as e:
            self.message("Error", f"Failed to load remote configuration: {e}", "error")
        if self.config is None:
            raise RuntimeError("Failed to load remote configuration. Cannot continue.")
        self.setup_toolbar()
        self.beta = False
        self.lastmod = get_lastmod()
        self.setup_ui()
        self.show()

    def setup_toolbar(self):
        self.toolbar = self.addToolBar("Toolbar")
        self.toolbar.setMovable(False)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.about_action = QAction("About", self)
        self.about_action.setShortcut("Ctrl+I")
        self.toolbar.addAction(self.about_action)
        self.github_action = QAction("GitHub", self)
        self.github_action.setShortcut("Ctrl+G")
        self.toolbar.addAction(self.github_action)
        self.about_action.triggered.connect(self.open_about_window)
        self.github_action.triggered.connect(
            lambda: open("https://github.com/xxanqw/winrar-installer")
        )

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(20, 15, 20, 20)
        header_frame = self.create_header_section()
        main_layout.addWidget(header_frame)
        config_frame = self.create_configuration_section()
        main_layout.addWidget(config_frame)
        install_frame = self.create_install_section()
        main_layout.addWidget(install_frame)
        main_layout.addStretch()

    def create_header_section(self):
        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        logo_label = QLabel()
        try:
            pixmap = QPixmap(window_location + "/rarcat-100x100.png")
            scaled_pixmap = pixmap.scaled(
                60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            logo_label.setPixmap(scaled_pixmap)
        except:
            logo_label.setText("🗜️")
            font = QFont()
            font.setPointSize(32)
            logo_label.setFont(font)
        logo_label.setAlignment(Qt.AlignCenter)
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)
        title = QLabel("WinRAR Installer")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        description = QLabel("Modern installer with built-in activation")
        desc_font = QFont()
        desc_font.setPointSize(9)
        description.setFont(desc_font)
        text_layout.addWidget(title)
        text_layout.addWidget(description)
        text_layout.addStretch()
        layout.addWidget(logo_label)
        layout.addWidget(text_widget, 1)
        return frame

    def create_configuration_section(self):
        group_box = QGroupBox("Configuration")
        layout = QGridLayout(group_box)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 20, 15, 15)
        version_label = QLabel("Version:")
        self.verdropdown = QComboBox()
        self.verdropdown.setMinimumWidth(120)
        language_label = QLabel("Language:")
        self.langdropdown = QComboBox()
        self.langdropdown.setMinimumWidth(120)
        self.show_betas_checkbox = QCheckBox("Show Beta Versions")
        self.launch_checkbox = QCheckBox("Launch after installation")
        self.launch_checkbox.setChecked(True)
        checkbox_font = QFont()
        checkbox_font.setPointSize(9)
        self.show_betas_checkbox.setFont(checkbox_font)
        self.launch_checkbox.setFont(checkbox_font)
        layout.addWidget(version_label, 0, 0)
        layout.addWidget(self.verdropdown, 0, 1)
        layout.addWidget(language_label, 1, 0)
        layout.addWidget(self.langdropdown, 1, 1)
        options_layout = QHBoxLayout()
        options_layout.setSpacing(8)
        options_layout.addWidget(self.show_betas_checkbox)
        options_layout.addWidget(self.launch_checkbox)
        options_layout.addStretch()
        layout.addLayout(options_layout, 2, 0, 1, 2)
        self.versions = get_versions()
        for version in self.versions:
            self.verdropdown.addItem(version)
        languages = get_languages()
        for language in languages:
            self.langdropdown.addItem(language)
        self.verdropdown.currentIndexChanged.connect(self.on_version_changed)
        self.langdropdown.currentIndexChanged.connect(self.on_language_changed)
        self.show_betas_checkbox.stateChanged.connect(self.show_betas)
        return group_box

    def create_install_section(self):
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 8, 0, 0)
        self.install_button = QPushButton("Install WinRAR")
        self.install_button.setMinimumHeight(40)
        self.install_button.clicked.connect(self.install)
        layout.addWidget(self.install_button)
        return frame

    def on_language_changed(self):
        self.update_versions_for_language()

    def on_version_changed(self):
        pass

    def update_versions_for_language(self):
        language = self.langdropdown.currentText()
        if not language:
            return
        self.verdropdown.currentIndexChanged.disconnect()
        current_version = self.verdropdown.currentText()
        self.verdropdown.clear()
        available_versions = self.get_available_versions_for_language(language)
        for version in available_versions:
            self.verdropdown.addItem(version)
        if current_version in available_versions:
            self.verdropdown.setCurrentText(current_version)
        self.verdropdown.currentIndexChanged.connect(self.on_version_changed)

    def get_available_versions_for_language(self, language: str) -> list:
        available_versions = []
        try:
            if self.config and "releases" in self.config:
                release_type = "beta" if self.beta else "stable"
                releases = self.config["releases"][release_type]
                for release in releases:
                    version = release.get("version", "")
                    availability = release.get("availability", {})
                    if availability.get(language, False):
                        available_versions.append(version)
            if not available_versions:
                available_versions = get_versions(self.beta)
        except Exception as e:
            print(f"Error getting available versions for {language}: {e}")
            available_versions = get_versions(self.beta)
        return available_versions

    def open_about_window(self):
        about_window = AboutWindow(self, self.lastmod)
        about_window.exec()

    def install(self):
        if not self.install_button.isEnabled():
            return
        self.disable_ui()
        self.temp = tempfile.gettempdir()
        version = self.verdropdown.currentText()
        self.language = self.langdropdown.currentText()
        self.ver = version.replace(".", "")
        if not hasattr(self, "lang_dict") or self.lang_dict is None:
            self.lang = ""
        else:
            self.lang = self.lang_dict[self.language]
        try:
            if self.beta:
                url = f"https://www.rarlab.com/rar/winrar-x64-{self.ver}{self.lang}.exe"
            else:
                url = f"https://www.rarlab.com/rar/winrar-x64-{self.ver}{self.lang}.exe"
            self.downpath = f"{self.temp}\\winrar-x64-{self.ver}{self.lang}.exe"
            self.downloader = Downloader(url, self.downpath)
            self.downloader.error_occurred.connect(self.handle_download_error)
            self.downloader.finished.connect(self.install_part_two)
            self.downloader.start()
        except Exception as e:
            self.message("Error", f"An error occurred: {e}", "error")
            self.reenable()

    def handle_download_error(self, error_msg):
        self.message("Download Error", error_msg, "error")
        self.reenable()

    def install_part_two(self):
        path = f"{self.temp}\\winrar-x64-{self.ver}{self.lang}.exe"
        try:
            self.installer = InstallerThread(path)
            self.installer.error_occurred.connect(self.handle_install_error)
            self.installer.finished.connect(self.install_the_last_one)
            self.installer.start()
        except Exception as e:
            self.message("Error", f"An error occurred: {e}", "error")
            self.reenable()

    def handle_install_error(self, error_msg):
        self.message("Installation Error", error_msg, "error")
        self.reenable()

    def install_the_last_one(self):
        try:
            self.key_downloader = Downloader(
                "https://fs.xserv.pp.ua/files/rarreg.key", f"{self.temp}\\rarreg.key"
            )
            self.key_downloader.error_occurred.connect(self.handle_key_download_error)
            self.key_downloader.finished.connect(self.install_key)
            self.key_downloader.start()
        except Exception as e:
            self.message("Error", f"An error occurred: {e}", "error")
            self.reenable()

    def handle_key_download_error(self, error_msg):
        self.message("Key Download Error", error_msg, "error")
        self.reenable()

    def install_key(self):
        winrar_install_path = "C:\\Program Files\\WinRAR"
        key_path = f"{self.temp}\\rarreg.key"
        key_path_winrar = f"{winrar_install_path}\\rarreg.key"
        try:
            if p.exists(winrar_install_path):
                if p.exists(key_path_winrar):
                    remove(key_path_winrar)
                shutil.move(key_path, winrar_install_path)
            else:
                raise FileNotFoundError(
                    "WinRAR installation path does not exist. Try reinstalling WinRAR."
                )
        except Exception as e:
            self.message("Error", f"An error occurred: {e}", "error")
            self.reenable()
            return
        if self.launch_checkbox.isChecked():
            print("| Launching WinRAR...")
            launch_winrar()
        self.cleanup()

    def cleanup(self):
        try:
            if hasattr(self, "downpath") and p.exists(self.downpath):
                remove(self.downpath)
        except FileNotFoundError:
            pass
        self.reenable()

    def disable_ui(self):
        self.install_button.setDisabled(True)
        self.langdropdown.setDisabled(True)
        self.verdropdown.setDisabled(True)
        self.launch_checkbox.setDisabled(True)
        self.show_betas_checkbox.setDisabled(True)
        self.install_button.setText("Installing...")

    def show_betas(self):
        self.langdropdown.currentIndexChanged.disconnect()
        self.verdropdown.currentIndexChanged.disconnect()
        if self.show_betas_checkbox.isChecked():
            self.beta = True
            self.langdropdown.clear()
            beta_languages = self.get_beta_available_languages()
            for language in beta_languages:
                self.langdropdown.addItem(language)
            if self.langdropdown.count() > 0:
                if self.langdropdown.currentText():
                    selected_language = self.langdropdown.currentText()
                else:
                    selected_language = (
                        beta_languages[0] if beta_languages else "English"
                    )
                    self.langdropdown.setCurrentText(selected_language)
                self.verdropdown.clear()
                available_versions = self.get_available_versions_for_language(
                    selected_language
                )
                for version in available_versions:
                    self.verdropdown.addItem(version)
        else:
            self.beta = False
            self.langdropdown.clear()
            languages = get_languages()
            for language in languages:
                self.langdropdown.addItem(language)
            if self.langdropdown.count() > 0:
                if self.langdropdown.currentText():
                    selected_language = self.langdropdown.currentText()
                else:
                    selected_language = languages[0] if languages else "English"
                    self.langdropdown.setCurrentText(selected_language)
                self.verdropdown.clear()
                available_versions = self.get_available_versions_for_language(
                    selected_language
                )
                for version in available_versions:
                    self.verdropdown.addItem(version)
        self.langdropdown.currentIndexChanged.connect(self.on_language_changed)
        self.verdropdown.currentIndexChanged.connect(self.on_version_changed)

    def get_beta_available_languages(self) -> list:
        if not self.config or "releases" not in self.config:
            raise RuntimeError("Beta languages unavailable: config not loaded.")
        available_languages = set()
        for release in self.config["releases"]["beta"]:
            if release.get("supported", False):
                availability = release.get("availability", {})
                for lang, is_available in availability.items():
                    if is_available:
                        available_languages.add(lang)
        return sorted(list(available_languages))

    def message(self, title, text, type: Literal["info", "warning", "error"]):
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
        self.install_button.setText("Install WinRAR")
        self.message(
            "Installation completed", "WinRAR has been installed successfully.", "info"
        )
