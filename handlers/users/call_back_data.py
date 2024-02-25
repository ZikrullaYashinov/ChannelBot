import random

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import BOT_USERNAME, channelsQuiz
from data.models.dictionary import Dictionary
from data.models.quiz import Quiz
from handlers.users.start import bot_start
from keyboards.default.cancel import keyboardBtnCancel
from keyboards.inline.inline_admin import inlineBtnAdminCommands
from loader import dp, db, bot
from states.states import OtherStates
from utils.constants import Command, Keys
from utils.notify_admins import on_error_notify

questions = [
    {
        'question': "O'zbekiston poytaxti qayer?",
        'options': ['Toshkent', 'Samarkand', 'Buxoro', 'Andijon'],
        'correct_option': 0  # To'g'ri javob variantining indeksi
    },
    {
        'question': "Dunyo chempionati qaysi sport turi uchun o'tkaziladi?",
        'options': ['Futbol', 'Basketbol', 'Tenis', 'Golf'],
        'correct_option': 0
    },
]


@dp.callback_query_handler()
async def callback(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    if data == Command.statistics:
        usersCount, blockedCount = db.get_users_count()
        dictionariesCount = db.get_dictionaries_count()
        sendText = (f"📊 Foydalanuvchilaringiz haqida statistika"
                    f"\n\n▪️Foydalanuvchilar: {usersCount}"
                    f"\n▫️Faol: {usersCount - blockedCount}"
                    f"\n▫️O'chirilgan: {blockedCount}"
                    f"\n\n▫️Lug'atlar soni: {dictionariesCount}"
                    f"\n\n🤖 Bot: {BOT_USERNAME}")
        await call.message.answer(sendText)
    elif data == Command.sendUsers:
        sendText = 'Yaxshi xabaringizni yuboring!'
        await call.message.answer(sendText, reply_markup=keyboardBtnCancel)
        await OtherStates.messageUsers.set()
    elif data == Command.checkMember:
        await bot_start(message=call.message)
    elif data == Command.sendVictorina:
        dictionaries = db.readRandomDictionaries()
        quizList = generateQuiz(dictionaries)
        # quizList = generateQuiz([
        #     Dictionary("apple", "olma"),
        #     Dictionary("orange", "apelsin"),
        #     Dictionary("banana", "banan"),
        #     Dictionary("tomato", "pamidor"),
        # ])
        for quiz in quizList:
            await sendQuiz(quiz)
    elif data == Command.insertDictionary:
        await call.message.answer("Lug'atlarni yozib yuboring!\nHar bitta lug'atni yangi qatordan kiriting\n\n"
                                  "Masalan:<b>\napple/olma\norange/apelsin</b>", reply_markup=keyboardBtnCancel)
        await OtherStates.dictionaries.set()
    elif data == Command.insertDictionaryAndSendChannel:
        await call.message.answer("Lug'atlarni yozib yuboring!\nHar bitta lug'atni yangi qatordan kiriting\n\n"
                                  "Masalan:<b>\napple/olma\norange/apelsin</b>", reply_markup=keyboardBtnCancel)
        await OtherStates.dictionariesAndSend.set()
    else:
        sendText = ("Nimadir bo'ldi shekilli lekin men tushunmadim dasturchi bir nimani esdan chiqardi shekilli u ham "
                    "banda xato qiladi to'g'ri tushunasiz degan umiddaman")
        await call.message.answer(sendText)
    await call.answer()


def generateQuiz(dictionaries: list[Dictionary], isKeyToValue=True) -> list[Quiz]:
    print(dictionaries)
    quizList = []
    if isKeyToValue:
        for dic in dictionaries:
            options = []
            dicList = dictionaries.copy()
            dicList.remove(dic)
            random.shuffle(dicList)
            for option in dicList:
                options.append(option.value)
                if len(options) == 3:
                    break
            options.append(dic.value)
            random.shuffle(options)
            correctVariant = options.index(dic.value)
            quizList.append(Quiz(
                question=dic.key,
                correct_option_id=correctVariant,
                options=options
            ))
    else:
        for dic in dictionaries:
            options = []
            dicList = dictionaries.copy()
            dicList.remove(dic)
            random.shuffle(dicList)
            for option in dicList:
                options.append(option.key)
                if len(options) == 3:
                    break
            options.append(dic.key)
            random.shuffle(options)
            correctVariant = options.index(dic.key)
            quizList.append(Quiz(
                question=dic.value,
                correct_option_id=correctVariant,
                options=options
            ))
    print(quizList)
    return quizList


async def sendQuiz(quiz: Quiz):
    for channel in channelsQuiz:
        await bot.send_poll(chat_id=channel, question=quiz.question,
                            is_anonymous=True, options=quiz.options, type="quiz",
                            correct_option_id=quiz.correct_option_id,
                            disable_notification=True, explanation=f"{BOT_USERNAME}")
