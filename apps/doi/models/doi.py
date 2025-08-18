import requests
from datetime import date, datetime
from django.conf import settings
from logging import getLogger
from html import unescape
from json import dumps as json_dumps
from orcid import PublicAPI
from re import compile as re_compile

from .author import DOIAuthor
from .funder import DOIFunder
from .reference import DOIReference
from parsers import parse_date


# Logging.
logger = getLogger(__name__)

# Compiled regular expression pattern for a DOI string.
DOI_REGEX = re_compile(r'(doi\:)?(10[.][0-9]{4,}[^\s"\/<>]*\/[^\s"<>]+)')


class DOI:
    """
    Digital Object Identifier (DOI).
    """
    doi: str = ""

    abstract: str = ""
    authors: list = []
    author_count: int = 0
    bibliography: str = ""
    bibtex: str = ""
    container_title: str = ""
    created: (date, datetime, None) = None
    deposited: (date, datetime, None) = None
    funders: list = []
    indexed: (date, datetime, None) = None
    issued: (date, datetime, None) = None
    json: str = ""
    member: str = ""
    published: (date, None) = None
    published_online: (date, None) = None
    published_print: (date, None) = None
    publisher: str = ""
    referenced_by_count: int = 0
    reference_count: int = 0
    references: list = []
    source: str = ""
    title: str = ""
    type: str = ""
    url: str = ""


    def __init__(self, _doi: str = "", check_orcids: bool = True):
        """Initialization of Digital Object Identifier (DOI) Python object."""

        # Immediately raise an exception if submitted DOI has invalid format.
        if not DOI_REGEX.match(_doi):
            raise NameError("Invalid DOI format.")

        # Gather and populate information about the DOI.
        self._populate(
            data=self._gather(doi=_doi),
            check_orcids=check_orcids
        )
        self.bibliography = self._gather_bibliography()
        self.bibtex = self._gather_bibtex()


    def _gather_bibliography(self) -> str:
        """Gather bibliography information from doi.org about the DOI."""
        settings.REQUEST_HEADERS["Accept"] = "text/x-bibliography"
        try:
            resp = requests.get(
                headers=settings.REQUEST_HEADERS,
                timeout=settings.REQUEST_TIMEOUT,
                url=f"https://doi.org/{self.doi}"
            )
            resp_text = resp.text.replace(
                f"https://doi.org/{self.doi}",
                ""
            ).strip()
            if resp_text:
                return resp_text

        except Exception as bibliography_exc:
            logger.exception(
                msg=f"Failed gathering bibliography. ({self.doi})",
                exc_info=bibliography_exc
            )

        return ""


    def _gather_bibtex(self) -> str:
        """Gather BibTeX information from doi.org about the DOI."""
        settings.REQUEST_HEADERS["Accept"] = "application/x-bibtex"
        try:
            resp = requests.get(
                headers=settings.REQUEST_HEADERS,
                timeout=settings.REQUEST_TIMEOUT,
                url=f"https://doi.org/{self.doi}"
            )
            resp_text = resp.text.strip()
            if resp_text:
                return resp_text
        except Exception as bibtex_exc:
            logger.exception(
                msg=f"Failed gathering BibTeX. ({self.doi})",
                exc_info=bibtex_exc
            )

        return ""


    def _gather(self, doi: str):
        """Gather JSON information from doi.org about the submitted DOI."""
        settings.REQUEST_HEADERS["Accept"] = "application/json"
        resp = requests.get(
            headers=settings.REQUEST_HEADERS,
            timeout=settings.REQUEST_TIMEOUT,
            url=f"https://doi.org/{doi}"
        )

        # Raise exception for non-existent DOI.
        if resp.status_code != 200:
            raise FileNotFoundError("No such DOI found.")

        # Convert response to JSON.
        try:
            return resp.json()
        except requests.exceptions.JSONDecodeError as json_err:
            msg = "Cannot decode response as JSON."
            logger.exception(f"{msg} ({doi})")
            raise ValueError(msg) from json_err


    def _populate(self, data, check_orcids: bool):
        """Fill in DOI object attributes using JSON response."""
        self.doi = data.get("DOI", self.doi)
        self.abstract = data.get("abstract", self.abstract)
        self.authors = data.get("author", self.authors)
        self.container_title = unescape(
            data.get("container-title", self.container_title)
        )
        self.member = data.get("member", self.member)
        self.publisher = data.get("publisher", self.publisher)
        self.referenced_by_count = data.get(
            "is-referenced-by-count", self.referenced_by_count
        )
        self.reference_count = data.get("reference-count", self.reference_count)
        self.source = data.get("source", self.source)
        self.type = data.get("type", self.type)
        self.url = data.get("URL", self.url)
        self.title = data.get("title", self.title)

        # Set up connection to ORCID API, by default.
        orcid_api = ()
        if check_orcids:
            orcid_conn = PublicAPI(
                institution_key=settings.ORCID_API_CLIENT_ID,
                institution_secret=settings.ORCID_API_CLIENT_SECRET
            )
            orcid_token = orcid_conn.get_search_token_from_orcid()
            orcid_api = (orcid_conn, orcid_token)

        # Create list of author objects, potentially using each authors ORCID.
        self.authors = []
        for author in data.get("author", []):
            author_obj = DOIAuthor(
                doi=self.doi, author=author, orcid_api=orcid_api
            )
            self.authors.append(author_obj)
        self.author_count = len(self.authors)

        # Create list of funder objects.
        self.funders = []
        for funder in data.get("funder", []):
            funder_obj = DOIFunder(doi=self.doi, funder=funder)
            if funder_obj:
                self.funders.append(funder_obj)

        # Create list of reference objects.
        self.references = []
        for reference in data.get("reference", []):
            reference_obj = DOIReference(doi=self.doi, reference=reference)
            if reference_obj:
                self.references.append(reference_obj)

        # Set date attributes.
        self.created = parse_date(data.get("created"))
        self.deposited = parse_date(data.get("deposited"))
        self.indexed = parse_date(data.get("indexed"))
        self.issued = parse_date(data.get("issued"))
        self.published = parse_date(data.get("published"))
        self.published_online = parse_date(data.get("published-online"))
        self.published_print = parse_date(data.get("published-print"))

        # Format raw JSON.
        self.json =  json_dumps(data, indent=2)


    def is_penn(self) -> bool:
        """If any author is Penn-affiliated, the DOI is Penn-affiliated."""
        for author in self.authors:
            if author.is_penn:
                return True
        return False


    @property
    def author_display(self) -> str:
        """Comma-separated string of each author name."""
        author_text = ""
        for i, author in enumerate(self.authors, start=1):
            author_text += f"{author.name}"
            if i < self.author_count:
                author_text += ", "
        return author_text


    @property
    def wikitext(self):
        """Information about DOI as wiki-text."""
        return (
            f"|{self.author_display}\n|"
            f"{self.published}\n|"
            f"{self.title}\n|"
            f"{self.container_title}\n|"
            f"{self.doi}\n|"
            f"-"
        )


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()}"


    def __str__(self) -> str:
        msg = self.doi
        if self.title:
            msg += f". {self.title}"
        if self.is_penn():
            msg += " [Penn]"
        return msg
