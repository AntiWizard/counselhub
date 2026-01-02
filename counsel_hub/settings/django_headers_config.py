from corsheaders.defaults import default_headers, default_methods
from counsel_hub.settings.django import settings

CORS_ORIGIN_WHITELIST = [
    "http://localhost:8000",
    "http://localhost:3000",
]

CORS_ALLOW_ALL_ORIGINS = settings.DEBUG

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = list(default_headers) + [
    "x-client",
    "x-token-id",
    "x-token",
    "X-Token",
    "accept-language",
]

CORS_ALLOW_METHODS = list(default_methods)
