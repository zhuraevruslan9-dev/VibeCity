from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup
)


def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🏙 Выбрать город"
                )
            ],
            [
                KeyboardButton(
                    text="📍 Категории"
                )
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )