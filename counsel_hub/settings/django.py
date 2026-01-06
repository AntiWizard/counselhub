import os

from decouple import config
from django.conf import settings

ROOT_URLCONF = f"{settings.PROJECT_NAME}.urls"

GDAL_LIBRARY_PATH = os.getenv("GDAL_LIBRARY_PATH", "/lib/libgdal.so")

GEOS_LIBRARY_PATH = os.getenv(
    "GEOS_LIBRARY_PATH", "/usr/lib/x86_64-linux-gnu/libgeos_c.so"
)

SECRET_KEY = config("SECRET_KEY", default="dummy")

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", default="", cast=lambda v: [s.strip() for s in v.split(",") if s]
)

if settings.DEBUG:
    ALLOWED_HOSTS += ["127.0.0.1", "localhost"]

INTERNAL_IPS = ["127.0.0.1"]


MEDIA_URL = "/medias/"
MEDIA_ROOT = os.path.join(settings.BASE_DIR, "medias")


WSGI_APPLICATION = f"{settings.PROJECT_NAME}.wsgi.application"

# Configure HTTPS
USE_X_FORWARDED_HOST = config("USE_X_FORWARDED_HOST", default=True, cast=bool)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TILES = [
    ("satellite", "//mt0.google.com/vt?lyrs=s,h&x={x}&y={y}&z={z}", ""),
    ("openstreet", "//tile.openstreetmap.org/{z}/{x}/{y}.png", ""),
]

LEAFLET_CONFIG = {
    "TILES": TILES,
    "RESET_VIEW": False,
    "NO_GLOBALS": True,
    "DEFAULT_CENTER": (35.702, 51.336),
    "DEFAULT_ZOOM": 18,
    "MAX_ZOOM": 24,
    "MIN_ZOOM": 8,
    "ATTRIBUTION_PREFIX": "powered by ali_marvel",
}

if not settings.DEBUG:
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_SECONDS = 86400
    SECURE_REFERRER_POLICY = "same-origin"

    CSRF_TRUSTED_ORIGINS = config(
        "CSRF_TRUSTED_ORIGINS",
        cast=lambda v: [s.strip() for s in v.split(",") if s],
    )
