from aiogram import types
from data.config import channels
from loader import bot


async def isChannelMember(message: types.Message):
    isMember = True
    for channel in channels:
        status = await bot.get_chat_member(chat_id=channel, user_id=message.chat.id)
        status = status.status
        if 'left' == status:
            isMember = False
            break
    return isMember
