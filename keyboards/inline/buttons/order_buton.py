from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import ORDER_URL

order_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Замовити', url=ORDER_URL),
        ]
    ]
)