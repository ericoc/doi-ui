"""
Funder of a DOI includes name, DOI, awards, etc.
"""
class DOIFunder:

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

    # Initialization of a DOI funder.
    def __init__(self, doi: str, funder: dict):
        self.doi = doi
        self.fund_doi = funder.get("DOI", "")
        self.name = funder.get("name", "")
        self.awards = set(funder.get("award", set()))

        # Fill in attributes of the Python DOI funder object, via JSON data.
        try:

            # Set label attributes.
            self.preferred_label = funder["prefLabel"]["Label"]\
                                   ["literalForm"]["content"]
            self.alternative_labels = []
            alts = funder["altLabel"]

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
            self.body_type = funder["fundingBodyType"]
            self.body_subtype = funder["fundingBodySubType"]

            # Set broader resource, and region attributes.
            self.broader = funder["broader"]["resource"]
            self.region = funder["region"]

        except KeyError:
            pass

        finally:
            del funder

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: {self.__str__()}'

    def __str__(self) -> str:
        return (
            f'{self.name} ({self.fund_doi}) [{len(self.awards)} awards(s)]'
            f' @ {self.doi}'
        )

    @property
    def anchor(self) -> str:
        return self.name.replace(" ", "-").replace("_", "-").replace("/", "-")
