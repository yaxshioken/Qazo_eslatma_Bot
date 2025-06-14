from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from bot.buttons.inline import hisobla
from bot.dispatcher import dp


@dp.callback_query(F.data == "qazo_calc")
async def handle_qazo_duolar(callback: CallbackQuery):
    await callback.message.message.edit_text(
        text="🕌 *Qazo namoz* — bu o‘z vaqtida o‘qilmagan farz yoki vojib namozlarni keyinchalik to‘ldirib o‘qishdir.\n\n"
             "Agar biror sabab bilan yoki sabab bo‘lmasdan namoz o‘tkazib yuborilgan bo‘lsa, u *qazo* bo‘ladi va iloji boricha tezroq o‘qilishi kerak.\n\n"
             "*Avvalo birinchi bir necha muhim qismlarni bilishingiz kerak:*\n"
             "- Namozning farz bo‘lishi\n"
             "- Balog‘at yosh\n"
             "- Shayx video rolliklari\n"
             "Qazo namozlaringizni hisoblashni boshlash uchun quyidagi tugmani bosing 👇",
        parse_mode="Markdown", reply_markup=hisobla
    )


@dp.callback_query(F.data == "start_calculation")
async def start_calculation(callback: CallbackQuery):
    await callback.message.message.edit_text(
        text="😇 *Rahmoniy* — qazo namozlarini o‘qishni xohlaydigan, Allohdan qo‘rquv bilan yondashadigan kishi.\n"
             "😈 *Shaytoniy* — dangasalik yoki unutish bilan qazo namozni e’tiborsiz qoldiradigan yondashuv.\n\n"
             "📅 Sizda necha yil qazo borligini kiriting. Masalan, agar 2019–2024 oralig‘ida namoz o‘qilmagan bo‘lsa, `5` deb yozing.\n\n"
             "❗️ *Faqat raqam bilan yil sonini kiriting.*",
        parse_mode="Markdown",
    )
@dp.callback_query(F.data == "one_less")
async def one_less(message:Message,callback: CallbackQuery):
    await callback.message.message.edit_text(
        "🗓 Sizda necha yillik qazo bor? Faqat yillar sonini yozing (masalan: `3`)."
    )
    year=int(message.text)
    user=message.from_user.id
    qaza=year*365
