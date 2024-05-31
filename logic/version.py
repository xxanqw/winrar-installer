import requests

# URL of the JSON file
url = "https://fs.xserv.pp.ua/files/winrar.json"
response = requests.get(url)

def get_versions():
    if response.status_code == 200:
        versions = response.json()
        version_list = versions["versions"]
        print("Successfully retrieved versions from the JSON file.")

        return version_list
    else:
        print("Failed to retrieve versions from the JSON file.")