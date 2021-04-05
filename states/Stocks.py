from aiogram.dispatcher.filters.state import StatesGroup, State


class Stocks(StatesGroup):
    editStockText = State()
    editStockPhoto = State()

    deleteStockPhoto = State()

    editPharmacyPhoto = State()
    deletePharmacyPhoto = State()
