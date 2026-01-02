from decouple import config

PROJECT_NAME = config("APP_BASE_NAME")

DB_NAME = config("DB_NAME", default="")
DB_HOST = config("DB_HOST", default="")
DB_PORT = config("DB_PORT", cast=int, default="")
DB_USER = config("DB_USER", default="")
DB_PASSWORD = config("DB_PASSWORD", default="")
# neshan service
NESHAN_API = config("NESHAN_API", default="")
NESHAN_TOKEN = config("NESHAN_TOKEN", default="")

# gis postgres config
GDAL_LIBRARY_PATH = config("GDAL_LIBRARY_PATH", default="")
