from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Emoji import emoji
from keyboards.inline.callback_datas import post_callback

bonus_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=f'💵 Перевірити баланс', callback_data=post_callback.new(action='check_balance')),
        ],
        [
            InlineKeyboardButton(text=f'{emoji.gift} Бонуси у подарунок',
                                 callback_data=post_callback.new(action='gift_bonus')),
        ],
        [
            InlineKeyboardButton(text=f'💳 Додати/Замінити картку',
                                 callback_data=post_callback.new(action='add_replace_card')),
        ],
        [
            InlineKeyboardButton(text=f'Повернутися в меню{emoji.left_hand}',
                                 callback_data=post_callback.new(action='back_to_menu')),
        ],
    ]
)


bonus_gift_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=f'{emoji.bonus} Отримати бонуси', callback_data=post_callback.new(action='get_bonus')),
        ],
        [
            InlineKeyboardButton(text=f'{emoji.check} Перевірити нарахування бонусів',
                                 callback_data=post_callback.new(action='check_bonus')),
        ],
        [
            InlineKeyboardButton(text=f'Назад',
                                 callback_data=post_callback.new(action='back_to_bonuses')),
        ],
    ]
)