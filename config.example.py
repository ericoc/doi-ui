from pathlib import Path
DEBUG = False
SECRET_KEY = "secret123"
CACHE_TYPE = "FileSystemCache"
CACHE_DEFAULT_TIMEOUT = 30
CACHE_DIR = Path(Path.home(), "cache")
