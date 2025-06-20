from pathlib import Path
DEBUG = False
CACHE_CONFIG = {
    # "CACHE_TYPE": "NullCache",
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_DIR": Path(Path.home(), "cache"),
    "CACHE_THRESHOLD": 500
}
SECRET_KEY = "xxx"
ORCID_API_CLIENT_ID = "APP-xxx"
ORCID_API_CLIENT_SECRET = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
