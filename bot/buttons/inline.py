from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

asosiy_menyu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🕌 Qazolar bo'limi", callback_data="qazolar_bo'limi"),
     InlineKeyboardButton(text="🕒 Namoz vaqtlari", callback_data="namoz_vaqti")
     ],
    [InlineKeyboardButton(text="❓ Ko‘p berilgan savollar", callback_data="savol"),
     InlineKeyboardButton(text="ℹ️ Bot haqida", callback_data="bot_haqida"), ],

    [InlineKeyboardButton(text="🌐 Saytga o‘tish", url="https://shopick.uz")]
])
welcome = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🕌 Qazolarim", callback_data="qazolarim"),
     InlineKeyboardButton(text="🔄 Qazo hisoblash", callback_data="qazo_hisobla")],
    [InlineKeyboardButton(text="🧎‍♂️ Alhamdulillah, qazoim yo‘q", callback_data="qazoim_yoq"),
     InlineKeyboardButton(text="🎓 Qazo ibodatlari haqida", callback_data="qazo_nima")]

])

calc_qazo = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🕌 Qazo namozlarimni  hisoblash", callback_data="qazolarini_hisoblash")],
    [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back")]
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

orqaga = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔙 Orqaga",
                callback_data="back_")
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
        ],
        [
            InlineKeyboardButton(
                text="🔙 Orqaga",
                callback_data="back"
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
