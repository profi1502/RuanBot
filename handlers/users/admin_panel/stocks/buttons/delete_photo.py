import os

from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, Message

from keyboards.default import main_keyboard
from keyboards.inline.admin_panel.stocks import cancel
from loader import bot, dp
from states.Stocks import Stocks


@dp.message_handler(text='Видалити фото', state=None)
async def delete_stock_photo(message: Message):
    photos = os.listdir('/src/stocks/photos')
    for photo in photos:
        await bot.send_photo(
            chat_id=message.from_user.id, photo=InputFile(path_or_bytesio=f'/src/stocks/photos/{photo}'), caption=photo
        )
    await message.answer('Скопіюйте та вставте ім\'я фотографії, яку ви хочете видалити!',
                         reply_markup=cancel.deleting_photo_keyboard)
    await Stocks.deleteStockPhoto.set()


@dp.message_handler(state=Stocks.deleteStockPhoto, content_types='text')
async def get_new_message(message: Message, state: FSMContext):
    photo_name = message.text

    path = os.path.join('/src/stocks/photos', photo_name)
    os.remove(path)

    await message.answer(f'Фото {photo_name} у вкладці "Діючі Акції" успішно видалено!', reply_markup=main_keyboard)
    await state.finish()
