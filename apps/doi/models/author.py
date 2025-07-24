from django.conf import settings

from requests.exceptions import HTTPError


"""Author of a DOI can include specific affiliation(s), ORCID, etc."""
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
    def __init__(self, doi: str, author: dict, orcid_api: tuple = ()):
        self.doi = doi
        self.orcid = author.get("ORCID", "")
        self.sequence = author.get("sequence", "")
        self.given = author.get("given", "")
        self.family = author.get("family", "")
        self.name = f"{self.given} {self.family}"

        # Check if DOI author is affiliated with the university.
        self.affiliation = author.get("affiliation", [])
        self.is_penn = self.is_affiliated(settings.UNIVERSITY, orcid_api)

    def is_affiliated(self, _test: str = "", orcid_api: tuple = ()):
        # Check for test string in each affiliation name.
        if _test:
            for affiliation in self.affiliation:
                if _test in affiliation.get("name", ""):
                    return True
        # Check for employment via ORCID.
        if self.orcid_id and orcid_api:
            return self.check_orcid(orcid_api)
        return False

    def check_orcid(self, orcid_api):

        # Gather information about an ORCID to check authors employments.
        employments = None
        try:
            employments = orcid_api[0].read_record_public(
                orcid_id=self.orcid_id,
                request_type="employments",
                token=orcid_api[1]
            )
        # Ignore HTTP response code failures (like 409 for deactivated ORCID).
        except HTTPError:
            pass

        # Process employment records found within the ORCID.
        if employments:
            employ_summary = employments.get("employment-summary")

            # Search each ORCID employment record for the university string.
            for employment in employ_summary:
                employ_org = employment.get("organization")
                if employ_org:
                    org_name = employ_org.get("name")
                    if org_name == settings.UNIVERSITY:
                        return True

        return False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()}"

    def __str__(self) -> str:
        msg = f"{self.name}"
        if self.orcid:
            msg += f" <{self.orcid}>"
        if self.is_penn:
            msg += " [Penn]"
        msg += f" ({self.sequence})"
        msg += f" @ {self.doi}"
        return msg

    @property
    def orcid_id(self) -> str:
        if self.orcid:
            return self.orcid.replace("https://orcid.org/", "")
        return self.orcid
