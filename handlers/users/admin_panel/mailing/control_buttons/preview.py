from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from Emoji import emoji
from keyboards.inline.admin_panel.mailing.main_keyboard import mailing_keyboard
from keyboards.inline.callback_datas import post_callback
from loader import dp


@dp.message_handler(text='Предпросмотр', state='*')
async def preview(message: Message, state: FSMContext):
    async with state.proxy() as data:
        pass

    try:
        if 'url_button' in data['cash']:
            await data['cash']['message'].send_copy(chat_id=message.from_user.id,
                                                    reply_markup=data['cash'].get('url_button'))

        elif 'stocks' in data['cash']:
            markup = InlineKeyboardMarkup()
            stocks = InlineKeyboardButton(text=f'{emoji.money_emoji} Діючі акції',
                                          callback_data=post_callback.new(action='stock_button'))
            markup.add(stocks)
            await data['cash']['message'].send_copy(chat_id=message.from_user.id, reply_markup=markup)

        elif 'contacts' in data['cash']:
            markup = InlineKeyboardMarkup()
            contacts = InlineKeyboardButton(text=f'{emoji.phone} Зв\'язатися з нами',
                                            callback_data=post_callback.new(action='contact_button'))
            markup.add(contacts)

            await data['cash']['message'].send_copy(chat_id=message.from_user.id, reply_markup=markup)

        else:
            await data['cash']['message'].send_copy(chat_id=message.from_user.id,
                                                    reply_markup=mailing_keyboard)

    except KeyError:
        await message.answer('Нет сообщений для предпросмотра.')
