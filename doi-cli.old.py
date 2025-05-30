#!/usr/bin/env python3
import logging
from requests import get
from argparse import ArgumentParser

"""
doi-cli.old.py

===

$ ./doi-cli.old.py
usage: doi-cli.old.py [-h] [-v] doi
doi-cli.old.py: error: the following arguments are required: doi

---

$ ./doi-cli.old.py -h
usage: doi-cli.old.py [-h] [-v] doi

positional arguments:
  doi            Digital Object Identifier (DOI)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  verbose

---

# 10.1038/s41586-024-08156-8
$ ./doi-cli.old.py 10.1038/s41586-024-08156-8
2025-05-29 21:48:39 EDT (-0400) [INFO] (61259): 12 author(s) found. (https://doi.org/10.1038/s41586-024-08156-8)
2025-05-29 21:48:39 EDT (-0400) [INFO] (61259):   1. Gaurav Modi (first) [https://orcid.org/0000-0001-6883-814X]
2025-05-29 21:48:39 EDT (-0400) [INFO] (61259):   2. Shubham K. Parate (additional) [https://orcid.org/0009-0004-5991-9609]
2025-05-29 21:48:39 EDT (-0400) [INFO] (61259):   3. Choah Kwon (additional) [None]
2025-05-29 21:48:39 EDT (-0400) [INFO] (61259):   4. Andrew C. Meng (additional) [None]
2025-05-29 21:48:39 EDT (-0400) [INFO] (61259):   5. Utkarsh Khandelwal (additional) [None]
2025-05-29 21:48:39 EDT (-0400) [INFO] (61259):   6. Anudeep Tullibilli (additional) [None]
2025-05-29 21:48:39 EDT (-0400) [INFO] (61259):   7. James Horwath (additional) [None]
2025-05-29 21:48:39 EDT (-0400) [INFO] (61259):   8. Peter K. Davies (additional) [None]
2025-05-29 21:48:39 EDT (-0400) [INFO] (61259):   9. Eric A. Stach (additional) [https://orcid.org/0000-0002-3366-2153]
2025-05-29 21:48:39 EDT (-0400) [INFO] (61259):   10. Ju Li (additional) [https://orcid.org/0000-0002-7841-8058]
2025-05-29 21:48:39 EDT (-0400) [INFO] (61259):   11. Pavan Nukala (additional) [None]
2025-05-29 21:48:39 EDT (-0400) [INFO] (61259):   12. Ritesh Agarwal (additional) [https://orcid.org/0000-0002-1289-4334]

"""

# Parse DOI argument.
parser = ArgumentParser()
parser.add_argument("doi", help="Digital Object Identifier (DOI)")
parser.add_argument("-v", "--verbose", help="verbose", action="store_true")
args = parser.parse_args()

# Logging.
LOG_LEVEL = logging.INFO
if args.verbose:
    LOG_LEVEL = logging.DEBUG
logging.basicConfig(
    datefmt="%Y-%m-%d %H:%M:%S %Z (%z)",
    format="%(asctime)s [%(levelname)s] (%(process)d): %(message)s",
    handlers=[logging.StreamHandler()],
    level=LOG_LEVEL
)
logger = logging.getLogger(__name__)

# Empty authors tuple and HTTPS request to doi.org to gather DOI information.
authors = ()
doi_url = f'https://doi.org/{args.doi}'
try:
    resp = get(
        url=doi_url,
        headers={
            "Accept": "application/json",
            "User-Agent": "DOI JSON Search / nano.upenn.edu v0.1"
        }
    ).json()
    logger.debug(resp)
    authors = resp["author"]
    logger.debug(authors)
except Exception as req_exc:
    logger.exception(msg="API request failed.", exc_info=req_exc)

# Ensure that at least one author is found.
finally:
    author_count = len(authors) or 0
    assert author_count > 0, f'No authors found for DOI! ({doi_url})'

# List total author count, as well as each author name, sequence, and ORCID.
logger.info(f'{author_count} author(s) found. ({doi_url})')
for (i, author) in enumerate(iterable=authors, start=1):
    logger.debug(author)
    """
    For example:
    2025-05-29 21:53:57 EDT (-0400) [DEBUG] (61452):
        {
            'ORCID': 'https://orcid.org/0000-0002-3366-2153',
            'authenticated-orcid': False,
            'given': 'Eric A.',
            'family': 'Stach',
            'sequence': 'additional',
            'affiliation': []
        }

    2025-05-29 21:53:57 EDT (-0400) [INFO] (61452):
        9. Eric A. Stach (additional) [https://orcid.org/0000-0002-3366-2153]
    """
    name = f'{author.get("given")} {author.get("family")}'
    orcid = author.get("ORCID")
    authenticated_orcid = author.get("authenticated-orcid")
    sequence = author.get("sequence")
    logger.info(f'  {i}. {name} ({sequence}) [{orcid}]')
