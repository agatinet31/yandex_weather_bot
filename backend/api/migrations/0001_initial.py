# Generated by Django 4.2.10 on 2024-02-13 11:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="YandexWeatherModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "city",
                    models.CharField(
                        help_text="Required. 3-150 characters. Letters only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.core.validators.MinLengthValidator(3)
                        ],
                        verbose_name="city",
                    ),
                ),
                (
                    "latitude",
                    models.FloatField(
                        help_text="Required. Latitude value.",
                        validators=[
                            django.core.validators.MinValueValidator(-90.0),
                            django.core.validators.MaxValueValidator(90.0),
                        ],
                        verbose_name="latitude",
                    ),
                ),
                (
                    "longitude",
                    models.FloatField(
                        help_text="Required. Longitude value.",
                        validators=[
                            django.core.validators.MinValueValidator(-180.0),
                            django.core.validators.MaxValueValidator(180.0),
                        ],
                        verbose_name="longitude",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        help_text="Not required. Update datetime from yandex.",
                        null=True,
                        verbose_name="updated_at",
                    ),
                ),
                (
                    "temp",
                    models.FloatField(
                        help_text="Not required. Temp in city.",
                        null=True,
                        verbose_name="temp",
                    ),
                ),
                (
                    "pressure_mm",
                    models.IntegerField(
                        help_text="Not required. Pressure in city.",
                        null=True,
                        verbose_name="pressure_mm",
                    ),
                ),
                (
                    "wind_speed",
                    models.FloatField(
                        help_text="Not required. Wind speed in city.",
                        null=True,
                        verbose_name="wind_speed",
                    ),
                ),
            ],
            options={
                "verbose_name": "Прогноз погоды для города",
                "verbose_name_plural": "Прогнозы погоды для городов",
                "ordering": ("city",),
            },
        ),
        migrations.AddConstraint(
            model_name="yandexweathermodel",
            constraint=models.UniqueConstraint(
                fields=("latitude", "longitude"), name="unique_coords"
            ),
        ),
    ]
