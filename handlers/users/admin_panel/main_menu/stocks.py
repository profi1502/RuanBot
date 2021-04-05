from aiogram.types import CallbackQuery

from Emoji import emoji
from keyboards.inline.admin_panel.stocks.main_keyboard import stock_keyboard
from keyboards.inline.callback_datas import post_callback
from loader import dp, bot


@dp.callback_query_handler(post_callback.filter(action='stocks'))
async def stocks_options(call: CallbackQuery):
    await call.answer()
    await bot.send_message(chat_id=call.from_user.id, text=f'Обирайте{emoji.arrow_down}', reply_markup=stock_keyboard)
    await call.message.delete()
