import os

from django.core.asgi import get_asgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "yandex_weather.settings.develop"
)

application = get_asgi_application()
