import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.models.dictionary import Dictionary
from handlers.users.call_back_data import generateQuiz, sendQuiz
from utils.constants import Command as cmd

from handlers.users.help import bot_help
from loader import dp, db
from filters.filter_admin import isAdmin
from keyboards.inline.inline_admin import inlineBtnAdminCommands
from states.states import OtherStates


@dp.message_handler(Command('admin'), state=None)
async def bot_cmd_admin(message: types.Message):
    if isAdmin(message.from_user.id):
        await message.answer("Siz adminsiz!", reply_markup=inlineBtnAdminCommands)
    else:
        await message.answer("Siz adminmassiz!")
        await bot_help(message)


@dp.message_handler(state=OtherStates.dictionaries)
async def bot_insert_dictionaries(message: types.Message, state: FSMContext):
    if message.text == cmd.cancel:
        await state.reset_state()
        await message.answer("Yaxshi", reply_markup=types.ReplyKeyboardRemove())
        await bot_cmd_admin(message)
    else:
        try:
            dictionaries = []
            lines = message.text.split('\n')
            for line in lines:
                key, value = line.split('/')
                dictionaries.append(Dictionary(key, value))
            db.insertDictionaries(dictionaries)
            await message.answer("Tayyor")
            await state.reset_state()
        except Exception as e:
            print(e)
            print(message.text)
            await message.answer("To'g'ri yubordingizmi?")


@dp.message_handler(state=OtherStates.dictionariesAndSend)
async def bot_insert_dictionaries(message: types.Message, state: FSMContext):
    if message.text == cmd.cancel:
        await state.reset_state()
        await message.answer("Yaxshi", reply_markup=types.ReplyKeyboardRemove())
        await bot_cmd_admin(message)
    else:
        try:
            dictionaries = []
            lines = message.text.split('\n')
            for line in lines:
                key, value = line.split('/')
                dictionaries.append(Dictionary(key, value))
            db.insertDictionaries(dictionaries)
            await message.answer("Tayyor")
            await state.reset_state()
            print(dictionaries)
            quizList = generateQuiz(dictionaries)
            print(quizList)
            for quiz in quizList:
                await sendQuiz(quiz)
        except Exception as e:
            print(e)
            print(message.text)
            await message.answer("To'g'ri yubordingizmi?")
