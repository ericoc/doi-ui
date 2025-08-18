class DOIReference:
    """
    Digital Object Identifier (DOI) Reference.
        always has a key, but may or may not include much more.
    """
    doi = ""
    key = ""
    article_title = ""
    author = ""
    doi_asserted_by = ""
    first_page = ""
    journal_title = ""
    referenced_doi = ""
    series_title = ""
    unstructured = ""
    volume = ""
    volume_title = ""
    year = ""

    def __init__(self, doi = "", reference = None):
        # Initialization of a DOI reference.
        self.doi = doi
        _data = reference or {}
        if _data:
            self.key = _data["key"]
            self.article_title = _data.get("article-title", "")
            self.author = _data.get("author", "")
            self.doi_asserted_by = _data.get("doi-asserted-by", "")
            self.first_page = _data.get("first-page", "")
            self.journal_title = _data.get("journal-title", "")
            self.referenced_doi = _data.get("DOI", "")
            self.series_title = _data.get("series-title", "")
            self.unstructured = _data.get("unstructured", "")
            self.volume = _data.get("volume", "")
            self.volume_title = _data.get("volume-title", "")
            self.year = _data.get("year", "")

    @property
    def anchor(self) -> str:
        # URL anchor.
        return self.key.replace(" ", "-").replace("_", "-").replace("/", "-")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()}"

    def __str__(self) -> str:
        return f"{self.key} (@ {self.doi})"
