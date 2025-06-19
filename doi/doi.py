"""
Digital Object Identifier (DOI).
https://www.doi.org/
"""
from datetime import date, datetime
from json import dumps as json_dumps
from re import compile as re_compile
from requests import get as requests_get

from .author import DOIAuthor
from .funder import DOIFunder
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

    doi: str = ""
    abstract: str = ""
    authors: list = []
    created: (date, datetime, None) = None
    deposited: (date, datetime, None) = None
    funders: list = []
    indexed: (date, datetime, None) = None
    issued: (date, datetime, None) = None
    is_penn: bool = False
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
                self.abstract = self._data.get("abstract", self.abstract)
                self.authors = self._data.get("author", self.authors)
                self.publisher = self._data.get("publisher", self.publisher)
                self.referenced_by_count = self._data.get(
                    "is-referenced-by-count", self.referenced_by_count
                )
                self.reference_count = self._data.get(
                    "reference-count", self.reference_count
                )
                self.references = self._data.get("reference", self.references)
                self.type = self._data.get("type", self.type)
                self.url = self._data.get("URL", self.url)
                self.title = self._data.get("title", self.title)

                # Set author(s).
                author_data = self._data.get("author")
                if author_data:
                    self.authors = []
                    for author in author_data:
                        author_obj = DOIAuthor(doi=self, author=author)
                        self.authors.append(author_obj)
                        if author_obj.is_penn:
                            self.is_penn = True
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

                # Set funders list attribute.
                self.funders = []
                funders = self._data.get("funder", self.funders)
                if funders:
                    for funder in funders:
                        funder_obj = DOIFunder(doi=self, funder=funder)
                        self.funders.append(funder_obj)

                # Format JSON and delete data dictionary.
                self.json =  json_dumps(self._data, indent=2)
                del self._data

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: {self.__str__()}'

    def __str__(self) -> str:
        msg = self.doi
        if self.title:
            msg += f'. {self.title}'
        if self.is_penn:
            msg += ' [Penn]'
        return msg

    # Gather (JSON) information about the DOI.
    def __gather(self) -> dict:
        try:
            resp = requests_get(
                headers={
                    "Accept": "application/json",
                    "User-Agent": "DOI Search / doi.ericoc.com v1.0"
                },
                url=f'https://doi.org/{self.doi}',
                timeout=3
            )
            if resp.status_code != 200:
                raise FileNotFoundError
            return resp.json()

        except Exception as doi_exc:
            raise doi_exc
