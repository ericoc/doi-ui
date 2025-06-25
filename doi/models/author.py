"""
Author of a DOI can include specific affiliation(s), ORCID, etc.
"""
class DOIAuthor:

    doi: str = ""
    given: str = ""
    family: str = ""
    name: str = ""
    sequence: str = ""
    affiliation: list = []
    orcid: str = ""
    is_penn: bool = False

    # Initialization of a DOI author.
    def __init__(self, doi: str, author: dict):
        self.doi = doi
        self.orcid = author.get("ORCID", "")
        self.sequence = author.get("sequence", "")
        self.given = author.get("given", "")
        self.family = author.get("family", "")
        self.name = f"{self.given} {self.family}"

        # Check if DOI author is affiliated with "University of Pennsylvania".
        self.affiliation = author.get("affiliation", [])
        self.is_penn = self.is_affiliated("University of Pennsylvania")

    def is_affiliated(self, _test: str = "") -> bool:
        # Check for test string in each affiliation name.
        if _test:
            for affiliation in self.affiliation:
                if _test in affiliation.get("name", ""):
                    return True
        return False

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: {self.__str__()}'

    def __str__(self) -> str:
        msg = f'{self.name}'
        if self.orcid:
            msg += f' <{self.orcid}>'
        if self.is_penn:
            msg += ' [Penn]'
        msg += f' ({self.sequence})'
        msg += f' @ {self.doi}'
        return msg
