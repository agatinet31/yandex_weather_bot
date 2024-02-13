from django.db import DatabaseError, transaction
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api.serializers import YandexWeatherSerializer
from core.exceptions import RequestYandexWeatherError
from core.utils import request_weather_from_yandex_api
from core.validators import validate_only_letters


class YandexWeatherAPIView(GenericAPIView):
    """Возвращает текущую погоду с Yandex для выбранного города."""

    serializer_class = YandexWeatherSerializer
    model = serializer_class.Meta.model
    lookup_field = "{}__iexact".format(model.CITYNAME_FIELD)

    class CityQueryParamsSerializer(serializers.Serializer):
        """Query параметр запроса по наименованию города."""

        city = serializers.CharField(
            min_length=3, max_length=150, validators=[validate_only_letters]
        )

    def get_queryset(self):
        return self.model.objects.select_for_update()

    @extend_schema(
        parameters=[CityQueryParamsSerializer],
        responses=YandexWeatherSerializer,
    )
    def get(self, request):
        filter_serializer = self.CityQueryParamsSerializer(
            data=request.query_params
        )
        filter_serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                self.kwargs[
                    self.lookup_field
                ] = filter_serializer.validated_data["city"]
                weather = self.get_object()
                if weather.is_need_update:
                    weather_from_yandex = request_weather_from_yandex_api(
                        latitude=weather.latitude, longitude=weather.longitude
                    )
                    serializer = self.get_serializer(
                        weather, data=weather_from_yandex
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save(updated_at=timezone.now())
                else:
                    serializer = self.get_serializer(weather)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
            )
        except (DatabaseError, RequestYandexWeatherError):
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
