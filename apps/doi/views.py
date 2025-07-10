from http import HTTPStatus
from re import compile as re_compile

from django.conf import settings
from apps.core.views import BaseView

from apps.doi.models import DOI


# Compile regular expression pattern (of a DOI) from Django settings.
DOI_REGEX = re_compile(settings.DOI_PATTERN)


class DOIView(BaseView):
    """Search DOI."""
    title = "Search"

    def setup(self, request, *args, **kwargs):

        doi = request.GET.get("doi", "")
        if doi:
            if not DOI_REGEX.match(doi):
                self.message = "Sorry, but that is not a valid DOI."
                self.status_code = HTTPStatus.BAD_REQUEST
                self.title = "Invalid DOI"
                self.template_name = "error.html"

            else:

                try:
                    self.doi = DOI(_doi=doi)
                    self.status_code = HTTPStatus.OK
                    self.title = self.doi.doi
                    self.template_name = "home.html"

                except FileNotFoundError:
                    self.message = f"Sorry, DOI ({doi}) could not be found."
                    self.status_code = HTTPStatus.NOT_FOUND
                    self.title = "Not Found"
                    self.template_name = "error.html"

                except Exception:
                    self.message = "Sorry, but there was an unknown error."
                    self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
                    self.title = "Unknown error"
                    self.template_name = "error.html"

        return super().setup(request, *args, **kwargs)
