from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.constants import Command

buttons = [
    ["📊 Bot statistikasi", Command.statistics],
    ["📨 Foydalanuvchilarga xabar yuborish", Command.sendUsers],
]
inlineBtnAdminCommands = InlineKeyboardMarkup()
for i in buttons:
    inlineBtnAdminCommands.add(InlineKeyboardButton(text=i[0], callback_data=i[1]))
