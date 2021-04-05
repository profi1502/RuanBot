from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.admin_panel.mailing.message_menu import variants
from keyboards.inline.callback_datas import post_callback
from loader import dp


@dp.callback_query_handler(post_callback.filter(action='add_contacts'), state='*')
async def stock_button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    async with state.proxy() as data:
        data['cash']['contacts'] = '1'

    if 'url_button' in data['cash']:
        await call.message.edit_reply_markup(await variants(data['cash'], data['cash']['url_button']))
    else:
        await call.message.edit_reply_markup(await variants(data['cash']))


@dp.callback_query_handler(post_callback.filter(action='delete_contacts'), state='*')
async def stock_button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    async with state.proxy() as data:
        data['cash'].pop('contacts')

    if 'url_button' in data['cash']:
        await call.message.edit_reply_markup(await variants(data['cash'], data['cash']['url_button']))
    else:
        await call.message.edit_reply_markup(await variants(data['cash']))
