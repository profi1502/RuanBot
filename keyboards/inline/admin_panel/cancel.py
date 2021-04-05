from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Назад'),
        ],
    ],
    resize_keyboard=True,
)
