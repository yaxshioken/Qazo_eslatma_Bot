import datetime

import pytz
import requests
from aiogram import F
from aiogram.types import CallbackQuery

from bot.buttons.inline import back_keyboard
from bot.dispatcher import dp


@dp.callback_query(F.data == "namoz_vaqti")
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
