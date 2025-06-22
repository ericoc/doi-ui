from requests import get as requests_get


class DOIFunder:
    """Funder of a DOI includes name, DOI, awards, etc."""

    _data: dict = {}

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
                try:

                    # Set label attributes.
                    self.preferred_label = self._data["prefLabel"]["Label"]\
                                           ["literalForm"]["content"]
                    self.alternative_labels = []
                    alts = self._data["altLabel"]

                    # Use single alternative label.
                    if len(alts) == 1:
                        self.alternative_labels.append(
                            alts["Label"]["literalForm"]["content"]
                        )

                    # Otherwise, use the alternative label that is longest.
                    else:
                        for alt_label in alts:
                            self.alternative_labels.append(
                                alt_label["Label"]["literalForm"]["content"]
                            )

                    # Set funding body type/subtype.
                    self.body_type = self._data["fundingBodyType"]
                    self.body_subtype = self._data["fundingBodySubType"]

                    # Set broader resource, and region attributes.
                    self.broader = self._data["broader"]["resource"]
                    self.region = self._data["region"]

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

    @property
    def anchor(self) -> str:
        return self.name.replace(" ", "-").replace("_", "-").replace("/", "-")
