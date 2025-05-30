#!/usr/bin/env python3
import logging
from argparse import ArgumentParser
from DOI import DOI


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

# Gather DOI information.
doi = DOI(args.doi)
logger.debug(doi)
authors = doi.authors
logger.debug(authors)

# List total author count, as well as each author name, sequence, and ORCID.
logger.info(doi.title)
logger.info(doi.url)
logger.info(f'{len(authors)} author(s) found:')
for (i, author) in enumerate(iterable=authors, start=1):
    logger.debug(author)
    name = f'{author.get("given")} {author.get("family")}'
    orcid = author.get("ORCID")
    sequence = author.get("sequence")
    logger.info(f'  {i}. {name} ({sequence}) [{orcid}]')
