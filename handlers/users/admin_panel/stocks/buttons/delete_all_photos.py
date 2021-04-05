import os

from aiogram.types import Message

from keyboards.inline.admin_panel.stocks.main_keyboard import stock_keyboard
from loader import dp


@dp.message_handler(text='Видалити всі фото', state=None)
async def enter_new_message(message: Message):
    folder = '/src/stocks/photos'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)

        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

    await message.answer(f'Все фото во вкладке "Діючі акції" успешно удалены!', reply_markup=stock_keyboard)
