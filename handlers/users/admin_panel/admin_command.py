from aiogram.dispatcher.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from data.config import admins
from keyboards.inline.admin_panel.admin_menu import admin_keyboard
from loader import dp


@dp.message_handler(Command('admin'), user_id=admins)
async def open_admin_panel(message: Message):
    await message.answer('Адмін дані:\n'
                         f'Ім\'я: <u>{message.from_user.first_name}</u>\n'
                         f'Id: <u>{message.from_user.id}</u>', reply_markup=ReplyKeyboardRemove())
    await message.answer('Ласкаво просимо в адмін панель!', reply_markup=admin_keyboard)
