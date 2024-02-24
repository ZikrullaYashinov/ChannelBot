import logging

from aiogram import Dispatcher

from data.config import ADMINS
from data.models.user import User
from loader import dp


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Bot ishga tushdi")

        except Exception as err:
            logging.exception(err)


async def on_add_user_notify(user: User, count: int):
    for admin in ADMINS:
        try:
            text = f"🆕 Yangi Foydalanuvchi!\nUmumiy: [{count}]\nIsmi: {user.first_name}\n@{user.username}"
            await dp.bot.send_message(admin, text)
        except Exception as err:
            logging.exception(err)


async def on_error_notify(error: str):
    for admin in DEVELOPERS:
        try:
            await dp.bot.send_message(admin, error)
        except Exception as err:
            logging.exception(err)
