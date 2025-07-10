import re
import requests
from datetime import date, datetime
from django.conf import settings
from json import dumps as json_dumps
from orcid import PublicAPI

from .author import DOIAuthor
from .funder import DOIFunder
from .reference import DOIReference
from parsers import parse_date


"""Digital Object Identifier (DOI)."""
DOI_REGEX = re.compile(r'(doi\:)?(10[.][0-9]{4,}[^\s"\/<>]*\/[^\s"<>]+)')
class DOI:

    doi: str = ""

    abstract: str = ""
    authors: list = []
    created: (date, datetime, None) = None
    deposited: (date, datetime, None) = None
    funders: list = []
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
    def __init__(self, submitted_doi: str = ""):
        # Gather information about the DOI.
        self.gather(doi=submitted_doi)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()}"

    def __str__(self) -> str:
        msg = self.doi
        if self.title:
            msg += f". {self.title}"
        if self.is_penn():
            msg += " [Penn]"
        return msg

    def gather(self, doi: str):

        # Gather information from doi.org about the submitted DOI.
        resp = requests.get(
            headers=settings.REQUEST_HEADERS, timeout=settings.REQUEST_TIMEOUT,
            url=f"https://doi.org/{doi}"
        )

        # Raise exception for non-existent DOI.
        if resp.status_code != 200:
            raise FileNotFoundError("No such DOI was found!")

        # Fill in DOI object attributes using JSON response.
        data = resp.json()
        self.doi = data.get("DOI", self.doi)
        self.abstract = data.get("abstract", self.abstract)
        self.authors = data.get("author", self.authors)
        self.publisher = data.get("publisher", self.publisher)
        self.referenced_by_count = data.get(
            "is-referenced-by-count", self.referenced_by_count
        )
        self.reference_count = data.get("reference-count", self.reference_count)
        self.type = data.get("type", self.type)
        self.url = data.get("URL", self.url)
        self.title = data.get("title", self.title)

        # Set authors list attribute.
        orcid_conn = PublicAPI(
            institution_key=settings.ORCID_API_CLIENT_ID,
            institution_secret=settings.ORCID_API_CLIENT_SECRET
        )
        orcid_token = orcid_conn.get_search_token_from_orcid()
        orcid_api = (orcid_conn, orcid_token)
        self.authors = []
        for author in data.get("author", []):
            author_obj = DOIAuthor(
                doi=self.doi, author=author, orcid_api=orcid_api
            )
            self.authors.append(author_obj)

        # Set funders list.
        self.funders = []
        for funder in data.get("funder", []):
            funder_obj = DOIFunder(doi=self.doi, funder=funder)
            self.funders.append(funder_obj)

        # Set references list.
        self.references = []
        for reference in data.get("reference", []):
            reference_obj = DOIReference(doi=self.doi, reference=reference)
            self.references.append(reference_obj)

        # Set date attributes.
        self.created = parse_date(data.get("created"))
        self.deposited = parse_date(data.get("deposited"))
        self.indexed = parse_date(data.get("indexed"))
        self.issued = parse_date(data.get("issued"))
        self.published = parse_date(data.get("published"))
        self.published_online = parse_date(data.get("published-online"))
        self.published_print = parse_date(data.get("published-print"))

        # Format JSON and delete data dictionary.
        self.json =  json_dumps(data, indent=2)

    def is_penn(self) -> bool:
        # If any author is Penn-affiliated, so is the DOI.
        for author in self.authors:
            if author.is_penn:
                return True
        return False
