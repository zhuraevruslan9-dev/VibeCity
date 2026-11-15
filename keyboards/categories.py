from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


def categories_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="☕ Кафе и рестораны",
                    callback_data="category:cafes"
                ),
                InlineKeyboardButton(
                    text="🎡 Развлечения",
                    callback_data="category:entertainment"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌳 Парки и природа",
                    callback_data="category:parks"
                ),
                InlineKeyboardButton(
                    text="🎮 Игры и досуг",
                    callback_data="category:games"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏛 Достопримечательности",
                    callback_data="category:attractions"
                ),
                InlineKeyboardButton(
                    text="🛍 Магазины",
                    callback_data="category:shops"
                )
            ]
        ]
    )