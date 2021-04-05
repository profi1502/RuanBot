from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from Emoji import emoji
from keyboards.inline.admin_panel.admin_menu import admin_keyboard
from loader import dp


@dp.message_handler(text='Скасувати редагування', state='*')
async def destroy_mailing_admin_panel(message: Message, state: FSMContext):
    await message.answer(f'Редагування успішно скасовано!', reply_markup=ReplyKeyboardRemove())
    await message.answer(f'Обирайте{emoji.arrow_down}', reply_markup=admin_keyboard)
    await state.finish()


@dp.message_handler(text='Скасувати видалення', state='*')
async def destroy_mailing_admin_panel(message: Message, state: FSMContext):
    await message.answer(f'Видалення успішно скасовано!', reply_markup=ReplyKeyboardRemove())
    await message.answer(f'Обирайте{emoji.arrow_down}', reply_markup=admin_keyboard)
    await state.finish()


@dp.message_handler(text='Назад')
async def get_message(message: Message):
    await message.answer(text='Успешный выход.', reply_markup=ReplyKeyboardRemove())

    await message.answer(text='Ласкаво просимо в адмін панель!', reply_markup=admin_keyboard)
