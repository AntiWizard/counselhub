from decouple import config
import os

from .common import BASE_DIR

URL_PREFIX = config("URL_PREFIX", default="")

FORCE_SCRIPT_NAME = URL_PREFIX

STATIC_URL = os.getenv("STATIC_URL", f"{URL_PREFIX}/static/")
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Media
MEDIA_URL = os.getenv("MEDIA_URL", f"{URL_PREFIX}/media/")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
