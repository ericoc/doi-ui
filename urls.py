from http import HTTPStatus

from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import path

from apps.core.views import ErrorView
from apps.doi.views import DOIView


# Include DOI application URL.
urlpatterns = [path("", DOIView.as_view(), name="doi"),]

# Error handlers.
handler400 = ErrorView.as_view(
    message="Sorry, but the request was not understood.",
    status_code=HTTPStatus.BAD_REQUEST,
    title="Bad Request"
)
handler401 = ErrorView.as_view(
    message="Sorry, but you do not have authorization to access this page.",
    status_code=HTTPStatus.UNAUTHORIZED,
    title="Not Authorized"
)
handler403 = ErrorView.as_view(
    message="Sorry, but access to this page is forbidden.",
    status_code=HTTPStatus.FORBIDDEN,
    title="Forbidden"
)
handler404 = ErrorView.as_view(
    message="Sorry, but no such page could be found.",
    status_code=HTTPStatus.NOT_FOUND,
    title="Page Not Found"
)
handler405 = ErrorView.as_view(
    message="Sorry, but the requested method is not supported.",
    status_code=HTTPStatus.METHOD_NOT_ALLOWED,
    title="Method Not Allowed"
)
handler410 = ErrorView.as_view(
    message="Sorry, but that resource is gone.",
    status_code=HTTPStatus.GONE,
    title="Gone"
)
handler420 = ErrorView.as_view(
    message="Sorry, but please enhance your calm.",
    status_code=420,
    title="Enhance Your Calm"
)
handler500 = ErrorView.as_view(
    message="Sorry, but unfortunately, there was an internal server error.",
    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
    title="Sorry!"
)
handler501 = ErrorView.as_view(
    message="Sorry, but the server cannot handle your request.",
    status_code=HTTPStatus.NOT_IMPLEMENTED,
    title="Not Implemented"
)

# Host static and media content in debug mode.
if settings.DEBUG:
    urlpatterns += \
        static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += \
        static(prefix=settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += path(f"{HTTPStatus.BAD_REQUEST}/", handler400, name="400"),
    urlpatterns += path(f"{HTTPStatus.UNAUTHORIZED}/", handler401, name="401"),
    urlpatterns += path(f"{HTTPStatus.FORBIDDEN}/", handler403, name="403"),
    urlpatterns += path(f"{HTTPStatus.NOT_FOUND}/", handler404, name="404"),
    urlpatterns += \
        path(f"{HTTPStatus.METHOD_NOT_ALLOWED}/", handler405, name="405"),
    urlpatterns += path(f"{HTTPStatus.GONE}/", handler410, name="410"),
    urlpatterns += path("420/", handler420, name="420"),
    urlpatterns += \
        path(f"{HTTPStatus.INTERNAL_SERVER_ERROR}/", handler500, name="500"),
    urlpatterns += \
        path(f"{HTTPStatus.NOT_IMPLEMENTED}/", handler501, name="501"),
