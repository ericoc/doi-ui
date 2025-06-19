"""
Funder of a DOI includes name, DOI, awards, etc..
"""
class DOIFunder:

    doi: str = ""
    name: str = ""
    awards: list = []
    funding_doi: str = ""

    # Initialization of a DOI funder.
    def __init__(self, doi, funder: dict = {}):
        self.doi = doi
        self.funding_doi = funder.get("DOI", "")
        self.name = funder.get("name", "")
        self.awards = funder.get("award", [])

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: {self.__str__()}'

    def __str__(self) -> str:
        return (
            f'{self.name} ({self.funding_doi}) [{len(self.awards)} awards(s)]'
            f' @ {self.doi}'
        )
