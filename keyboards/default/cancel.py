from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.constants import Command

buttonTextCancel = [
    [Command.cancel],
]
cancelKeyboardBtn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
for i in buttonTextCancel:
    cancelKeyboardBtn.add(*i)
