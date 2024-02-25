from aiogram import types

from handlers.users.call_back_data import generateQuiz, sendQuiz
from handlers.users.help import bot_help
from handlers.users.start import bot_start, action_cancel
from loader import dp, db
from utils.constants import Command


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    if message.text == Command.start:
        await bot_start(message)
    elif message.text == Command.help:
        await bot_help(message)
    elif message.text == Command.cancel:
        await action_cancel(message)
    elif message.text == Command.quizEnUz:
        dictionaries = db.readRandomDictionaries(5)
        quizList = generateQuiz(dictionaries)
        for quiz in quizList:
            await sendQuiz(quiz, False, message.chat.id)
    elif message.text == Command.quizUzEn:
        dictionaries = db.readRandomDictionaries(5)
        quizList = generateQuiz(dictionaries, False)
        for quiz in quizList:
            await sendQuiz(quiz, False, message.chat.id)
    else:
        await message.answer(message.text)
