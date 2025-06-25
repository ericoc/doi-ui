from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from views import ErrorView


# Error handlers.
handler400 = ErrorView.as_view(
    message="Sorry, but the request was not understood.",
    status_code=400,
    title="Bad Request"
)
handler401 = ErrorView.as_view(
    message="Sorry, but you do not have authorization to access this page.",
    status_code=401,
    title="Not Authorized"
)
handler403 = ErrorView.as_view(
    message="Sorry, but access to this page is forbidden.",
    status_code=403,
    title="Forbidden"
)
handler404 = ErrorView.as_view(
    message="Sorry, but no such page could be found.",
    status_code=404,
    title="Page Not Found"
)
handler405 = ErrorView.as_view(
    message="Sorry, but the requested method is not supported.",
    status_code=405,
    title="Method Not Allowed"
)
handler410 = ErrorView.as_view(
    message="Sorry, but that resource is gone.",
    status_code=410,
    title="Gone"
)
handler420 = ErrorView.as_view(
    message="Sorry, but please enhance your calm.",
    status_code=420,
    title="Enhance Your Calm"
)
handler500 = ErrorView.as_view(
    message="Sorry, but unfortunately, there was an internal server error.",
    status_code=500,
    title="Sorry!"
)
handler501 = ErrorView.as_view(
    message="Sorry, but the server cannot handle your request.",
    status_code=501,
    title="Not Implemented"
)

# Include main application URL(s).
urlpatterns = [
    path("", include("doi.urls"), name="main"),
]

# Host static and media content in debug mode.
if settings.DEBUG:
    urlpatterns += static(
        prefix=settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        prefix=settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
