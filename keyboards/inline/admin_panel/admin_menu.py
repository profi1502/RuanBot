from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Emoji import emoji
from keyboards.inline.callback_datas import post_callback

admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Зробити розсилку', callback_data=post_callback.new(action='make_mailing')),
        ],
        [
            InlineKeyboardButton(text='Акції', callback_data=post_callback.new(action='stocks')),
            InlineKeyboardButton(text='Статистика', callback_data=post_callback.new(action='statistic')),
        ],
        [
            InlineKeyboardButton(text='Додати аптеку', callback_data=post_callback.new(action='add_pharmacy')),
        ],
        [
            InlineKeyboardButton(text='Видалити Аптеку', callback_data=post_callback.new(action='delete_pharmacy')),
        ],
        [
            InlineKeyboardButton(text=f'Повернутися в меню{emoji.left_hand}',
                                 callback_data=post_callback.new(action='back_to_menu')),
        ],
    ]
)
