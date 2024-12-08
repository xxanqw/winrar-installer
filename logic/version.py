import requests

APP_VERSION = "0.1.1.1"

url = "https://fs.xserv.pp.ua/files/winrar.json"
response = requests.get(url)

def get_versions(beta=False):
    if response.status_code == 200:
        if beta:
            versions = response.json()
            version_list = versions["betas"]
        else:
            versions = response.json()
            version_list = versions["versions"]

        return version_list

def get_languages():
    if response.status_code == 200:
        languages = response.json()
        language_list = languages["languages"]

        return language_list

def get_lang_dict():
    if response.status_code == 200:
        lang_dict = response.json()
        lang_dict = lang_dict["lang_dict"]

        return lang_dict

def get_lastmod():
    if response.status_code == 200:
        lastmod = response.json()
        lastmod_date = lastmod["datemodified"]

        return lastmod_date