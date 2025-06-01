#!/usr/bin/env python3
import logging
from argparse import ArgumentParser, RawTextHelpFormatter
from doi import DOI, DOI_URL


# Parse DOI argument.
parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
parser.add_argument(
    "doi",
    help="Digital Object Identifier (DOI)\n\te.g. 10.1038/s41586-024-08156-8"
)
parser.add_argument(
    "-a", "--authors", help="Show authors.", action="store_true"
)
parser.add_argument(
    "-d", "--dates", help="Show dates.", action="store_true"
)
parser.add_argument(
    "-r", "--references",
    help="Show reference information.", action="store_true"
)
parser.add_argument(
    "-v", "--verbose", help="Verbose output.", action="store_true"
)
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

# Gather DOI information, and list its basic details.
doi = DOI(args.doi)
logger.info(f'{doi.title} ({doi.type})')
logger.info(doi.url)
logger.info(doi.publisher)
logger.debug(doi)

# List dates, if requested.
if args.dates is True:
    created = doi.created
    if created:
        logger.info(f'Created: {created.strftime("%c")} ({created})')
    deposited = doi.deposited
    if deposited:
        logger.info(f'Deposited: {deposited.strftime("%c")} ({deposited})')
    indexed = doi.indexed
    if indexed:
        logger.info(f'Indexed: {indexed.strftime("%c")} ({indexed})')
    issued = doi.issued
    if issued:
        logger.info(f'Issued: {issued.strftime("%c")} ({issued})')
    published = doi.published
    if published:
        logger.info(f'Published: {published.strftime("%c")} ({published})')
    published_online = doi.published_online
    if published_online:
        logger.info(
            f'Published Online: {published_online.strftime("%c")}'
            f' ({published_online})'
        )
    published_print = doi.published_print
    if published_print:
        logger.info(
            f'Published Print: {published_print.strftime("%c")}'
            f' ({published_print})'
        )

# List authors, if requested.
if args.authors is True:
    authors = doi.authors
    if authors:
        logger.info(f'{len(authors)} author(s):')
        for (i, author) in enumerate(iterable=authors, start=1):
            name = f'{author.get("given")} {author.get("family")}'
            orcid = author.get("ORCID")
            sequence = author.get("sequence")
            logger.info(f'  {i}. {name} ({sequence}) [ORCID: {orcid}]')
            logger.debug(author)

# List reference DOI(s), if requested.
if args.references is True:
    referenced_by_count = doi.referenced_by_count
    logger.info(f'Referenced By: {doi.referenced_by_count}')
    references = doi.references
    if references:
        logger.info(f'{doi.reference_count} reference(s):')

        # Gather the information of any DOI of each reference.
        for (i, reference) in enumerate(iterable=references, start=1):
            msg = f'      {i}. '
            if reference:
                reference_doi = reference.get("DOI")
                if reference_doi:
                    reference_obj = DOI(reference_doi)
                    if reference_obj:
                        msg += reference_obj.title
                        reference_url = f"{DOI_URL}/{reference_doi}"
                        if reference_url:
                            msg += f' ({reference_url})'
                        logger.debug(reference_obj)
                else:
                    msg = f'      {i}. {str(reference)}'
            logger.info(msg)
