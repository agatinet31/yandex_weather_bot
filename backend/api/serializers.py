from rest_framework import serializers

from api.models import YandexWeatherModel


class YandexWeatherSerializer(serializers.ModelSerializer):
    """Сериалайзер погоды."""

    temp = serializers.IntegerField()

    class Meta:
        model = YandexWeatherModel
        fields = ("updated_at", "temp", "pressure_mm", "wind_speed")
        extra_kwargs = {
            "updated_at": {"write_only": True},
            "temp": {"required": True},
            "pressure_mm": {"required": True},
            "wind_speed": {"required": True},
        }
