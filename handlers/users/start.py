from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default import main_keyboard
from loader import dp
from utils.db_api.admin_db_methods import add_new_user
from utils.misc import rate_limit


@rate_limit(5, 'start')
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):

    if message.from_user.last_name is None:
        await message.answer(f'Привіт {message.from_user.first_name}, Ви зайшли на офіційну сторінку бота мережі аптек '
                             f'РУАН', reply_markup=main_keyboard)
    else:
        await message.answer(f'Привіт {message.from_user.full_name}, Ви зайшли на офіційну сторінку бота мережі аптек '
                             f'РУАН', reply_markup=main_keyboard)
    await add_new_user()
