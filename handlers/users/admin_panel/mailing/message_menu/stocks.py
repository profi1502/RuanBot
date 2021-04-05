from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from keyboards.inline.admin_panel.mailing.message_menu import variants
from keyboards.inline.callback_datas import post_callback
from loader import dp


@dp.callback_query_handler(post_callback.filter(action='add_stocks'), state='*')
async def stock_button(call: CallbackQuery, state: FSMContext):
    await call.answer()

    async with state.proxy() as data:
        data['cash']['stocks'] = '1'

    # проверяем были ли созданы юрл кнопки
    if 'url_button' in data['cash']:
        await call.message.edit_reply_markup(await variants(data['cash'], data['cash']['url_button']))
    else:
        markup = InlineKeyboardMarkup()
        await call.message.edit_reply_markup(await variants(data['cash'], markup))


@dp.callback_query_handler(post_callback.filter(action='delete_stocks'), state='*')
async def stock_button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    async with state.proxy() as data:
        data['cash'].pop('stocks')

    if 'url_button' in data['cash']:
        await call.message.edit_reply_markup(await variants(data['cash'], data['cash']['url_button']))
    else:
        await call.message.edit_reply_markup(await variants(data['cash']))
