from requests import get as requests_get


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
    def __init__(self, doi, funder: dict = {}, _gather: bool = True):
        self.doi = doi
        self.fund_doi = funder.get("DOI", "")
        self.name = funder.get("name", "")
        self.awards = set(funder.get("award", set()))

        # Gather fund DOI data, by default.
        if self.fund_doi and _gather:
            self._data = self.__gather(self.fund_doi)

            # Fill in attributes of the Python DOI funder object, via JSON data.
            if self._data:

                # Set label attributes.
                try:
                    self.preferred_label = self._data["prefLabel"]["Label"]\
                                           ["literalForm"]["content"]
                    alts = self._data["altLabel"]

                    # Use single alternative label.
                    if len(alts) == 1:
                        self.alternative_label = alts["Label"]["literalForm"]\
                            ["content"]

                    # Otherwise, use the alternative label that is longest.
                    else:
                        for alt_label in alts:
                            alt = alt_label["Label"]["literalForm"]["content"]
                            if len(alt) > len(self.alternative_label):
                                self.alternative_label = alt

                except KeyError:
                    pass

                finally:
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
