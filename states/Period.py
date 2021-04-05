from aiogram.dispatcher.filters.state import StatesGroup, State


class PeriodState(StatesGroup):
    EnterDate = State()
