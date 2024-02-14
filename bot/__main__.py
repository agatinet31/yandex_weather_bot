import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.telegram import TelegramAPIServer
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web
from fluent.runtime import FluentLocalization, FluentResourceLoader

from bot.commands import set_bot_commands
from bot.core.config import settings
from bot.handlers import setup_routers
from bot.middlewares import L10nMiddleware

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    locales_dir = Path(__file__).parent.joinpath("locales")
    l10n_loader = FluentResourceLoader(str(locales_dir) + "/{locale}")
    l10n = FluentLocalization(
        ["ru"], ["strings.ftl", "errors.ftl"], l10n_loader
    )
    bot = Bot(token=settings.bot_token.get_secret_value())
    dp = Dispatcher()
    router = setup_routers()
    dp.include_router(router)
    if settings.custom_bot_api:
        bot.session.api = TelegramAPIServer.from_base(
            settings.custom_bot_api, is_local=True
        )
    dp.update.middleware(L10nMiddleware(l10n))
    await set_bot_commands(bot)
    try:
        if not settings.webhook_domain:
            await bot.delete_webhook()
            await dp.start_polling(
                bot, allowed_updates=dp.resolve_used_update_types()
            )
        else:
            aiohttp_logger = logging.getLogger("aiohttp.access")
            aiohttp_logger.setLevel(logging.CRITICAL)
            await bot.set_webhook(
                url=settings.webhook_domain + settings.webhook_path,
                drop_pending_updates=True,
                allowed_updates=dp.resolve_used_update_types(),
            )
            app = web.Application()
            SimpleRequestHandler(dispatcher=dp, bot=bot).register(
                app, path=settings.webhook_path
            )
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(
                runner, host=settings.app_host, port=settings.app_port
            )
            await site.start()
            await asyncio.Event().wait()
    finally:
        await bot.session.close()


try:
    asyncio.run(main())
except (KeyboardInterrupt, SystemExit):
    logger.error("Bot stopped!")
