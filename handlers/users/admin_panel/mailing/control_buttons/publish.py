import os

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, InputMediaPhoto

from Emoji import emoji
from data.config import admins
from keyboards.default import main_keyboard
from keyboards.inline.callback_datas import post_callback
from loader import dp
from utils.db_api import db_commands
from utils.db_api.db_commands import delete_Blocked_User
from utils.db_api.models import User
from utils.misc import rate_limit


@dp.message_handler(text='Опубликовать', state='*')
async def send_message(message: Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    try:
        users = await User.query.gino.all()
        for user in users:
            if 'url_button' in data['cash']:
                try:
                    await message.bot.send_message(chat_id=user.chat_id, text=f'Обирайте{emoji.arrow_down}',
                                                   reply_markup=main_keyboard)
                    await data['cash']['message'].send_copy(chat_id=user.chat_id, reply_markup=data['cash']['url_button'])
                except Exception:
                    print('blocked user')
                    await delete_Blocked_User(user.chat_id)

            elif 'stocks' in data['cash']:
                markup = InlineKeyboardMarkup()
                stocks = InlineKeyboardButton(text=f'{emoji.money_emoji} Діючі акції',
                                              callback_data=post_callback.new(action='stock_button'))
                markup.add(stocks)
                try:
                    await message.bot.send_message(chat_id=user.chat_id, text=f'Обирайте{emoji.arrow_down}',
                                                   reply_markup=main_keyboard)

                    await data['cash']['message'].send_copy(chat_id=user.chat_id, reply_markup=markup)
                except Exception:
                    print('blocked user')
                    await delete_Blocked_User(user.chat_id)

            elif 'contacts' in data['cash']:

                markup = InlineKeyboardMarkup()
                contacts = InlineKeyboardButton(text=f'{emoji.phone} Зв\'язатися з нами',
                                                callback_data=post_callback.new(action='contact_button'))
                markup.add(contacts)
                try:
                    await message.bot.send_message(chat_id=user.chat_id, text=f'Обирайте{emoji.arrow_down}',
                                                   reply_markup=main_keyboard)

                    await data['cash']['message'].send_copy(chat_id=user.chat_id, reply_markup=markup)
                except Exception:
                    print('blocked user')
                    await delete_Blocked_User(user.chat_id)

            else:
                try:
                    await data['cash']['message'].send_copy(chat_id=user.chat_id, reply_markup=main_keyboard)
                except Exception:
                    print('blocked user')
                    await delete_Blocked_User(user.chat_id)

        await message.answer(f'Сообщение успешно опубликовано!', reply_markup=main_keyboard)
        await state.finish()
    except KeyError:
        await message.answer('Нет сообщений для рассылки.')


@rate_limit(5, 'stocks')
@dp.callback_query_handler(post_callback.filter(action='stock_button'), state='*')
async def show_near_pharmacy(call: CallbackQuery):
    await call.answer(cache_time=60)

    if call.from_user.id in admins:
        await call.answer()
        return

    path = '/src/stocks/photos'
    files = [f for f in os.listdir(path)
             if os.path.isfile(os.path.join(path, f))]

    try:
        caption = await db_commands.get_StockText()
    except IndexError:
        caption = 'None'

    if files:

        media = [InputMediaPhoto(open(f'/src/stocks/photos/{files[0]}', 'rb'), None, caption)]
        files.__delitem__(0)

        for photo in files:
            media.append(InputMediaPhoto(open(f'/src/stocks/photos/{photo}', 'rb')))

        await call.message.answer_media_group(media)
    else:
        await call.message.answer('На даний момент акцій не виявлено :(')


@rate_limit(5, 'Зв\'язатися з нами')
@dp.callback_query_handler(post_callback.filter(action='contact_button'), state='*')
async def show_contacts(call: CallbackQuery):
    await call.answer(cache_time=60)

    if call.from_user.id in admins:
        await call.answer()
        return

    await call.bot.send_message(chat_id=call.from_user.id,
                                text=f'{emoji.pager} 0 800 75 80 18\n'
                                     f'{emoji.envelope_with_arrow} info@apteka-ruan.com.ua',
                                reply_markup=main_keyboard)
