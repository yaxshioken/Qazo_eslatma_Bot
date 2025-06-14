import datetime
import os

import pytz
import requests
from aiogram import Bot, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, \
    InputTextMessageContent
from pyexpat.errors import messages

from bot.buttons.inline import builder, qazos, calc_qazo
from bot.dispatcher import dp
from db.config import DB
from utils.utils import Config

db = DB()


@dp.message(CommandStart)
async def start(message: Message, bot: Bot):
    first_name = message.from_user.first_name
    if db.check_user_exist(message.from_user.id):

        await message.answer(
            f"<b>Assalomu alaykum <b>{first_name}</b>!😊</b>\n\n"
            "Yana siz bilan ko‘rishganimizdan juda xursandmiz!\n"
            "Sizga qanday yordam bera olishimiz mumkin?\n"
            "Quyidagi tugmalardan birini tanlang va davom eting 👇",
            reply_markup=builder,
            parse_mode="HTML",
        )
    else:
        username = message.from_user.username
        telegram_id = message.from_user.id
        await message.answer(
            f"<b>Assalomu alaykum <b>{first_name}</b>! 😊</b>\n"
            "🤲 Ushbu bot sizga namoz qazoingizni doimiy ravishda hisoblab borishda yordam beradi.\n"
            "📌 Dastlab, sizda qancha qazo namoz borligini aniqlab olaylik.\n"
            "📤 Hisob-kitobni boshlash uchun pastdagi <b>\"Qazo hisoblash\"</b> tugmasini bosing.",
            reply_markup=qazos,
            parse_mode="HTML"
        )
        db.insert_user(username=username, telegram_id=telegram_id, first_name=first_name)
        db.create_null_qazo(telegram_id)
@dp.callback_query(F.data=="back")
async def back(callback: CallbackQuery):
    await callback.message.edit_text(text="Siz Asosiy Menyudasiz", reply_markup=builder)

