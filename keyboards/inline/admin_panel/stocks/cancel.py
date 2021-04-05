from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


#  в каждом названии клавиатуры, в начале ставь название файла, в нашем случае - CANCEL


editing_text_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Скасувати редагування'),
        ],
    ],
    resize_keyboard=True
)


deleting_photo_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Скасувати видалення'),
        ],
    ],
    resize_keyboard=True
)