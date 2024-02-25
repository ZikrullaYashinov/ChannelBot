from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.constants import Command

buttons = [
    ["📊 Bot statistikasi", Command.statistics],
    ["📨 Foydalanuvchilarga xabar yuborish", Command.sendUsers],
    ["📋 Viktorina yuborish", Command.sendVictorina],
    ["➕ Lug'at qo'shish", Command.insertDictionary],
    ["➕ Lug'at qo'shish va kanalga yubor", Command.insertDictionaryAndSendChannel],
]
inlineBtnAdminCommands = InlineKeyboardMarkup()
for i in buttons:
    inlineBtnAdminCommands.add(InlineKeyboardButton(text=i[0], callback_data=i[1]))
