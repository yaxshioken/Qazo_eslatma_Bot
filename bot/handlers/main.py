from aiogram import Bot, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.buttons.inline import asosiy_menyu, welcome
from bot.dispatcher import dp
from db.config import DB

db = DB()



@dp.message(F.text=="/start")
async def start(message: Message, bot: Bot):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    if db.check_user_exist(message.from_user.id):

        await message.answer(
            f"<b>Assalomu alaykum <b>  {last_name}</b>!😊</b>\n\n"
            "Yana siz bilan ko‘rishganimizdan juda xursandmiz!\n"
            "Sizga qanday yordam bera olishimiz mumkin?\n"
            "Quyidagi tugmalardan birini tanlang va davom eting 👇",
            reply_markup=asosiy_menyu,
            parse_mode="HTML",
        )
    else:
        username = message.from_user.username
        telegram_id = message.from_user.id
        await message.answer(
            f"<b>Assalomu alaykum <b>{first_name}  {last_name}</b>! 😊</b>\n"
            "🤲 Ushbu bot sizga namoz qazoingizni doimiy ravishda hisoblab borishda yordam beradi.\n"
            "📌 Dastlab, sizda qancha qazo namoz borligini aniqlab olaylik.\n"
            "📤 Hisob-kitobni boshlash uchun pastdagi <b>\"Qazo hisoblash\"</b> tugmasini bosing.",
            reply_markup=welcome,
            parse_mode="HTML"
        )
        db.insert_user(username=username, telegram_id=telegram_id, first_name=first_name)
        db.create_null_qazo(telegram_id)
