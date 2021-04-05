import os

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from Emoji import emoji
from keyboards.default import main_keyboard
from keyboards.inline.admin_panel.admin_menu import admin_keyboard
from keyboards.inline.admin_panel.stocks import cancel
from keyboards.inline.callback_datas import post_callback
from loader import dp
from states.Stocks import Stocks


@dp.message_handler(text='Скасувати видалення', state='*')
async def destroy_mailing_admin_panel(message: Message, state: FSMContext):
    await message.answer(f'Видалення успішно скасовано!', reply_markup=ReplyKeyboardRemove())
    await message.answer(f'Обирайте{emoji.arrow_down}', reply_markup=admin_keyboard)
    await state.finish()


@dp.callback_query_handler(post_callback.filter(action='delete_pharmacy'), state=None)
async def delete_stock_photo(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Введіть назву картинки (номер аптеки), яку ви хочете видалити!',
                                  reply_markup=cancel.deleting_photo_keyboard)
    await Stocks.deletePharmacyPhoto.set()


@dp.message_handler(state=Stocks.deletePharmacyPhoto, content_types='text')
async def get_new_message(message: Message, state: FSMContext):
    photo_name = f'{message.text}.jpg'

    path = os.path.join('/src/pharmacy_photos/', photo_name)
    os.remove(path)

    await message.answer(f'Фото {photo_name} успешно удалено!', reply_markup=main_keyboard)
    await state.finish()
