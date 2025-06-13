import os

from aiogram import Dispatcher, Bot


dp = Dispatcher()


async def on_startup(bot: Bot):
    await bot.send_message(chat_id=os.getenv("USER_ID"), text="Bot Ishga tushdi ✅")


async def on_shutdown(bot: Bot):
    await bot.send_message(chat_id=os.getenv("USER_ID"), text="Bot To'xtadi ⚠️")
    await bot.session.close()
