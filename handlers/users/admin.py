import os

from aiogram import types
from aiogram.dispatcher.filters import Command

from handlers.users.help import bot_help
from loader import dp, db
from filters.filter_admin import isAdmin
from keyboards.inline.inline_admin import inlineBtnAdminCommands


@dp.message_handler(Command('admin'), state=None)
async def bot_cmd_admin(message: types.Message):
    if isAdmin(message.from_user.id):
        await message.answer("Siz adminsiz!", reply_markup=inlineBtnAdminCommands)
    else:
        await message.answer("Siz adminmassiz!")
        await bot_help(message)


