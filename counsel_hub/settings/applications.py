# Application definition
LOCAL_APPS = ["apps.general", "apps.court"]

THIRD_PARTY_APPS = [
    "import_export",
    "simple_history",
    "corsheaders",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    "health_check.contrib.migrations",
    "jalali_date",
    "rest_framework",
    "drf_spectacular",
    "django.contrib.gis",
    "leaflet",
]

DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_APPS = THIRD_PARTY_APPS + DEFAULT_APPS + LOCAL_APPS
