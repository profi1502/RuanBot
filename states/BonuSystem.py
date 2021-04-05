from aiogram.dispatcher.filters.state import StatesGroup, State


class Bonus(StatesGroup):
    EnterCard = State()
    EnterCardWithoutGT = State()
    EnterCardWithoutGT_check = State()
