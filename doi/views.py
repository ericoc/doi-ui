from django.core.exceptions import BadRequest
from django.http.response import Http404
from django.views.generic.base import TemplateView

from .models import DOI


class HomeView(TemplateView):
    """Main page searches DOI."""

    doi = None
    http_method_names = ("get",)
    template_name = "home.html"

    def setup(self, request, *args, **kwargs):
        return super().setup(request, *args, **kwargs)


    def dispatch(self, request, *args, **kwargs):

        # Create object using DOI submitted via URL.
        submitted_doi = request.GET.get("doi")
        if submitted_doi:
            try:
                self.doi = DOI(submitted_doi=submitted_doi)
            except FileNotFoundError as not_found_err:
                raise Http404(not_found_err)
            except ValueError as val_err:
                raise BadRequest(val_err)
            except Exception as doi_exc:
                raise RuntimeError("Unknown error.") from doi_exc
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doi"] = self.doi
        return context
