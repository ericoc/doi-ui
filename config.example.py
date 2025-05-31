from re import compile
SECRET_KEY = "secret123"
USER_AGENT = "DOI JSON Search / nano.upenn.edu v0.1"
DOI_HEADERS = {"Accept": "application/json", "User-Agent": USER_AGENT}
DOI_REGEX = compile(r'(doi\:)?(10[.][0-9]{4,}[^\s"\/<>]*\/[^\s"<>]+)')
DOI_TIMEOUT = 3
DOI_URL = "https://doi.org"
