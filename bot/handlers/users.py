import logging

from aiogram import Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    ContentType,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from fluent.runtime import FluentLocalization

from bot.core.exceptions import BotYandexWeatherError
from bot.services.weather import get_weather_from_service


class City(StatesGroup):
    city = State()


router = Router()
dp = Dispatcher()
logger = logging.getLogger(__name__)


@router.message(Command(commands=["help"]))
async def cmd_help(message: Message, l10n: FluentLocalization):
    """Справка по сервису."""
    await message.answer(l10n.format_value("help"))


@router.message(F.text.lower() == "узнать погоду")
async def question_city(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Введите свой город",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Command("start"))
async def cmd_start(message: Message, l10n: FluentLocalization):
    kb = [
        [
            KeyboardButton(text="Узнать погоду"),
        ],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Yandex погода",
    )
    await message.answer(
        "Интересно узнать погоду в твоем городе?", reply_markup=keyboard
    )


@router.message(F.text)
async def echo_with_weathe_info(message: Message):
    try:
        weather = await get_weather_from_service(message.text)
        await message.answer(weather)
    except BotYandexWeatherError:
        await message.answer(
            "Мне не удалось получить информацию о погоде с сервиса!"
        )


@router.message()
async def unsupported_types(message: Message, l10n: FluentLocalization):
    """Хэндлер на неподдерживаемые типы сообщений."""
    if message.content_type not in (
        ContentType.VIDEO_CHAT_STARTED,
        ContentType.VIDEO_CHAT_ENDED,
        ContentType.VIDEO_CHAT_PARTICIPANTS_INVITED,
        ContentType.MESSAGE_AUTO_DELETE_TIMER_CHANGED,
        ContentType.NEW_CHAT_PHOTO,
        ContentType.DELETE_CHAT_PHOTO,
        ContentType.SUCCESSFUL_PAYMENT,
    ):
        await message.reply(
            l10n.format_value("unsupported-message-type-error")
        )
