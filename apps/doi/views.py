from http import HTTPStatus
from logging import getLogger
from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
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
            err_msg = ""
            try:
                self.doi = cache.get_or_set(key=doi, default=DOI(_doi=doi))
                self.status_code = HTTPStatus.OK
                self.title = self.doi.doi

            # HTTP 400 if submitted DOI is not valid format/syntax.
            except NameError as invalid_name_err:
                self.status_code = HTTPStatus.BAD_REQUEST
                self.title = "Invalid DOI Format"
                err_msg = "Sorry, but that is not a valid DOI."
                if settings.DEBUG:
                    logger.exception(
                        msg=f"{self.title} ({doi})",
                        exc_info=invalid_name_err
                    )

            # HTTP 206 if submitted DOI is not supported (is not Crossref).
            except ValueError as unsupported_val_err:
                self.status_code = HTTPStatus.PARTIAL_CONTENT
                self.title = "Not Supported"
                url = f"https://doi.org/{doi}"
                err_msg = format_html(
                    'Sorry &mdash; only <i>Crossref</i> is currently'
                    ' supported &mdash; not'
                    ' <code><a href="{}" target="_blank" title="DOI:'
                    ' {}">{}</a></code>',
                    url, doi, url
                )
                logger.exception(
                    msg=f"{self.title} ({doi})",
                    exc_info=unsupported_val_err
                )

            # HTTP 404 if DOI could not be found.
            except FileNotFoundError as not_found_err:
                self.status_code = HTTPStatus.NOT_FOUND
                self.title = "Not Found"
                err_msg = format_html(
                    "Sorry. DOI (<code>{}</code>) not found.",
                    doi
                )
                if settings.DEBUG:
                    logger.exception(
                        msg=f"{self.title} ({doi})",
                        exc_info=not_found_err
                    )

            # Unknown error?
            except Exception as unknown_exc:
                self.title = "Unknown Error"
                err_msg = "Sorry, but there was an unknown error."
                self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
                logger.exception(
                    msg=f"{self.title} ({doi})",
                    exc_info=unknown_exc
                )

            # Message any errors.
            finally:
                if err_msg:
                    messages.error(request=request, message=err_msg)
