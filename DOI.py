"""
Digital Object Identifier (DOI).
https://www.doi.org/
"""
from re import compile as re_compile
from requests import get


USER_AGENT = "DOI JSON Search / nano.upenn.edu v0.1"
DOI_HEADERS = {"Accept": "application/json", "User-Agent": USER_AGENT}
DOI_REGEX = re_compile(r'(doi\:)?(10[.][0-9]{4,}[^\s"\/<>]*\/[^\s"<>]+)')
DOI_TIMEOUT = 3
DOI_URL = "https://doi.org"


class DOI:
    """A DOI is a digital identifier of an object, any object -
    physical, digital, or abstract. DOIs solve a common problem:
    keeping track of things. Things can be matter, material, content, or
    activities. Designed to be used by humans as well as machines,
    DOIs identify objects persistently. They allow things to be uniquely
    identified and accessed reliably. You know what you have, where it is,
    and others can track it too."""

    doi: str = ""
    _data: dict = {}
    author: (list, dict) = []
    authors: (list, dict) = []
    title: str = ""


    # Validate format of a given DOI.
    def __init__(self, doi: str = '', _gather: bool = True):
        doi_match = DOI_REGEX.match(doi)
        if not doi_match:
            raise ValueError('Invalid DOI format.')

        # Gather DOI data, if valid format.
        self.doi = doi
        if _gather is True:
            self._data = self.__gather()

            # Fill in attributes of the Python DOI object.
            if self._data:

                # Set authors, and determine primary/"first" author.
                self.authors = self._data.get("author")
                if self.authors:
                    for author in self.authors:
                        if author.get("sequence") != "additional":
                            self.author.append(author)

                # Single dictionary for one primary ("first") author.
                if len(self.author) == 1:
                    self.author = self.author[0]

                # Set title and URL on the Python object.
                self.title = self._data.get("title")
                self.url = self._data.get("URL")

                # Delete data dictionary, when done with it.
                del self._data


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()}"

    def __str__(self) -> str:
        msg = self.doi
        if self.title:
            msg += f' ({self.title})'
        return msg

    # Gather (JSON) information about the DOI.
    def __gather(self) -> dict:
        try:
            return get(
                headers=DOI_HEADERS,
                url=f'{DOI_URL}/{self.doi}',
                timeout=DOI_TIMEOUT
            ).json()
        except Exception as doi_exc:
            raise RuntimeError(f'Exception gathering {self.doi}.') from doi_exc
