from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

stock_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Редагувати опис'),
            KeyboardButton('Додати фото'),
        ],
        [
            KeyboardButton('Видалити фото'),
            KeyboardButton('Видалити всі фото'),
        ],
        [
            KeyboardButton('Назад'),
        ],
    ],
    resize_keyboard=True
)
