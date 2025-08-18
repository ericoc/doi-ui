from functools import cached_property


class DOIReference:
    """
    Digital Object Identifier (DOI) Reference.
        Always has a key, but may or may not include much more.
    """
    _data: dict = {}
    key: str = ""
    doi: str = ""
    article_title: str = ""
    author: str = ""
    doi_asserted_by: str = ""
    first_page: str = ""
    journal_title: str = ""
    referenced_doi: str = ""
    series_title: str = ""
    unstructured: str = ""
    volume: str = ""
    volume_title: str = ""
    year: str = ""

    def __init__(self, doi, reference: dict):
        """Initialization of a DOI reference."""
        self._data = reference
        self.key = self._data["key"]
        self.doi = doi
        self.article_title = self._data.get("article-title", "")
        self.author = self._data.get("author", "")
        self.doi_asserted_by = self._data.get("doi-asserted-by", "")
        self.first_page = self._data.get("first-page", "")
        self.journal_title = self._data.get("journal-title", "")
        self.referenced_doi = self._data.get("DOI", "")
        self.series_title = self._data.get("series-title", "")
        self.unstructured = self._data.get("unstructured", "")
        self.volume = self._data.get("volume", "")
        self.volume_title = self._data.get("volume-title", "")
        self.year = self._data.get("year", "")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} @ {self.doi}"

    def __str__(self) -> str:
        return str(self._data)

    @cached_property
    def anchor(self) -> str:
        """HTML anchor to the reference. Example: #reference-ref5-cit5 """
        return self.key.replace(" ", "-").replace("_", "-").replace("/", "-")
