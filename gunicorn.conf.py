import os

import gunicorn

gunicorn.SERVER_SOFTWARE = ""
gunicorn.SERVER = ""
bind = "0.0.0.0:8000"
workers = 5
preload_app = True
proc_name = os.getenv("PROJECT_NAME")
loglevel = "info"
