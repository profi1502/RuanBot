from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

publish_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Запостити'),
        ],
    ],
    resize_keyboard=True
)


publish_button_pharmacy = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Запостити аптеку'),
        ],
    ],
    resize_keyboard=True
)
