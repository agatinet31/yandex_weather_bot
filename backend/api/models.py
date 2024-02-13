from datetime import timedelta

from django.core.validators import (
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
from yandex_weather.settings.base import TIMEOUT_YANDEX_UPDATE


class YandexWeatherModel(BaseModel):
    """Модель для прогноза погоды."""

    CITYNAME_FIELD = "city"

    city = models.CharField(
        _("city"),
        unique=True,
        max_length=150,
        validators=[MinLengthValidator(3)],
        help_text=_("Required. 3-150 characters. Letters only."),
    )
    latitude = models.FloatField(
        _("latitude"),
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
        help_text=_("Required. Latitude value."),
    )
    longitude = models.FloatField(
        _("longitude"),
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
        help_text=_("Required. Longitude value."),
    )
    updated_at = models.DateTimeField(
        _("updated_at"),
        null=True,
        help_text=_("Not required. Update datetime from yandex."),
    )
    temp = models.FloatField(
        _("temp"),
        null=True,
        help_text=_("Not required. Temp in city."),
    )
    pressure_mm = models.IntegerField(
        _("pressure_mm"),
        null=True,
        help_text=_("Not required. Pressure in city."),
    )
    wind_speed = models.FloatField(
        _("wind_speed"),
        null=True,
        help_text=_("Not required. Wind speed in city."),
    )

    @property
    def is_need_update(self):
        return (
            self.updated_at is None
            or self.updated_at
            < timezone.now() - timedelta(minutes=TIMEOUT_YANDEX_UPDATE)
        )

    def __str__(self):
        return (
            f"City: {self.city} ("
            f"temp: {self.temp}, "
            f"pressure_mm: {self.pressure_mm}, "
            f"wind_speed: {self.wind_speed})"
        )

    class Meta:
        verbose_name = "Прогноз погоды для города"
        verbose_name_plural = "Прогнозы погоды для городов"
        ordering = ("city",)
        constraints = [
            UniqueConstraint(
                fields=["latitude", "longitude"],
                name="unique_coords",
            )
        ]
