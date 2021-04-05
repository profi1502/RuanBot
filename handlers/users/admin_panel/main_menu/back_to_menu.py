from aiogram.types import CallbackQuery

from Emoji import emoji
from keyboards.default import main_keyboard
from loader import dp, bot


@dp.callback_query_handler(text_contains='back_to_menu')
async def back_to_menu(call: CallbackQuery):
    await call.message.delete()

    await bot.send_message(chat_id=call.from_user.id, text=f'Обирайте{emoji.arrow_down}', reply_markup=main_keyboard)