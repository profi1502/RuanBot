from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import post_callback

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Так', callback_data=post_callback.new(action='yes')),
            InlineKeyboardButton(text='Ні', callback_data=post_callback.new(action='no')),
        ],

    ]
)

keyboard_without_gt = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Так', callback_data=post_callback.new(action='yes_without_gt')),
            InlineKeyboardButton(text='Ні', callback_data=post_callback.new(action='no')),
        ],

    ]
)