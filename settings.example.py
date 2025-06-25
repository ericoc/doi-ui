"""Django settings for doi-ui project."""
from pathlib import Path


# Website title.
WEBSITE_TITLE = 'DOI'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

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
ADMINS = MANAGERS = (('Eric OC', 'doi@ericoc.com'),)
DEFAULT_FROM_EMAIL = SERVER_EMAIL = 'doi@' + ALLOWED_HOSTS[0]
EMAIL_SUBJECT_PREFIX = f'[Django: {WEBSITE_TITLE}] '
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = EMAIL_HOST_PASSWORD = None

# Application definition.
INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'doi'
]

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'doi.contexts.website_title',
            ],
            'libraries': {
                'doi': 'doi.templatetags'
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

# Media files (and galleries, in this case).
GALLERY_URL = 'galleries/'
MEDIA_URL = 'media/'
MEDIA_ROOT = Path(BASE_DIR, MEDIA_URL)

X_FRAME_OPTIONS = 'SAMEORIGIN'

# ORCID API settings.
ORCID_API_CLIENT_ID = "APP-xxx"
ORCID_API_CLIENT_SECRET = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
