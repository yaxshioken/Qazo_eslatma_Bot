from aiogram import F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.buttons.inline import calc_qazo, one_less_keyboard, asosiy_menyu, welcome
from bot.buttons.umumiy_qazolari import create_qazo_keyboard
from bot.dispatcher import dp
from db.config import DB

db = DB()


class QazoStates(StatesGroup):
    waiting_years = State()
    waiting_days = State()


@dp.callback_query(F.data == "qazo_hisobla")
async def handle_qazo_duolar(callback: CallbackQuery):
    await callback.message.edit_text(
        text=(
            "🕌 *Qazo namoz* — bu o‘z vaqtida o‘qilmagan farz yoki vojib namozlarni keyinchalik to‘ldirib o‘qishdir.\n\n"
            "Agar sababsiz yoki sababli o‘tkazib yuborilgan bo‘lsa, u *qazo* bo‘ladi va tezroq o‘qilishi lozim.\n\n"
            "*Muhim qismlar:*"
            "- Farz va vojib namozlar\n"
            "- Balog‘at va niyat\n"
            "- Shayx ma’ruzalari\n\n"
            "Qazo namozlaringizni hisoblashni boshlash uchun tugmani bosing 👇"),
        parse_mode="Markdown",
        reply_markup=calc_qazo
    )
    await callback.answer()


@dp.callback_query(F.data == "qazolarini_hisoblash")
async def ask_years(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=("📅 Necha yil qazo borligini kiriting? Masalan, 2019–2024 oralig‘ida `5` deb yozing.\n"
              "❗️ Faqat butun son kiriting."),
        parse_mode="Markdown",
        reply_markup=one_less_keyboard
    )
    await state.set_state(QazoStates.waiting_years)
    await callback.answer()


@dp.message(F.content_type == "text", QazoStates.waiting_years)
async def process_years(message: Message, state: FSMContext):
    try:
        years = int(message.text)
    except ValueError:
        return await message.reply("Iltimos, faqat raqam kiriting: yil sonini yuboring.")

    await state.update_data(years=years)
    await message.answer("📆 Endi necha kundik qazo bor? 0–364 oralig‘idagi sonni kiriting.")
    await state.set_state(QazoStates.waiting_days)


@dp.message(F.content_type == "text", QazoStates.waiting_days)
async def process_days(message: Message, state: FSMContext):
    data = await state.get_data()
    years = data.get("years", 0)
    try:
        days = int(message.text)
        if not 0 <= days <= 364:
            raise ValueError
    except ValueError:
        return await message.reply("Iltimos, 0 dan 364 gacha butun son kiriting.")

    total_days = years * 365 + days
    updated = db.qazolarni_qoshish(
        telegram_id=message.from_user.id, qaza=total_days)
    await message.answer("Muvaffaqiyatli  yangilandi", reply_markup=create_qazo_keyboard(message.from_user.id))
    await state.clear()


@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Asosiy menyu:", reply_markup=asosiy_menyu)

@dp.callback_query(F.data=="back")
async def back(callback: CallbackQuery, state: FSMContext):
    await callback.answer(
        "Menyulardan birini tanlang",reply_markup=welcome
    )
@dp.callback_query(F.data == "one_less")
async def start_adjust(callback: CallbackQuery):
    await callback.message.edit_text("Qazo namozlarni tahrirlash:",
                                     reply_markup=create_qazo_keyboard(callback.message.from_user.id))
    await callback.answer()


@dp.callback_query(
    F.data.startswith("increase:") | F.data.startswith("decrease:") | F.data == "back"
)
async def handle_qazo_adjust(callback: CallbackQuery):
    data = callback.data
    if data == "back":
        await callback.message.edit_text("Asosiy menyu:", reply_markup=calc_qazo)
        return await callback.answer()

    action, namoz = data.split(":")
    user_id = callback.from_user.id
    qazo_data = db.get_all_qazos(user_id)
    current = qazo_data.get(namoz, 0)
    new = current + 1 if action == "increase" else max(0, current - 1)

    if new != current:
        db.update_single_qazo(user_id, namoz, new)
        # yangilangan klaviaturani yuborish
        await callback.message.edit_reply_markup(reply_markup=create_qazo_keyboard(user_id))
    await callback.answer()


@dp.message(F.text == "create_qazo_keyboard")
async def message_create_keyboard(message: Message):
    markup = create_qazo_keyboard(message.from_user.id)
    await message.answer("Bu yerda qazo namozlarni tahrirlash klaviaturasi:", reply_markup=markup)
