from http import HTTPStatus
from logging import getLogger
from re import compile as re_compile

from django.conf import settings
from django.contrib import messages
from django.utils.html import format_html
from requests.exceptions import JSONDecodeError

from apps.core.views import BaseView
from apps.doi.models import DOI


# Logger.
logger = getLogger(__name__)

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

                except FileNotFoundError as not_found:
                    logger.exception(not_found)
                    messages.error(
                        request,
                        message=format_html(
                            "Sorry. DOI (<code>{}</code>) not found.",
                            doi
                        )
                    )
                    self.status_code = HTTPStatus.NOT_FOUND
                    self.title = "Not Found"

                except JSONDecodeError as json_err:
                    logger.exception(json_err)
                    messages.error(
                        request,
                        "Sorry, but there was a JSON decoding error."
                    )
                    self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
                    self.title = "JSON Decoding Error"

                except Exception as other_exc:
                    logger.exception(other_exc)
                    messages.error(
                        request,
                        "Sorry, but there was an unknown error."
                    )
                    self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
                    self.title = "Unknown Error"

        return super().setup(request, *args, **kwargs)
