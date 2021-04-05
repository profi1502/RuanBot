from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from keyboards.inline.callback_datas import post_callback

add_url_button = InlineKeyboardButton(text='Добавить URL-кнопки', callback_data=post_callback.new(action='add_url'))

add_contact_button = InlineKeyboardButton(text='Добавить кнопку "Зв\'язатися з нами"',
                                          callback_data=post_callback.new(action='add_contacts'))
add_stock_button = InlineKeyboardButton(text='Добавить кнопку "Діючі акції"',
                                        callback_data=post_callback.new(action='add_stocks'))
delete_contact_button = InlineKeyboardButton(text='Удалить кнопку "Зв\'язатися з нами"',
                                             callback_data=post_callback.new(action='delete_contacts'))
delete_stock_button = InlineKeyboardButton(text='Удалить кнопку "Діючі акції"',
                                           callback_data=post_callback.new(action='delete_stocks'))
delete_url_button = InlineKeyboardButton(text='Удалить URL-кнопки', callback_data=post_callback.new(action='delete_url'))

mailing_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Очистить'),
            KeyboardButton('Предпросмотр'),
        ],
        [
            KeyboardButton('Отменить'),
            KeyboardButton('Опубликовать'),
        ],
    ],
    resize_keyboard=True
)

mailing_settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            add_url_button
        ],
        [
            add_stock_button
        ],
        [
            add_contact_button
        ]
    ]
)
