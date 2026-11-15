from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from database.db import get_user_city
from keyboards.categories import categories_keyboard

router = Router()


CATEGORY_NAMES = {
    "cafes": "Кафе и рестораны",
    "entertainment": "Развлечения",
    "parks": "Парки и природа",
    "games": "Игры и досуг",
    "attractions": "Достопримечательности",
    "shops": "Магазины"
}


@router.message(F.text == "📍 Категории")
async def show_categories(message: Message):
    city = await get_user_city(message.from_user.id)

    if not city:
        await message.answer(
            "Сначала выбери город кнопкой "
            "«🏙 Выбрать город»."
        )
        return

    await message.answer(
        f"Выбери категорию для города {city}:",
        reply_markup=categories_keyboard()
    )


@router.callback_query(F.data.startswith("category:"))
async def select_category(callback: CallbackQuery):
    category_key = callback.data.split(":", maxsplit=1)[1]

    category_name = CATEGORY_NAMES.get(category_key)

    if not category_name:
        await callback.answer(
            "Неизвестная категория.",
            show_alert=True
        )
        return

    city = await get_user_city(callback.from_user.id)

    if not city:
        await callback.answer(
            "Сначала выбери город.",
            show_alert=True
        )
        return

    await callback.answer()

    await callback.message.answer(
        f"Ты выбрал: {category_name}.\n"
        f"Город: {city}.\n\n"
        "Скоро здесь появятся реальные места "
        "и их рейтинги. Пока мы создаём основу VibeCity."
    )