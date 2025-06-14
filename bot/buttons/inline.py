from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

builder = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🕌 Qazolarim", callback_data="qazolar"),
     InlineKeyboardButton(text="🕒 Namoz vaqtlari", callback_data="namoz_times")
     ],
    [InlineKeyboardButton(text="❓ Ko‘p berilgan savollar", callback_data="faq"),
     InlineKeyboardButton(text="ℹ️ Bot haqida", callback_data="about_bot")],

    [InlineKeyboardButton(text="🌐 Saytga o‘tish", url="https://shopick.uz")]
])
qazos = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🕌 Qazo hisoblash", callback_data="qazo_calc")],
    [InlineKeyboardButton(text="🧎‍♂️ Alhamdulillah, qazoim yo‘q", callback_data="iamnot_qazo")],
    [InlineKeyboardButton(text="🎓 Qazo ibodatlari haqida", callback_data="what_qazo")]

])


calc_qazo = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🕌 Qazo namozlarimni  hisoblash", callback_data="hisoblash_qazoni")],
    [InlineKeyboardButton(text="🧎‍♂️ Alhamdulillah, qazoim yo‘q", callback_data="not_qazo")],
    [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_menu")]
])
hisobla = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🧮 Hisoblashni boshlash",
                callback_data="start_calculation"
            )
        ]
    ]
)
one_less_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📆 Menda yildan kam qazo bor",
                callback_data="one_less"
            )
        ]
    ]
)
back_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔙 Orqaga",
                callback_data="back"
            )
        ]
    ]
)