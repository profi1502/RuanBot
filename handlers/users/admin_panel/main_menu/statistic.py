from aiogram.types import CallbackQuery

from Emoji import emoji
from keyboards.inline.admin_panel.admin_menu import admin_keyboard
from keyboards.inline.admin_panel.statistic.keyboard import stat_keyboard
from keyboards.inline.admin_panel.statistic.period import keyboard
from keyboards.inline.callback_datas import post_callback
from loader import dp
from utils.db_api.admin_db_methods import count_users


@dp.callback_query_handler(text_contains='statistic')
async def count_users_admin_panel(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text='Статистика бота RUAN', reply_markup=stat_keyboard)


@dp.callback_query_handler(post_callback.filter(action='count_users'))
async def count_users_admin_panel(call: CallbackQuery):
    await call.answer(f'Кількість підписників: {await count_users()}', show_alert=True)


@dp.callback_query_handler(post_callback.filter(action='period'))
async def count_users_admin_panel(call: CallbackQuery):
    await call.message.edit_text(f'Обирайте{emoji.arrow_down}', reply_markup=keyboard)


@dp.callback_query_handler(post_callback.filter(action='back_to_admin'))
async def count_users_admin_panel(call: CallbackQuery):
    await call.message.edit_text('Ласкаво просимо в адмін панель!', reply_markup=admin_keyboard)
