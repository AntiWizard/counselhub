from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Set the Django setting from the environment variable.
DEBUG = bool(str(config("DEBUG", default=True)).lower() in ["true", "1"])
