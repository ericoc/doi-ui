from requests import get as requests_get

from ..common import cache


class DOIFunder:
    """Funder of a DOI includes name, DOI, awards, etc."""

    _data: dict = {}

    doi: str = ""
    name: str = ""
    preferred_label: str = ""
    alternative_label: str = ""
    awards: set = set()
    fund_doi: str = ""

    # Initialization of a DOI Funder Python object.
    def __init__(self, doi, funder: dict = {}):
        self.doi = doi
        self.fund_doi = funder.get("DOI", "")
        self.url = \
            f"https://data.crossref.org/fundingdata/funder/{self.fund_doi}"
        self.name = funder.get("name", "")
        self.awards = set(funder.get("award", set()))

        # Check cache for fund DOI information.
        fund_doi_cache = cache.get(self.url)

        # Use cached fund DOI information, if it was found.
        if fund_doi_cache:
            resp = fund_doi_cache

        # Otherwise, gather and cache fund DOI data.
        else:
            resp = requests_get(
                url=self.url,
                headers={"User-Agent": "DOI Search / doi.ericoc.com v1.0"},
                timeout=3
            )
            cache.set(self.url, resp)

        self._data = resp.json()
        self.preferred_label = self._data["prefLabel"]["Label"]["literalForm"]\
            ["content"]
        alts = self._data["altLabel"]

        # Use single alternative label.
        if len(alts) == 1:
            self.alternative_label = alts["Label"]["literalForm"]["content"]

        # Otherwise, use the alternative label that is longest.
        else:
            for alt_label in alts:
                alt = alt_label["Label"]["literalForm"]["content"]
                if len(alt) > len(self.alternative_label):
                    self.alternative_label = alt

        del self._data

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: {self.__str__()}'

    def __str__(self) -> str:
        return (
            f'{self.name} ({self.fund_doi}) [{len(self.awards)} awards(s)]'
            f' @ {self.doi}'
        )

    # Gather (JSON) information about the DOI funder.
    def __gather(self, fund_doi: str) -> dict:
        try:
            resp = requests_get(
                headers={"User-Agent": "DOI Search / doi.ericoc.com v1.0"},
                url=f'https://data.crossref.org/fundingdata/funder/{fund_doi}',
                timeout=3
            )
            if resp.status_code != 200:
                raise FileNotFoundError
            return resp.json()

        except Exception as fund_doi_exc:
            raise fund_doi_exc
