from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import post_callback

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Сьогодні', callback_data=post_callback.new(action='period_today')),
        ],
        [
            InlineKeyboardButton(text='Поточний місяць', callback_data=post_callback.new(action='period_current_month'))
        ],
        [
            InlineKeyboardButton(text='Минулий місяць', callback_data=post_callback.new(action='period_last_month')),
        ],
        [
            InlineKeyboardButton(text='Довільний період', callback_data=post_callback.new(action='period_any'))
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data=post_callback.new(action='back_to_period'))
        ],
    ]
)
