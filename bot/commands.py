from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_bot_commands(bot: Bot):
    usercommands = [
        BotCommand(
            command="help", description="Справка по использованию бота"
        ),
    ]
    await bot.set_my_commands(usercommands, scope=BotCommandScopeDefault())
