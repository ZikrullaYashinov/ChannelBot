from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.constants import Command

buttons = [
    InlineKeyboardButton("➕ Zikrulla Production", 'https://t.me/Zikrulla_Production'),
    InlineKeyboardButton("✅ A'zo bo'ldim", callback_data=Command.checkMember),
]
keyboardChannel = InlineKeyboardMarkup(row_width=1)
keyboardChannel.add(*buttons)
