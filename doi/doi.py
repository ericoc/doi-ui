"""
Digital Object Identifier (DOI).
https://www.doi.org/
"""
from datetime import date, datetime
from json import dumps as json_dumps
from re import compile as re_compile
from requests import get

from .author import DOIAuthor
from .parsers import parse_date


DOI_REGEX = re_compile(r'(doi\:)?(10[.][0-9]{4,}[^\s"\/<>]*\/[^\s"<>]+)')


class DOI:
    """A Digital Object Identifier (DOI) is a digital identifier of an object,
    any object - physical, digital, or abstract. DOIs solve a common problem:
    keeping track of things. Things can be matter, material, content, or
    activities. Designed to be used by humans as well as machines,
    DOIs identify objects persistently. They allow things to be uniquely
    identified and accessed reliably. You know what you have, where it is,
    and others can track it too."""

    _data: dict = {}
    _timeout: int = 3

    doi: str = ""
    abstract: str = ""
    authors: list = []
    created: (date, datetime, None) = None
    deposited: (date, datetime, None) = None
    indexed: (date, datetime, None) = None
    issued: (date, datetime, None) = None
    json: str = ""
    published: (date, None) = None
    published_online: (date, None) = None
    published_print: (date, None) = None
    publisher: str = ""
    referenced_by_count: int = 0
    reference_count: int = 0
    references: list = []
    title: str = ""
    type: str = ""
    url: str = ""

    # Initialization of a Digital Object Identifier (DOI) Python object.
    def __init__(self, doi: str = '', _gather: bool = True):

        # Validate format of a given DOI.
        if not DOI_REGEX.match(doi):
            raise ValueError

        # Gather DOI data, by default.
        self.doi = doi
        if _gather:
            self._data = self.__gather()

            # Fill in attributes of the Python DOI object, using JSON data.
            if self._data:
                self.abstract = self._data.get("abstract")
                self.authors = self._data.get("author")
                self.publisher = self._data.get("publisher")
                self.referenced_by_count = self._data.get(
                    "is-referenced-by-count"
                )
                self.reference_count = self._data.get("reference-count")
                self.references = self._data.get("reference")
                self.type = self._data.get("type")
                self.url = self._data.get("URL")
                self.title = self._data.get("title")

                # Set author(s).
                author_data = self._data.get("author")
                if author_data:
                    self.authors = []
                    for author in author_data:
                        self.authors.append(DOIAuthor(doi=self, author=author))
                del author_data

                # Set date attributes.
                self.created = parse_date(self._data.get("created"))
                self.deposited = parse_date(self._data.get("deposited"))
                self.indexed = parse_date(self._data.get("indexed"))
                self.issued = parse_date(self._data.get("issued"))
                self.published = parse_date(self._data.get("published"))
                self.published_online = parse_date(
                    self._data.get("published-online")
                )
                self.published_print = parse_date(
                    self._data.get("published-print")
                )

                # Format JSON and delete data dictionary.
                self.json =  json_dumps(self._data, indent=2)
                del self._data

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: {self.__str__()}'

    def __str__(self) -> str:
        msg = self.doi
        if self.title:
            msg += f'. {self.title}'
        return msg

    # Gather (JSON) information about the DOI.
    def __gather(self) -> dict:
        try:
            resp = get(
                headers={
                    "Accept": "application/json",
                    "User-Agent": "DOI JSON Search / doi.ericoc.com v1.0"
                },
                url=f'https://doi.org/{self.doi}',
                timeout=self._timeout
            )
            if resp.status_code != 200:
                raise FileNotFoundError
            return resp.json()

        except Exception as doi_exc:
            raise doi_exc
