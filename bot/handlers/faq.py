from aiogram import F, types
from aiogram.types import CallbackQuery, InlineQueryResultArticle, InputTextMessageContent

from bot.buttons.inline import back_keyboard, asosiy_menyu
from bot.dispatcher import dp
from db.config import DB

db = DB()


@dp.callback_query(F.data == "savol")
async def show_faq(callback: CallbackQuery):
    text = "<b>FAQ – Ko‘p so‘raladigan savollar</b>\n\n" \
           "1. Qazo nima?\n" \
           "– Qazo – vaqtida o‘qilmagan namozning qarzidir.\n\n" \
           "2. Qazo namozini qanday o‘qish kerak?\n" \
           "– Oddiy farz namoz kabi, faqat niyatda 'qazo' deb aytiladi."
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_keyboard)
    await callback.answer()


@dp.callback_query(F.data == "back")
async def back(callback: CallbackQuery):
    await callback.message.edit_text(text="Asosiy Menyu:", reply_markup=asosiy_menyu)
