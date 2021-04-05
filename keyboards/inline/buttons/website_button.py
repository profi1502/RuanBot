from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import RUAN_URL

website_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Перейти на сайт', url=RUAN_URL),
        ]
    ]
)
