from PyQt6.QtCore import QThread
import requests

class Downloader(QThread):
    def __init__(self, url, save_path):
        super().__init__()
        self.url = url
        self.save_path = save_path

    def run(self):
        # Implement your download logic here
        # For example, you can use the requests library to download the file

        response = requests.get(self.url)
        if response.status_code == 200:
            with open(self.save_path, 'wb') as file:
                file.write(response.content)
                print("Download completed!")
        else:
            print("Failed to download file.")