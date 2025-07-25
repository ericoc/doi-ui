# from django.conf import settings
from django.core.management.base import BaseCommand # , CommandError
# from pathlib import Path
# from pprint import pformat


class WikifyDOICommand(BaseCommand):
    """TODO: Perhaps create a wikify Django management command,
        to display wiki-text using the wikitext property of each DOI object."""
