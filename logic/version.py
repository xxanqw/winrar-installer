import requests

url = "https://fs.xserv.pp.ua/files/winrar.json"
response = requests.get(url)

def get_versions():
    if response.status_code == 200:
        versions = response.json()
        version_list = versions["versions"]
        print("Successfully retrieved versions.")

        return version_list
    else:
        print("Failed to retrieve versions.")

def get_languages():
    if response.status_code == 200:
        languages = response.json()
        language_list = languages["languages"]
        print("Successfully retrieved languages.")

        return language_list
    else:
        print("Failed to retrieve languages.")

def get_lastmod():
    if response.status_code == 200:
        lastmod = response.json()
        lastmod_date = lastmod["datemodified"]
        print("Successfully retrieved last modified date.")

        return lastmod_date
    else:
        print("Failed to retrieve last modified date.")