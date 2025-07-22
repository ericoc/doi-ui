from http import HTTPStatus
from django.views.generic.base import TemplateView

from apps.doi.models.doi import DOI


class BaseView(TemplateView):
    """
    Base view.
    """
    doi: (DOI, str) = ""
    http_method_names: tuple = ("get",)
    status_code: int = HTTPStatus.OK
    title: str = "Home"
    template_name: str = "home.html"

    def get_context_data(self, **kwargs):
        # Include DOI object and title in response context.
        context = super().get_context_data(**kwargs)
        context["doi"] = self.doi
        context["title"] = self.title
        return context

    def get(self, request, *args, **kwargs):
        # Update HTTP response code.
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=self.status_code)
