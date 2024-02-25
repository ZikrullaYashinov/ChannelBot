from aiogram import types

from handlers.users.help import bot_help
from handlers.users.start import bot_start, action_cancel
from loader import dp
from utils.constants import Command


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    if message.text == Command.start:
        await bot_start(message)
    elif message.text == Command.help:
        await bot_help(message)
    elif message.text == Command.cancel:
        await action_cancel(message)
    else:
        await message.answer(message.text)
