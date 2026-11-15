from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from database.db import get_user_city
from keyboards.main_menu import main_menu

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    city = await get_user_city(message.from_user.id)

    if city:
        text = (
            f"Привет! Это VibeCity 👋\n"
            f"Твой выбранный город: {city}.\n"
            "Выбирай, что будем искать!"
        )
    else:
        text = (
            "Привет! Добро пожаловать в VibeCity! 👋\n"
            "Я помогу находить интересные места "
            "для отдыха и развлечений.\n"
            "Для начала выбери свой город."
        )

    await message.answer(
        text,
        reply_markup=main_menu()
    )