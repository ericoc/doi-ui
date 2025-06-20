from .config import CACHE_CONFIG
from flask_caching import Cache


cache = Cache(config=CACHE_CONFIG)
