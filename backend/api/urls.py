from django.urls import include, path

from api.views import YandexWeatherAPIView

app_name = "api"

weather_urls = [
    path(
        route="",
        view=YandexWeatherAPIView.as_view(),
        name="weather",
    ),
]

urlpatterns = [
    path("weather/", include(weather_urls)),
]
