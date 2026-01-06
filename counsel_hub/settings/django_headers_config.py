from corsheaders.defaults import default_headers, default_methods
from decouple import config
from django.conf import settings

CORS_ALLOW_ALL_ORIGINS = config(
    "CORS_ALLOW_ALL_ORIGINS", default=settings.DEBUG, cast=bool
)

CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="",
    cast=lambda v: [s.strip() for s in v.split(",") if s],
)

CORS_ALLOW_CREDENTIALS = config("CORS_ALLOW_CREDENTIALS", default=True, cast=bool)

CORS_ALLOW_HEADERS = list(default_headers) + [
    "x-client",
    "x-token-id",
    "x-token",
    "X-Token",
    "accept-language",
]

CORS_ALLOW_METHODS = list(default_methods)
