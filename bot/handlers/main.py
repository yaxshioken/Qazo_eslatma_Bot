import os

from aiogram import Bot
from aiogram.filters import CommandStart

from aiogram.types import Message

from bot.buttons.inline import builder, qazos
from bot.dispatcher import dp
from db.config import DB

db = DB()


@dp.message(CommandStart)
async def start(message: Message, bot: Bot):
    if db.check_user_exist(message.from_user.id):
        await message.answer("""
        <b>Assalomu alaykum! 😊</b>
        
        Yana siz bilan ko‘rishganimizdan juda xursandmiz!<br>
        Sizga qanday yordam bera olishimiz mumkin?<br><br>
        Quyidagi tugmalardan birini tanlang va davom eting 👇 
                """, reply_markup=builder, parse_mode="HTML")
    else:
        await message.answer("""<b>Assalomu alaykum! 😊</b>
        🤲 Ushbu bot sizga namoz qazoingizni doimiy ravishda hisoblab borishda yordam beradi.
        📌 Dastlab, sizda qancha qazo namoz borligini aniqlab olaylik.
        📤 Hisob-kitobni boshlash uchun pastdagi <b>"Qazo hisoblash"</b> tugmasini bosing.""", reply_markup=qazos)
