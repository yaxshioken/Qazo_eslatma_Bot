from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

builder = InlineKeyboardBuilder()
builder.button(text="🕌 Qazo duolarim", callback_data="qazo_duolar")
builder.button(text="❓ Ko‘p berilgan savollar", callback_data="faq")
builder.button(text="🕒 Namoz vaqtlari", callback_data="namoz_times")
builder.button(text="ℹ️ Bot haqida", callback_data="about_bot")

builder.row(InlineKeyboardButton(text="🌐 Saytga o‘tish", url="https://google.com"))

builder.adjust(2, 2, 1)
builder = builder.as_markup()

qazos = InlineKeyboardBuilder()
qazos.button(text="🕌 Qazo hisoblash", callback_data="qazo_calc")
qazos.button(text="🎓 Qazo ibodatlari haqida", callback_data="what_qazo")
qazos.button(text="🧎‍♂️ Alhamdulillah, qazoim yo‘q", callback_data="iamnot_qazo")
qazos = qazos.as_markup()

calc_qazo = InlineKeyboardBuilder()
calc_qazo.button(text="🕌 Qazo hisoblash", callback_data="hisoblash_qazoni")
calc_qazo.button(text="🧎‍♂️ Alhamdulillah, qazoim yo‘q", callback_data="not_qazo")
