import datetime

import pytz
import requests
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton

from bot.buttons.inline import builder, qazos, back_keyboard
from bot.dispatcher import dp
from db.config import DB
from utils.utils import Config


@dp.callback_query(F.data == "namoz_times")
async def prayer_times(callback: CallbackQuery):
    city = "Tashkent"
    today = datetime.datetime.now(pytz.timezone("Asia/Tashkent")).strftime("%Y-%m-%d")
    url = f"https://api.aladhan.com/v1/timingsByCity?city={city}&country=Uzbekistan&method=2&date={today}"
    resp = requests.get(url).json()
    timings = resp["data"]["timings"]
    text = f"<b>Namoz vaqtlari (Toshkent – {today})</b>\n"
    for name, time in timings.items():
        text += f"\n{name}: {time}"
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_keyboard)
    await callback.answer()


class QazoStates(StatesGroup):
    waiting_qazo = State()


@dp.callback_query(F.data == "qazo_calc")
async def ask_qazo(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "<b>Qazo nima?</b>\n\nQazo — bu vaqtida o‘qilmagan farz yoki vojib namozlarning qarzidir.\n"
        "Namozni belgilangan vaqtda o‘qish farzdir. Agar sababsiz o‘tkazib yuborilsa, keyinchalik qazo qilish lozim.\n\n"
        "Qancha qazo namozingiz borligini son bilan yozing:",
        reply_markup=qazos,
        parse_mode="HTML"
    )
    await state.set_state(QazoStates.waiting_qazo)
    await callback.answer()


@dp.callback_query(F.text, QazoStates.waiting_qazo)
async def save_qazo(message: Message, state: FSMContext):
    try:
        count = int(message.text)
    except ValueError:
        await message.answer("Iltimos, faqat son kiriting.")
        return

    date = datetime.datetime.now(pytz.timezone(Config.TIMEZONE)).strftime("%Y-%m-%d")
    DB().add_qazo(message.from_user.id, date, count)
    total = DB().get_qazo(message.from_user.id)

    await message.message.edit_text(
        f"Sizning jami qazo namozlaringiz: {total} ta",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Bosh menyu", callback_data="back_to_menu")]
        ])
    )
    await state.clear()
