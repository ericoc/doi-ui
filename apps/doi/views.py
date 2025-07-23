from http import HTTPStatus
from logging import getLogger
from django.contrib import messages
from django.utils.html import format_html

from apps.core.views import BaseView
from apps.doi.models import DOI


# Logger.
logger = getLogger(__name__)


class DOIView(BaseView):
    """
    View to search a DOI.
    """
    title = "Search"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        # Process any submitted DOI from query string.
        doi = request.GET.get("doi", "")
        if doi:
            try:
                self.doi = DOI(_doi=doi)
                self.status_code = HTTPStatus.OK
                self.title = self.doi.doi

            # HTTP 400 if submitted DOI is not valid format/syntax.
            except NameError as name_err:
                logger.exception(name_err)
                messages.error(
                    request,
                    message="Sorry, but that is not a valid DOI."
                )
                self.status_code = HTTPStatus.BAD_REQUEST
                self.title = "Invalid DOI Format"

            # HTTP 206 if submitted DOI is not supported (is not Crossref).
            except ValueError as lookup_err:
                logger.exception(lookup_err)
                url = f"https://doi.org/{doi}"
                messages.error(
                    request,
                    message=format_html(
                        'Sorry'
                        ' &mdash; only <i>Crossref</i> is currently supported'
                        ' &mdash; not <code><a href="{}" target="_blank" title="DOI:'
                        ' {}">{}</a></code>',
                        url, doi, url
                    )
                )
                self.status_code = HTTPStatus.PARTIAL_CONTENT
                self.title = "Not Supported"

            # HTTP 404 if DOI could not be found.
            except FileNotFoundError as not_found:
                logger.exception(not_found)
                messages.error(
                    request,
                    message=(
                        format_html(
                        "Sorry. DOI (<code>{}</code>) not found.",
                        doi
                        )
                    )
                )
                self.status_code = HTTPStatus.NOT_FOUND
                self.title = "Not Found"

            # Unknown errors?
            except Exception as other_exc:
                logger.exception(other_exc)
                messages.error(
                    request,
                    message="Sorry, but there was an unknown error."
                )
                self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
                self.title = "Unknown Error"
