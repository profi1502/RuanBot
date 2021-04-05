from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import INSTAGRAM_URL, FACEBOOK_URL

social_network_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Instagram', url=INSTAGRAM_URL),
        ],
        [
            InlineKeyboardButton('Facebook', url=FACEBOOK_URL),
        ]
    ]
)
