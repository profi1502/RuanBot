from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from keyboards.default import main_keyboard
from keyboards.inline.admin_panel.stocks import cancel
from loader import dp
from states.Stocks import Stocks
from utils.db_api import db_commands
from utils.db_api.models import StockText


@dp.message_handler(text_contains='Редагувати опис', state=None)
async def enter_new_message(message: Message):
    try:
        caption = await db_commands.get_StockText()
    except IndexError:
        caption = 'None'

    await message.answer('Надішліть новий текст для вкладки "Діючі Акції":\n'
                         '\n'
                         f'Текущій текст: {caption}', reply_markup=cancel.editing_text_keyboard)
    await Stocks.editStockText.set()


@dp.message_handler(state=Stocks.editStockText, content_types='text')
async def get_new_message(message: Message, state: FSMContext):

    await db_commands.truncate_table(StockText)
    await db_commands.add_StockText(message.html_text)
    await message.answer('Редагування тексту у вкладці "Діючі Акції" успішно завершено!',
                         reply_markup=main_keyboard)
    await state.finish()
