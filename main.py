import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database.db import init_db

from handlers.start import router as start_router
from handlers.city import router as city_router
from handlers.categories import router as categories_router


async def main():
    logging.basicConfig(level=logging.INFO)

    await init_db()

    bot = Bot(token=BOT_TOKEN)

    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_router)
    dp.include_router(city_router)
    dp.include_router(categories_router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())