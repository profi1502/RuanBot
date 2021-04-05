from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import post_callback

stat_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Кількість юзерів', callback_data=post_callback.new(action='count_users')),
            InlineKeyboardButton(text='Період', callback_data=post_callback.new(action='period'))
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data=post_callback.new(action='back_to_admin')),
        ],
    ]
)
