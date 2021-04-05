from aiogram import types

from keyboards.default import main_keyboard
from loader import dp
from utils.misc import rate_limit


@rate_limit(5, 'echo')
@dp.message_handler()
async def bot_echo(message: types.Message):
    await message.answer(text=message.text, reply_markup=main_keyboard)
