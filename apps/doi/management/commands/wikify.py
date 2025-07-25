from django.core.management.base import BaseCommand, CommandError
from apps.doi.models.doi import DOI


class Command(BaseCommand):
    """wikify command to format a single DOI as wiki-text."""

    help = "Wikify single DOI."

    def add_arguments(self, parser):
        parser.add_argument("doi", nargs=1, type=str)

    def handle(self, *args, **kwargs):
        try:
            doi = DOI(kwargs["doi"][0], check_orcids=False)
        except Exception as exc:
            raise CommandError(exc) from exc

        self.stdout.write(f"{doi}")
        self.stdout.write(self.style.SUCCESS(doi.wikitext))
