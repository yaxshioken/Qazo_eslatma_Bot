from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db.config import DB

db = DB()


def create_qazo_keyboard(user_id: int) -> InlineKeyboardMarkup:
    qazo_data = db.get_all_qazos(user_id)
    keyboard = []

    for namoz, count in qazo_data.items():
        row = [
            InlineKeyboardButton(text="-", callback_data=f"decrease:{namoz}"),
            InlineKeyboardButton(text=f"{namoz.capitalize()}: {count}", callback_data="ignore"),
            InlineKeyboardButton(text="+", callback_data=f"increase:{namoz}")
        ]
        keyboard.append(row)

    keyboard.append([
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
