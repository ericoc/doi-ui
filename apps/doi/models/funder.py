import requests
from django.conf import settings
from logging import getLogger


# Logging.
logger = getLogger(__name__)


class DOIFunder:
    """
    Digital Object Identifier (DOI) Funder.
        Includes name, DOI, awards, etc.
    """
    doi: str = ""
    name: str = ""
    preferred_label: str = ""
    alternative_labels: list = []
    awards: set = set()
    broader: str = ""
    fund_doi: str = ""
    body_type: str = ""
    body_subtype: str = ""
    region: str = ""

    def __init__(self, doi: str, funder: dict):
        """Initialization of DOI funder."""
        self.doi = doi
        self.fund_doi = funder.get("DOI", self.fund_doi)
        self.name = funder.get("name", self.name)
        self.awards = set(funder.get("award", self.awards))

        # Gather information about the funder DOI.
        if self.fund_doi:
            self.gather()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()}"

    def __str__(self) -> str:
        return (
            f"{self.name} ({self.fund_doi}) [{len(self.awards)} awards(s)]"
            f" @ {self.doi}"
        )

    def gather(self):
        """Gather information from crossref.org about the funding DOI."""
        try:
            resp = requests.get(
                headers=settings.REQUEST_HEADERS,
                timeout=settings.REQUEST_TIMEOUT,
                url="https://data.crossref.org/fundingdata/funder/"
                    f"{self.fund_doi}"
            )
            resp.raise_for_status()
            data = resp.json()

        # Skip failed DOI funder request/JSON.
        except (
            requests.exceptions.HTTPError,
            requests.exceptions.JSONDecodeError
        ):
            return None

        # Fill in funder object attributes using JSON response.
        try:
            self.preferred_label = data["prefLabel"]["Label"]["literalForm"]\
            ["content"]
            self.alternative_labels = []
            alts = data["altLabel"]

            # Use single alternative label, or append to list of alternatives.
            if len(alts) == 1:
                self.alternative_labels.append(
                    alts["Label"]["literalForm"]["content"]
                )
            else:
                for alt_label in alts:
                    self.alternative_labels.append(
                        alt_label["Label"]["literalForm"]["content"]
                    )

            # Set funding body type/subtype.
            self.body_type = data["fundingBodyType"]
            self.body_subtype = data["fundingBodySubType"]

            # Set broader resource and region attributes.
            self.broader = data["broader"]["resource"]
            self.region = data["region"]

        except KeyError:
            pass
