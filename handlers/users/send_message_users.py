from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.admin import bot_cmd_admin
from loader import dp, bot, db
from states.states import OtherStates
from utils.constants import Command
from utils.notify_admins import on_error_notify


@dp.message_handler(state=OtherStates.messageUsers,
                    content_types=['text', 'photo', 'video', 'audio', 'voice', 'document', 'sticker'])
async def messageUsers(message: types.Message, state: FSMContext):
    if message.text == Command.cancel:
        await state.reset_state()
        await bot_cmd_admin(message)
    else:
        count = 0
        blockedCount = 0
        if message.content_type == 'text':
            for userId in db.get_users_user_id():
                try:
                    result = await bot.send_message(userId[0], message.text)
                    if result:
                        count += 1
                except:
                    blockedCount += 1
                    db.updateUserBlocked(userId=userId[0], isBlocked=True)
            await state.reset_state()
        elif message.content_type == 'photo':
            photo = message.photo[-1]
            file_id = photo.file_id
            file_info = await bot.get_file(file_id)
            file_path = file_info.file_path
            format_type = file_path.split('.')[-1]
            print(format_type)
            await message.photo[-1].download(f"dir/photo.{format_type}")
            for userId in db.get_users_user_id():
                try:
                    photo = open(f"dir/photo.{format_type}", "rb")
                    result = await bot.send_photo(chat_id=userId[0], photo=photo, caption=message.caption)
                    if result:
                        count += 1
                except Exception as e:
                    await on_error_notify(e)
                    blockedCount += 1
                    db.updateUserBlocked(userId=userId[0], isBlocked=True)
            await state.reset_state()
        await bot.send_message(
            message.chat.id,
            f"Muvofaqyatli yuborilgan foydalanuvchilar: <b>{count}</b> ✅"
            f"\nBloklagan foydalanuvchilar: <b>{blockedCount}</b> ❌",
            parse_mode='html',
            reply_markup=types.ReplyKeyboardRemove()
        )
