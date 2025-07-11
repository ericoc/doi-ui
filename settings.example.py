"""Django settings for doi-ui project."""
from pathlib import Path


# Website title.
UNIVERSITY = "University of Pennsylvania"
WEBSITE_TITLE = 'DOI'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = 'xxx'
DEBUG = False
ALLOWED_HOSTS = ("doi.ericoc.com",)

# Logging.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG" if DEBUG else "INFO",
    },
}

# Caching.
if DEBUG:
    CACHE_BACKEND = "django.core.cache.backends.dummy.DummyCache"
else:
    CACHE_BACKEND = "django.core.cache.backends.filebased.FileBasedCache"
CACHES = {
    "default": {
        "BACKEND": CACHE_BACKEND,
        "LOCATION": Path(BASE_DIR, "cache"),
    }
}

# CSRF and session cookies.
CSRF_COOKIE_HTTPONLY = SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = SESSION_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = (f'http://{ALLOWED_HOSTS[0]}/',)

# E-mail.
ADMINS = MANAGERS = (('Eric OC', 'eric@ericoc.com'),)
DEFAULT_FROM_EMAIL = SERVER_EMAIL = 'doi@' + ALLOWED_HOSTS[0]
EMAIL_SUBJECT_PREFIX = f'[Django: {WEBSITE_TITLE}] '
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = EMAIL_HOST_PASSWORD = None

# Application definition.
INSTALLED_APPS = [
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.core.CoreConfig',
    'apps.doi.DOIConfig',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (Path(BASE_DIR, 'apps/core/templates/'),),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'apps.core.contexts.website_title',
            ],
            'libraries': {
                'doi': 'apps.core.templatetags'
            },
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_THOUSAND_SEPARATOR = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = Path(BASE_DIR, STATIC_URL)

# Media files.
MEDIA_URL = 'media/'
MEDIA_ROOT = Path(BASE_DIR, MEDIA_URL)

X_FRAME_OPTIONS = 'SAMEORIGIN'

# DOI regular expression pattern.
DOI_PATTERN = r'(doi\:)?(10[.][0-9]{4,}[^\s"\/<>]*\/[^\s"<>]+)'

# ORCID API settings.
ORCID_API_CLIENT_ID = "APP-0123ABCDEFG"
ORCID_API_CLIENT_SECRET = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

REQUEST_HEADERS = {"User-Agent": f"DOI Search / {WEBSITE_TITLE} v2.0"}
REQUEST_TIMEOUT = 5
