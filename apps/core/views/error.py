from http import HTTPStatus
from django.contrib import messages

from .base import BaseView


class ErrorView(BaseView):
    """
    Template view for error handling shows message with status code.
    """
    message = "Sorry, but unfortunately, there was an unknown error."
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    title = "Sorry"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        # Actually message any message string.
        if self.message:
            messages.error(request, self.message)
