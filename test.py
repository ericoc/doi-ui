#!/usr/bin/env python3
from DOI import DOI

doi = '10.1038/s41586-024-08156-8'
test = DOI(doi)

print(f'{test.title} @ {test.url}')
for author in test.authors:
    name = f'{author.get("given")} {author.get("family")}'
    print(f'  - {name} (ORCID: {author.get("ORCID")})')
