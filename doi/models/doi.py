"""
Digital Object Identifier (DOI).
https://www.doi.org/
"""
from datetime import date, datetime
from json import dumps as json_dumps

from .author import DOIAuthor
from .funder import DOIFunder
from .reference import DOIReference
from ..parsers import parse_date


class DOI:
    """
    A Digital Object Identifier (DOI) is a digital identifier of an object,
    any object - physical, digital, or abstract. DOIs solve a common problem:
    keeping track of things. Things can be matter, material, content, or
    activities. Designed to be used by humans as well as machines,
    DOIs identify objects persistently. They allow things to be uniquely
    identified and accessed reliably. You know what you have, where it is,
    and others can track it too.
    """

    doi: str = ""
    _data: dict = {}

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
    def __init__(self, doi: str, _data: dict):
        self.doi = doi
        self.abstract = _data.get("abstract", self.abstract)
        self.authors = _data.get("author", self.authors)
        self.publisher = _data.get("publisher", self.publisher)
        self.referenced_by_count = _data.get(
            "is-referenced-by-count", self.referenced_by_count
        )
        self.reference_count = _data.get(
            "reference-count", self.reference_count
        )
        self.type = _data.get("type", self.type)
        self.url = _data.get("URL", self.url)
        self.title = _data.get("title", self.title)

        # Set authors list attribute.
        self.authors = []
        for author in _data.get("author", []):
            author_obj = DOIAuthor(doi=self.doi, author=author)
            # TODO: Check ORCID.
            self.authors.append(author_obj)

            # If any author is Penn-related, DOI is Penn-related.
            if author_obj.is_penn:
                self.is_penn = True

        # Set funders list.
        self.funders = []
        for funder in _data.get("funder", []):
            funder_obj = DOIFunder(doi=self.doi, funder=funder)
            self.funders.append(funder_obj)

        # Set references list.
        self.references = []
        for reference in _data.get("reference", []):
            reference_obj = DOIReference(doi=self.doi, reference=reference)
            self.references.append(reference_obj)

        # Set date attributes.
        self.created = parse_date(_data.get("created"))
        self.deposited = parse_date(_data.get("deposited"))
        self.indexed = parse_date(_data.get("indexed"))
        self.issued = parse_date(_data.get("issued"))
        self.published = parse_date(_data.get("published"))
        self.published_online = parse_date(_data.get("published-online"))
        self.published_print = parse_date(_data.get("published-print"))

        # Format JSON and delete data dictionary.
        self.json =  json_dumps(_data, indent=2)
        del _data

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: {self.__str__()}'

    def __str__(self) -> str:
        msg = self.doi
        if self.title:
            msg += f'. {self.title}'
        if self.is_penn:
            msg += ' [Penn]'
        return msg
