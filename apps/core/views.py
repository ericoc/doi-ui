from http import HTTPStatus

from django.contrib import messages
from django.views.generic.base import TemplateView

from apps.doi.models.doi import DOI


class BaseView(TemplateView):
    """Base view."""
    doi: (DOI, str) = ""
    http_method_names: tuple = ("get",)
    message: str = ""
    status_code: int = HTTPStatus.OK
    title: str = "Home"
    template_name: str = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doi"] = self.doi
        context["title"] = self.title
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=self.status_code)


class ErrorView(BaseView):
    """Template view for error handlers shows message with status code."""
    message = "Sorry, but unfortunately, there was an unknown error."
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    title = "Sorry"

    def setup(self, request, *args, **kwargs):
        if self.message:
            messages.error(request, self.message)
        return super().setup(self, request, *args, **kwargs)
