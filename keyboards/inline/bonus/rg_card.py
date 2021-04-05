from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Emoji import emoji
from keyboards.inline.callback_datas import post_callback

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=f'👩🏻‍💻Зареєструвати', callback_data=post_callback.new(action='add_replace_card')),
        ],
        [
            InlineKeyboardButton(text=f'Повернутися в меню{emoji.left_hand}',
                                 callback_data=post_callback.new(action='back_to_menu')),
        ],
    ]
)

# gt - google table
keyboard_without_gt = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=f'💳 Додати картку',
                                 callback_data=post_callback.new(action='add_card')),
        ],
        [
            InlineKeyboardButton(text=f'Повернутися в меню{emoji.left_hand}',
                                 callback_data=post_callback.new(action='back_to_menu')),
        ],
    ]
)
