import os

from configurations.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "totoro_app.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")


application = get_wsgi_application()
