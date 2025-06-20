from PySide6.QtCore import QThread, Signal
import requests
import os


class Downloader(QThread):
    progress = Signal(int)
    error_occurred = Signal(str)

    def __init__(self, url, save_path):
        super().__init__()
        self.url = url
        self.save_path = save_path

    def run(self):
        try:
            if os.path.exists(self.save_path):
                os.remove(self.save_path)

            response = requests.get(self.url, stream=True, timeout=30)

            if response.status_code == 200:
                total_size = int(response.headers.get("content-length", 0))
                downloaded = 0

                with open(self.save_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                            downloaded += len(chunk)

                            if total_size > 0:
                                progress_percent = int((downloaded / total_size) * 100)
                                self.progress.emit(progress_percent)

                print("| Download completed!")
            else:
                error_msg = f"Failed to download file. HTTP {response.status_code}"
                print(f"| {error_msg}")
                self.error_occurred.emit(error_msg)

        except requests.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            print(f"| {error_msg}")
            self.error_occurred.emit(error_msg)
        except Exception as e:
            error_msg = f"Download error: {str(e)}"
            print(f"| {error_msg}")
            self.error_occurred.emit(error_msg)
