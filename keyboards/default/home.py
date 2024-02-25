from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.constants import Command

buttons = [
    [Command.quizEnUz],
    [Command.quizUzEn],
]
keyboardBtnCancel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
for i in buttons:
    keyboardBtnCancel.add(*i)
