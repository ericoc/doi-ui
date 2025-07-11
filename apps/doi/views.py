from http import HTTPStatus
from re import compile as re_compile

from django.conf import settings
from django.contrib import messages
# from django.http import Http404
from django.utils.html import format_html

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
                messages.error(
                    request,
                    "Sorry, but that is not a valid DOI."
                )
                self.status_code = HTTPStatus.BAD_REQUEST
                self.title = "Invalid DOI"

            else:

                try:
                    self.doi = DOI(_doi=doi)
                    self.status_code = HTTPStatus.OK
                    self.title = self.doi.doi
                    self.template_name = "home.html"

                except FileNotFoundError:
                    messages.error(
                        request,
                        message=format_html(
                            "Sorry. DOI (<code>{}</code>) not found.",
                            doi
                        )
                    )
                    self.status_code = HTTPStatus.NOT_FOUND
                    self.title = "Not Found"

                except Exception:
                    messages.error(
                        request,
                        "Sorry, but there was an unknown error."
                    )
                    self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
                    self.title = "Unknown Error"

        return super().setup(request, *args, **kwargs)
