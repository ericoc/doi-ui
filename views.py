from http import HTTPStatus
from re import compile as re_compile

from django.conf import settings
from django.views.generic.base import TemplateView

from models import DOI


# Compile regular expression pattern (of a DOI) from Django settings.
DOI_REGEX = re_compile(settings.DOI_PATTERN)


class HomeView(TemplateView):
    """Main page searches DOI."""

    doi: DOI = ""
    http_method_names: tuple = ("get",)
    message: str = ""
    status_code: int = HTTPStatus.OK
    title: str = "Home"
    template_name: str = "home.html"

    def setup(self, request, *args, **kwargs):

        submitted_doi = request.GET.get("doi", "")
        if submitted_doi:
            if not DOI_REGEX.match(submitted_doi):
                self.message = "Sorry, but that is not a valid DOI."
                self.status_code = HTTPStatus.BAD_REQUEST
                self.title = "Invalid DOI"
                self.template_name = "error.html"

            else:

                try:
                    self.doi = DOI(submitted_doi=submitted_doi)
                    self.status_code = HTTPStatus.OK
                    self.title = self.doi.doi
                    self.template_name = "home.html"

                except FileNotFoundError:
                    self.message = f"Sorry, but that DOI ({submitted_doi})" \
                        " could not be found."
                    self.status_code = HTTPStatus.NOT_FOUND
                    self.title = "Not Found"
                    self.template_name = "error.html"

                except Exception:
                    self.message = "Sorry, but there was an unknown error."
                    self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
                    self.title = "Unknown error"
                    self.template_name = "error.html"

        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doi"] = self.doi
        context["title"] = self.title
        context["message"] = self.message
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=self.status_code)
