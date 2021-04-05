from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message, ReplyKeyboardMarkup, \
    KeyboardButton
from aiogram.utils.exceptions import BadRequest

from keyboards.inline.admin_panel.mailing.message_menu import variants
from keyboards.inline.admin_panel.mailing.main_keyboard import mailing_keyboard
from keyboards.inline.callback_datas import post_callback
from loader import dp, bot
from states.NewPost import NewPost


@dp.callback_query_handler(post_callback.filter(action='add_url'), state='*')
async def enter_message(call: CallbackQuery):
    await call.message.delete()
    keyboard = ReplyKeyboardMarkup()
    cancel = KeyboardButton('Отмена', callback_data='cancel')
    keyboard.add(cancel)
    keyboard.resize_keyboard = True

    await bot.send_message(chat_id=call.from_user.id, text='Отправьте мне список URL-кнопок в одном сообщении.\n'
                                                           'Пожалуйста, следуйте этому формату:\n\n'
                                                           '<code>Кнопка 1 - http://example1.com</code>\n'
                                                           '<code>Кнопка 2 - http://example2.com</code>\n\n'
                                                           'Используйте разделитель |, '
                                                           'чтобы добавить до трех кнопок в один ряд. Пример:\n\n'
                                                           '<code>Кнопка 1 - http://example1.com | Кнопка 2 - http://example2.com</code>\n'
                                                           '<code>Кнопка 3 - http://example3.com | Кнопка 4 - http://example4.com</code>\n\n\n'
                                                           'Нажмите кнопку «Отмена», чтобы вернуться к добавлению сообщений.',
                           reply_markup=keyboard)
    await NewPost.getUrlButton.set()


@dp.message_handler(state=NewPost.getUrlButton, content_types='text')
async def get_message(message: Message, state: FSMContext):
    button_list = []

    await state.update_data(button_list=button_list)

    async with state.proxy() as data:
        pass

    try:
        if '|' in message.text and '\n' in message.text:
            button_text = message.text.split('\n')
            for butt in button_text:
                button_text_edit = butt.split('|')
                data['button_list'].append(button_text_edit)

            url_markup = InlineKeyboardMarkup(row_width=len(data['button_list']))
            for button in data['button_list']:
                for i in button:
                    button_name = i.split('-')[0]
                    button_url = i.split('-')[1].replace(' ', '')

                    button1 = InlineKeyboardButton(text=button_name, url=button_url)
                    url_markup.insert(button1)

            async with state.proxy() as data:
                data['cash']['url_button'] = url_markup

            await data['cash']['message'].send_copy(chat_id=message.from_user.id,
                                                    reply_markup=await variants(data['cash'], url_markup))
            await message.answer(text='URL-кнопки сохранены. Продолжайте отправлять сообщения.',
                                 reply_markup=mailing_keyboard)

        elif '\n' in message.text:
            # code
            button_text = message.text.split('\n')

            for butt in button_text:
                button_name = butt.split('-')[0]
                button_url = butt.split('-')[1].replace(' ', '')

                button = InlineKeyboardButton(text=button_name, url=button_url)
                data['button_list'].append(button)

            url_markup = InlineKeyboardMarkup()

            for button in data['button_list']:
                url_markup.add(button)
            # code

            async with state.proxy() as data:
                data['cash']['url_button'] = url_markup

            await data['cash']['message'].send_copy(chat_id=message.from_user.id,
                                                    reply_markup=await variants(data['cash'], url_markup))
            await message.answer(text='URL-кнопки сохранены. Продолжайте отправлять сообщения.',
                                 reply_markup=mailing_keyboard)

        elif '|' in message.text:
            button_text = message.text.split('|')
            for butt in button_text:
                button_name = butt.split('-')[0]
                button_url = butt.split('-')[1].replace(' ', '')

                button = InlineKeyboardButton(text=button_name, url=button_url)
                data['button_list'].append(button)

            url_markup = InlineKeyboardMarkup()

            for button in data['button_list']:
                url_markup.insert(button)

            async with state.proxy() as data:
                data['cash']['url_button'] = url_markup

            await data['cash']['message'].send_copy(chat_id=message.from_user.id,
                                                    reply_markup=await variants(data['cash'], url_markup))
            await message.answer(text='URL-кнопки сохранены. Продолжайте отправлять сообщения.',
                                 reply_markup=mailing_keyboard)
        else:
            button_name = message.text.split('-')[0]
            button_url = message.text.split('-')[1].replace(' ', '')

            button = InlineKeyboardButton(text=button_name, url=button_url)
            data['button_list'].append(button)

            url_markup = InlineKeyboardMarkup()

            for button in data['button_list']:
                url_markup.add(button)

            async with state.proxy() as data:
                data['cash']['url_button'] = url_markup

            await data['cash']['message'].send_copy(chat_id=message.from_user.id,
                                                    reply_markup=await variants(data['cash'], url_markup))
            await message.answer(text='URL-кнопки сохранены. Продолжайте отправлять сообщения.',
                                 reply_markup=mailing_keyboard)
    except IndexError:
        await message.answer(
            'Вы прислали что-то не внятное. Пришлите клавиатуру по примеру выше.')
        await NewPost.getUrlButton.set()

    except BadRequest:
        await message.answer(
            'Некорректная клавиатура: <code>wrong HTTP URL</code>\n\n'
            'Исправьте ошибку и пришлите еще раз.')
        await NewPost.getUrlButton.set()

    data['button_list'].clear()


@dp.callback_query_handler(post_callback.filter(action='delete_url'), state='*')
async def stock_button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    async with state.proxy() as data:
        data['cash'].pop('url_button')

    markup = InlineKeyboardMarkup()
    await call.message.edit_reply_markup(await variants(data['cash'], markup))
