import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "yandex_weather.settings.develop"
)

application = get_wsgi_application()
