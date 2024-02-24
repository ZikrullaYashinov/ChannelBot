from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import BOT_USERNAME
from handlers.users.start import bot_start
from keyboards.default.cancel import cancelKeyboardBtn
from keyboards.inline.inline_admin import inlineBtnAdminCommands
from loader import dp, db
from states.states import OtherStates
from utils.constants import Command, Keys
from utils.notify_admins import on_error_notify


@dp.callback_query_handler(state='*')
async def callback(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    if data == Command.statistics:
        usersCount, blockedCount = db.get_users_count()
        sendText = (f"📊 Foydalanuvchilaringiz haqida statistika"
                    f"\n\n▪️Foydalanuvchilar: {usersCount}"
                    f"\n▫️Faol: {usersCount - blockedCount}"
                    f"\n▫️O'chirilgan: {blockedCount}"
                    f"\n\n🤖 Bot: {BOT_USERNAME}")
        await call.message.answer(sendText)
    elif data == Command.sendUsers:
        sendText = 'Yaxshi xabaringizni yuboring!'
        await call.message.answer(sendText, reply_markup=cancelKeyboardBtn)
        await OtherStates.messageUsers.set()
    elif data == Command.checkMember:
        await bot_start(message=call.message)
    else:
        sendText = ("Nimadir bo'ldi shekilli lekin men tushunmadim dasturchi bir nimani esdan chiqardi shekilli u ham "
                    "banda xato qiladi to'g'ri tushunasiz degan umiddaman")
        await call.message.answer(sendText)
    await call.answer()
