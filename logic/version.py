import requests
from typing import Optional, Dict, List
import time

APP_VERSION = "0.1.1.3"


class VersionManager:
    def __init__(self):
        self.url = "https://fs.xserv.pp.ua/winrar/config.json"
        self._cache = None
        self._cache_time = 0
        self._cache_duration = 300

    def _fetch_data(self) -> Optional[Dict]:
        current_time = time.time()
        if self._cache and (current_time - self._cache_time) < self._cache_duration:
            return self._cache
        try:
            response = requests.get(self.url, timeout=10)
            if response.status_code == 200:
                self._cache = response.json()
                self._cache_time = current_time
                return self._cache
        except requests.RequestException as e:
            print(f"Error fetching version data: {e}")
            return self._cache
        return None

    def _extract_version_number(self, version_obj) -> str:
        if isinstance(version_obj, dict):
            return version_obj.get("version", "")
        return str(version_obj)

    def get_versions(self, beta=False) -> List[str]:
        data = self._fetch_data()
        if not data:
            return ["7.11", "7.10", "7.01", "7.00", "6.24"]
        if "releases" in data:
            releases_key = "beta" if beta else "stable"
            releases = data["releases"].get(releases_key, [])
            versions = [self._extract_version_number(release) for release in releases]
            return versions
        key = "betas" if beta else "versions"
        return data.get(key, [])

    def get_languages(self) -> List[str]:
        data = self._fetch_data()
        if not data:
            return ["English"]
        if "localization" in data:
            languages = data["localization"].get("supported_languages", [])
            return [lang["name"] for lang in languages]
        return data.get("languages", [])

    def get_lang_dict(self) -> Dict[str, str]:
        data = self._fetch_data()
        if not data:
            return {"English": ""}
        if "localization" in data:
            languages = data["localization"].get("supported_languages", [])
            return {lang["name"]: lang["code"] for lang in languages}
        return data.get("lang_dict", {})

    def get_lastmod(self) -> str:
        data = self._fetch_data()
        if not data:
            return "Unknown"
        if "metadata" in data:
            return data["metadata"].get("last_updated", "Unknown")
        return data.get("datemodified", "Unknown")

    def get_download_config(self) -> Dict:
        data = self._fetch_data()
        if not data:
            return {
                "base_url": "https://www.rarlab.com/rar/",
                "filename_pattern": "winrar-x64-{version}{lang_code}.exe",
                "activation_key_url": "https://fs.xserv.pp.ua/files/rarreg.key",
            }
        return data.get("download_config", {})

    def get_supported_languages_since_version(self, min_version: str) -> List[str]:
        data = self._fetch_data()
        if not data or "localization" not in data:
            return self.get_languages()
        languages = data["localization"].get("supported_languages", [])
        return [
            lang["name"]
            for lang in languages
            if self._version_compare(lang.get("supported_since", "1.0.0"), min_version)
            >= 0
        ]

    def _version_compare(self, v1: str, v2: str) -> int:
        def version_tuple(v):
            return tuple(map(int, v.split(".")))

        try:
            v1_tuple = version_tuple(v1)
            v2_tuple = version_tuple(v2)
            if v1_tuple < v2_tuple:
                return -1
            elif v1_tuple > v2_tuple:
                return 1
            else:
                return 0
        except (ValueError, AttributeError):
            return 0


_version_manager = VersionManager()


def get_versions(beta=False):
    return _version_manager.get_versions(beta)


def get_languages():
    return _version_manager.get_languages()


def get_lang_dict():
    return _version_manager.get_lang_dict()


def get_lastmod():
    return _version_manager.get_lastmod()


def get_download_config():
    return _version_manager.get_download_config()


def check_file_availability(url: str) -> bool:
    try:
        response = requests.head(url, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False
