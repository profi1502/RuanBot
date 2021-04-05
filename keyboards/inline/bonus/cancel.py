from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from Emoji import emoji

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(f'Повернутися в меню{emoji.left_hand}'),
        ],
    ],
    resize_keyboard=True
)
