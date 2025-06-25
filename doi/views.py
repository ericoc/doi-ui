import re
import requests

from django.conf import settings
from django.core.cache import cache
from django.views.generic.base import TemplateView
from django.http.response import HttpResponseBadRequest

from .models import DOI


DOI_REGEX = re.compile(r'(doi\:)?(10[.][0-9]{4,}[^\s"\/<>]*\/[^\s"<>]+)')
REQUEST_HEADERS = {
    "Accept": "application/json",
    "User-Agent": f"DOI Search / {settings.WEBSITE_TITLE} v1.0"
}


class HomeView(TemplateView):
    """Main page also searches DOI."""

    doi = None
    http_method_names = ("get",)
    template_name = "home.html"

    def dispatch(self, request, *args, **kwargs):

        submitted_doi = request.GET.get("doi")

        if submitted_doi:
            if not DOI_REGEX.match(submitted_doi):
                return HttpResponseBadRequest("Invalid DOI format!")

            doi_cache_key = f"doi_{submitted_doi}"
            self.doi = cache.get(doi_cache_key)

            if not self.doi:
                try:
                    resp = requests.get(
                        headers=REQUEST_HEADERS,
                        url=f"https://doi.org/{submitted_doi}",
                        timeout=3
                    )
                    if resp.status_code != 200:
                        return HttpResponseBadRequest("No such DOI was found!")
                    self.doi = DOI(doi=submitted_doi, _data=resp.json())
                    cache.set(doi_cache_key, self.doi)
                except Exception as doi_exc:
                    raise doi_exc

        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doi"] = self.doi
        return context
