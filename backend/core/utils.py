from collections import OrderedDict
from json import JSONDecodeError
from typing import Any, Dict

from django.shortcuts import _get_queryset
from django.utils.translation import gettext_lazy as _
from httpx import Client, HTTPError
from rest_framework.exceptions import ParseError, PermissionDenied

from core.exceptions import RequestYandexWeatherError
from yandex_weather.settings.base import X_YANDEX_API_KEY, YANDEX_WEATHER_URL

REQUEST_HEADERS = {
    "X-Yandex-API-Key": X_YANDEX_API_KEY,
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
}


def get_yandex_weather_query_params(
    latitude: float, longitude: float
) -> Dict[str, Any]:
    return {"lat": latitude, "lon": longitude, "lang": "ru_RU"}


def request_weather_from_yandex_api(
    latitude: float, longitude: float
) -> Dict[str, Any]:
    """Возвращает данные о погоде c yandex."""
    try:
        with Client() as client:
            response = client.get(
                YANDEX_WEATHER_URL,
                headers=REQUEST_HEADERS,
                params=get_yandex_weather_query_params(latitude, longitude),
            )
            response.raise_for_status()
            fact_wheater = response.json()["fact"]
            return dict(
                filter(
                    lambda item: item[0]
                    in ("temp", "pressure_mm", "wind_speed"),
                    fact_wheater.items(),
                )
            )
    except (JSONDecodeError, KeyError, TypeError, HTTPError) as exc:
        raise RequestYandexWeatherError(
            "Не получены данные о погоде с сервиса yandex!"
        ) from exc


def get_field_values_from_object(obj, *fields, **kwargs):
    """Возвращает кортеж из значений атрибутов fields объекта."""
    if not fields:
        return None
    if not isinstance(obj, object):
        raise TypeError(_("Unable to get field data"))
    if kwargs.get("only_one_field"):
        return getattr(obj, fields[0], None)
    return (getattr(obj, field) for field in fields if hasattr(obj, field))


def get_from_objects_field_values(records, *fields, **kwargs):
    """Возвращает список.

    Элементы - кортежи значений полей fields списка объектов records.
    """
    return [
        get_field_values_from_object(obj, *fields, **kwargs) for obj in records
    ]


def get_field_values_from_dict(data, *fields, **kwargs):
    """Возвращает кортеж значений полей из словаря data."""
    if not fields:
        return None
    try:
        field_values = []
        for key in fields:
            value = data[key]
            if isinstance(value, object) and hasattr(value, "id"):
                value = int(value.id)
            field_values.append(value)
        if kwargs.get("only_one_field"):
            return field_values[0]
        return tuple(field_values)
    except (TypeError, KeyError, ValueError):
        return None


def get_from_dicts_field_values(records, *fields, **kwargs):
    """Возвращает список.

    Элементы кортежи значений
    полей fields из списка словарей records.
    """
    return [
        get_field_values_from_dict(data, *fields, **kwargs) for data in records
    ]


def create_ordered_dicts_from_objects(objs, key):
    """Создает список словарей на основании списка объектов."""
    return [OrderedDict({key: obj}) for obj in objs]


def get_object_or_400(klass, *args, **kwargs):
    """Возвращает один объект модели, в противном случае 400 ошибка."""
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist as e:
        raise ParseError(*e.args)
    except queryset.model.MultipleObjectsReturned as e:
        raise ParseError(*e.args)


def get_object_or_403(klass, *args, **kwargs):
    """Возвращает один объект модели, в противном случае 403 ошибка."""
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist as e:
        raise PermissionDenied(*e.args)
    except queryset.model.MultipleObjectsReturned as e:
        raise PermissionDenied(*e.args)


def is_exists_user_info(queryset, user):
    """Проверка наличия связаной информации по пользователю в queryset."""
    if user.is_anonymous:
        return False
    return queryset.filter(pk=user.pk).exists()
