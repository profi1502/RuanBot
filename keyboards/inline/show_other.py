from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import post_callback

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Переглянути інші міста',
                                 callback_data=post_callback.new(action='show_other_city'))
        ],

    ]
)


choose_manually = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Переглянути інші міста',
                                 callback_data=post_callback.new(action='show_other_city'))
        ],

    ]
)