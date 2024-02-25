from aiogram.dispatcher.filters.state import StatesGroup, State


class OtherStates(StatesGroup):
    messageUsers = State()

    dictionaries = State()
    dictionariesAndSend = State()
