from typing import Any

from httpx import AsyncClient, HTTPError

from bot.core.config import settings
from bot.core.exceptions import BotYandexWeatherError

REQUEST_HEADERS = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
}


def get_params_for_city(city: str) -> dict[str, Any]:
    return {"city": city}


async def get_weather_from_service(city: str) -> str:
    """Запрашивает информацию о погоде с сервиса."""
    try:
        async with AsyncClient() as client:
            response = await client.get(
                settings.url_weather_service,
                headers=REQUEST_HEADERS,
                params=get_params_for_city(city),
            )
            response.raise_for_status()
            weather = response.json()
            return (
                f"Температура: {weather['temp']}, "
                f"Давление: {weather['pressure_mm']}, "
                f"Скорость ветра: {weather['wind_speed']}"
            )
    except (HTTPError, KeyError, ValueError, OSError) as exc:
        raise BotYandexWeatherError from exc
