from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from database.db import save_user_city
from keyboards.main_menu import main_menu

router = Router()


class CityForm(StatesGroup):
    waiting_for_city = State()


@router.message(F.text == "🏙 Выбрать город")
async def ask_city(message: Message, state: FSMContext):
    await state.set_state(CityForm.waiting_for_city)

    await message.answer(
        "Напиши название своего города.\n"
        "Например: Ханты-Мансийск"
    )


@router.message(CityForm.waiting_for_city)
async def receive_city(message: Message, state: FSMContext):
    city = (message.text or "").strip()

    if len(city) < 2 or len(city) > 60:
        await message.answer(
            "Название города должно содержать "
            "от 2 до 60 символов. Попробуй ещё раз."
        )
        return

    await save_user_city(
        message.from_user.id,
        city
    )

    await state.clear()

    await message.answer(
        f"Город сохранён: {city} 📍",
        reply_markup=main_menu()
    )