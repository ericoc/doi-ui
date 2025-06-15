"""
Digital Object Identifier (DOI).
https://www.doi.org/
"""
import json
from datetime import date, datetime
from re import compile
from requests import get


DOI_HEADERS = {
    "Accept": "application/json",
    "User-Agent": "DOI JSON Search / nano.upenn.edu v0.1"
}
DOI_REGEX = compile(r'(doi\:)?(10[.][0-9]{4,}[^\s"\/<>]*\/[^\s"<>]+)')
DOI_URL = "https://doi.org"


def _parse_date(item: (dict, None)) -> (date, datetime, None):
    # Parse "date-time" and "date-parts" chunks from DOI JSON.
    if item:
        iso_dt = item.get("date-time")
        if iso_dt:
            try:
                return datetime.fromisoformat(iso_dt)
            except ValueError:
                pass

        date_parts = item.get("date-parts")
        if date_parts:
            p_date = date_parts[0]
            if p_date:
                if len(p_date) == 3:
                    return date(p_date[0], p_date[1], p_date[2])
                elif len(p_date) == 2:
                    return date(p_date[0], p_date[1], 1)
                elif len(p_date) == 1 and p_date[0] is not None:
                    return date(p_date[0], 1, 1)
        return item

    return None


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
        doi_match = DOI_REGEX.match(doi)
        if not doi_match:
            raise ValueError

        # Gather DOI data, by default.
        self.doi = doi
        if _gather:
            self._data = self.__gather()

            # Fill in attributes of the Python DOI object, using JSON data.
            if self._data:
                self.abstract = self._data.get("abstract", self.abstract)
                self.abstract = self._data.get("abstract", self.abstract)
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
                    for _author in author_data:
                        self.authors.append(
                            self.DOIAuthor(doi=self, author=_author)
                        )
                del author_data

                # Set date attributes.
                created = self._data.get("created")
                if created:
                    self.created = _parse_date(created)

                deposited = self._data.get("deposited")
                if deposited:
                    self.deposited = _parse_date(deposited)

                indexed = self._data.get("indexed")
                if indexed:
                    self.indexed = _parse_date(indexed)

                issued = self._data.get("issued")
                if issued:
                    self.issued = _parse_date(issued)

                published = self._data.get("published")
                if published:
                    self.published = _parse_date(published)

                published_online = self._data.get("published-online")
                if published_online:
                    self.published_online = _parse_date(published_online)

                published_print = self._data.get("published-print")
                if published_print:
                    self.published_print = _parse_date(published_print)

                # Format JSON and delete data dictionary.
                self.json =  json.dumps(self._data, indent=2)
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
                headers=DOI_HEADERS,
                url=f'{DOI_URL}/{self.doi}',
                timeout=self._timeout
            )
            if resp.status_code != 200:
                raise FileNotFoundError
            return resp.json()

        except Exception as doi_exc:
            raise doi_exc


    class DOIAuthor:
        """Author of a DOI can include specific affiliation(s), ORCID, etc."""

        doi: str = ""
        given: str = ""
        family: str = ""
        name: str = ""
        sequence: str = ""
        affiliation: list = []
        orcid: str = ""
        is_penn_affiliated: bool = False

        # Initialization of a DOI author.
        def __init__(self, doi, author: dict = {}):
            self.doi = doi
            self.orcid = author.get("ORCID", self.orcid)
            self.sequence = author.get("sequence", self.sequence)
            self.given = author.get("given", self.given)
            self.family = author.get("family", self.family)
            self.name = f'{self.given} {self.family}'

            # Check if the author is affiliated with Penn.
            self.affiliation = author.get("affiliation", self.affiliation)
            if self.affiliation:
                uni = "University of Pennsylvania"
                self.is_penn_affiliated = self._is_affiliation(uni)

        def _is_affiliation(self, test: str = ""):
            # Check for the test string in each affiliation name.
            if test:
                for _affiliation in self.affiliation:
                    if test in _affiliation.get("name", ""):
                        return True
            return False

        def __repr__(self) -> str:
            return f'{self.__class__.__name__}: {self.__str__()}'

        def __str__(self) -> str:
            msg = f'{self.name}'
            if self.orcid:
                msg += f' <{self.orcid}>'
            msg += f' ({self.sequence})'
            if self.is_penn_affiliated:
                msg += ' [Penn]'
            msg += f' @ {self.doi}'
            return msg
