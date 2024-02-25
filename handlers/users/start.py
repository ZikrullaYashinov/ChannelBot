import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.utils import deep_linking
from data.config import BOT_USERNAME
from data.models.quiz import Quiz
from keyboards.default.home import keyboardBtnCancel
from data.models.user import User
from filters.filter_members import isChannelMember
from keyboards.inline.inline_member import keyboardChannel
from loader import dp, db, bot
from utils.constants import Command
from utils.notify_admins import on_add_user_notify


async def showChannel(message: types.Message):
    await message.answer(
        f"Bizni qo'llab quvvatlash va botdan foydalanish uchun telegram kanalimizga obuna bo'ling va pastdagi "
        f"\n<b>✅ A'zo bo'ldim</b> tugmasini bosing!!",
        reply_markup=keyboardChannel)


async def action_cancel(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer("Bekor qilindi! /start", reply_markup=remove_keyboard)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    fromUser = message.from_user
    user = User(fromUser.id, fromUser.first_name, fromUser.last_name, fromUser.username, 0, False)
    if not await isChannelMember(message):
        await showChannel(message)
    else:
        await message.answer(
            f"Assalomu alaykum 👋", reply_markup=keyboardBtnCancel)

    has = db.has_user(user.id)
    if not has and not message.from_user.is_bot:
        db.insertUser(user)
        usersCount, blockedCount = db.get_users_count()
        await on_add_user_notify(user, usersCount)
    elif not message.from_user.is_bot:
        oldUser = db.getUser(user.id)
        if oldUser.isBlocked:
            db.updateUser(user)
