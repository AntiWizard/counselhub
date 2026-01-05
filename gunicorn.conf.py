import gunicorn
from decouple import config

gunicorn.SERVER_SOFTWARE = ""
gunicorn.SERVER = ""
bind = "0.0.0.0:8000"
workers = 5
preload_app = True
proc_name = config("PROJECT_NAME")
loglevel = "info"
