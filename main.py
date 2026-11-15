
import logging
import os
import re

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)

from config import BOT_TOKEN
from database.db import init_db

from handlers.start import router as start_router
from handlers.city import router as city_router
from handlers.categories import router as categories_router


# Настройки Webhook
WEBHOOK_PATH = "/telegram/webhook"
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
BASE_WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL")
PORT = int(os.getenv("PORT", "10000"))


# Проверка работоспособности сервера
async def health_check(request: web.Request) -> web.Response:
    return web.json_response({
        "status": "ok",
        "service": "VibeCity"
    })


# Действия при запуске приложения
async def on_startup(bot: Bot) -> None:
    await init_db()

    if not BASE_WEBHOOK_URL:
        raise RuntimeError(
            "RENDER_EXTERNAL_URL is missing."
        )

    webhook_url = (
        f"{BASE_WEBHOOK_URL.rstrip('/')}{WEBHOOK_PATH}"
    )

    await bot.set_webhook(
        url=webhook_url,
        secret_token=WEBHOOK_SECRET,
        drop_pending_updates=False,
    )

    logging.info("Webhook configured: %s", webhook_url)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        ),
    )

    if not WEBHOOK_SECRET:
        raise RuntimeError(
            "WEBHOOK_SECRET is missing."
        )

    if not re.fullmatch(
        r"[A-Za-z0-9_-]{1,256}",
        WEBHOOK_SECRET
    ):
        raise RuntimeError(
            "Invalid WEBHOOK_SECRET format."
        )

    bot = Bot(token=BOT_TOKEN)

    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем обработчики VibeCity
    dp.include_router(start_router)
    dp.include_router(city_router)
    dp.include_router(categories_router)

    # Регистрируем запуск
    dp.startup.register(on_startup)

    # Создаём HTTP-приложение
    app = web.Application()

    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)

    # Подключаем Telegram Webhook
    webhook_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )

    webhook_handler.register(
        app,
        path=WEBHOOK_PATH
    )

    # Подключаем события aiogram
    setup_application(app, dp, bot=bot)

    # Запускаем сервер Render
    web.run_app(
        app,
        host="0.0.0.0",
        port=PORT
    )


if __name__ == "__main__":
    main()
