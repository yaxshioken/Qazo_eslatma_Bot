from aiogram import F
from aiogram.types import CallbackQuery

from bot.buttons.inline import builder
from bot.buttons.umumiy_qazolari import create_qazo_keyboard
from bot.dispatcher import dp
from db.config import DB

db = DB()


@dp.callback_query(F.data == "qazolar")
async def handle_qazo_duolar(callback: CallbackQuery):
    await callback.message.answer(
        "Sizning qazolaringiz :(",
        parse_mode="HTML", reply_markup=create_qazo_keyboard(callback.from_user.id)
    )
    await callback.answer()
    await callback.message.edit_reply_markup()

    @dp.callback_query(F.data == "back")
    async def handle_back(callback: CallbackQuery):
        await callback.message.edit_text("Asosiy menyu:", reply_markup=builder)
    @dp.callback_query(F.data.startswith("increase:") | F.data.startswith("decrease:"))
    async def handle_qazo_adjust(callback: CallbackQuery):
        action, namoz = callback.data.split(":")
        user_id = callback.from_user.id
        qazo_data = db.get_all_qazos(user_id)
        current_value = qazo_data.get(namoz, 0)
        new_value = current_value
        if action == "increase":
            new_value += 1
        elif action == "decrease" and current_value > 0:
            new_value -= 1

        if new_value != current_value:
            db.update_single_qazo(user_id, namoz, new_value)
            updated_keyboard = create_qazo_keyboard(user_id)

            await callback.message.edit_reply_markup(
                reply_markup=updated_keyboard
            )
        if callback.data =="back":
            await callback.message.answer(
                text="Siz Asosiy Menyudasiz!",reply_markup=builder)
        await callback.answer()
