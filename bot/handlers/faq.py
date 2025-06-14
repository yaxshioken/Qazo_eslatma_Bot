from aiogram import F, types
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent

from bot.buttons.inline import back_keyboard
from bot.dispatcher import dp
from db.config import DB

db=DB()
@dp.callback_query(F.data == "faq")
async def show_faq(callback: CallbackQuery):
    text = "<b>FAQ – Ko‘p so‘raladigan savollar</b>\n\n" \
           "1. Qazo nima?\n" \
           "– Qazo – vaqtida o‘qilmagan namozning qarzidir.\n\n" \
           "2. Qazo namozini qanday o‘qish kerak?\n" \
           "– Oddiy farz namoz kabi, faqat niyatda 'qazo' deb aytiladi."
    await callback.message.edit_text(text, parse_mode="HTML",reply_markup=back_keyboard)
    await callback.answer()


@dp.inline_query()
async def inline_faq_search(inline_query: types.InlineQuery):
    query = inline_query.query.lower()
    results = []

    faqs = db.search_faqs(query)

    for faq in faqs:
        results.append(
            InlineQueryResultArticle(
                id=str(faq["id"]),
                title=faq["question"],
                input_message_content=InputTextMessageContent(
                    message_text=faq["question"]
                ),
                description="Javobni olish uchun bosing"
            )
        )

    await inline_query.answer(results, cache_time=1)

@dp.message(F.text.in_([faq["question"] for faq in db.get_all_faqs()]))
async def show_faq_answer(message: types.Message):
    faq = db.get_faq_by_question(message.text)

    if faq["answer_video_file_id"]:
        await message.answer_video(
            video=faq["answer_video_file_id"],
            caption=faq["question"]
        )
    elif faq["answer_text"]:
        await message.answer(f"<b>{faq['question']}</b>\n\n{faq['answer_text']}", parse_mode="HTML")
    else:
        await message.answer("Bu savolga hali javob mavjud emas.")