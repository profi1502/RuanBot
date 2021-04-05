from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from Emoji import emoji


pharmacy_near_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(f'За координатами{emoji.earth}', request_location=True),
            KeyboardButton(f'Оберіть місто{emoji.keyboard}'),
        ],
        [
            KeyboardButton(f'Повернутися в меню{emoji.left_hand}'),
        ],
    ],
    resize_keyboard=True
)

