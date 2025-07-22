from django.conf import settings


def context_processors(request):
    # Context processors for debug boolean, university name, and website title.
    return {
        "DEBUG": settings.DEBUG,
        "UNIVERSITY": settings.UNIVERSITY,
        "WEBSITE_TITLE": settings.WEBSITE_TITLE
    }
