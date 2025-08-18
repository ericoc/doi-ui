import requests
from django.conf import settings
from logging import getLogger


# Logging.
logger = getLogger(__name__)


class DOIFunder:
    """
    Digital Object Identifier (DOI) Funder.
        includes name, DOI, awards, etc.
    """
    doi = ""

    name = ""
    preferred_label = ""
    alternative_labels = []
    awards = set()
    broader = ""
    fund_doi = ""
    body_type = ""
    body_subtype = ""
    region = ""

    # Initialization of a DOI funder.
    def __init__(self, doi: str, funder: dict):

        self.doi = doi
        self.fund_doi = funder.get("DOI", self.fund_doi)
        self.name = funder.get("name", self.name)
        self.awards = set(funder.get("award", self.awards))

        # Gather information about the funder DOI.
        if self.fund_doi:
            try:
                self.gather()
            except Exception as fund_gather_exc:
                logger.exception(fund_gather_exc)
                pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()}"

    def __str__(self) -> str:
        return (
            f"{self.name} ({self.fund_doi}) [{len(self.awards)} awards(s)]"
            f" @ {self.doi}"
        )

    @property
    def anchor(self) -> str:
        return self.name.replace(" ", "-").replace("_", "-").replace("/", "-")

    def gather(self):
        # Gather information from crossref.org about the funding DOI.
        try:
            resp = requests.get(
                headers=settings.REQUEST_HEADERS,
                timeout=settings.REQUEST_TIMEOUT,
                url=f'https://data.crossref.org/fundingdata/funder/{self.fund_doi}'
            )
            resp.raise_for_status()

            # Fill in funder object attributes using JSON response.
            data = resp.json()

            self.preferred_label = data["prefLabel"]["Label"]["literalForm"]\
            ["content"]
            self.alternative_labels = []
            alts = data["altLabel"]

            # Use single alternative label.
            if len(alts) == 1:
                self.alternative_labels.append(
                    alts["Label"]["literalForm"]["content"]
                )

            # Otherwise, create a list of alternative labels.
            else:
                for alt_label in alts:
                    self.alternative_labels.append(
                        alt_label["Label"]["literalForm"]["content"]
                    )

            # Set funding body type/subtype.
            self.body_type = data["fundingBodyType"]
            self.body_subtype = data["fundingBodySubType"]

            # Set broader resource, and region attributes.
            self.broader = data["broader"]["resource"]
            self.region = data["region"]

        except KeyError as fund_gather_key_err:
            logger.exception(fund_gather_key_err)
            pass
