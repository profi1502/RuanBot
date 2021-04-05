from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from keyboards.default import main_keyboard
from keyboards.inline.admin_panel.stocks.publish_button import publish_button
from loader import dp
from states.Stocks import Stocks


@dp.message_handler(text='Додати фото', state=None)
async def enter_photo(message: Message):
    await message.answer('Отправьте новое фото для вкладки "Діючі акції", '
                         'после чего нажмите кнопку "Я закончил": \n\n'
                         f'* Если вы не отправите фото и нажмете кнопку "Запостити", '
                         f'то вы просто вернетесь в админ панель)',
                         reply_markup=publish_button)
    await Stocks.editStockPhoto.set()


@dp.message_handler(text='Скасувати публікацію', state='*')
async def destroy_publication(message: Message, state: FSMContext):
    await message.answer('Редактирование фото во вкладке "Діючі акції" успешно завершено!', reply_markup=main_keyboard)
    await state.finish()


@dp.message_handler(state=Stocks.editStockPhoto, content_types='photo')
async def get_photo(message: Message):
    await message.photo[-1].download('/src/stocks/')


@dp.message_handler(text='Запостити', state='*')
async def post_photo(message: Message, state: FSMContext):
    await message.answer('Редактирование фото во вкладке "Діючі акції" успешно завершено!', reply_markup=main_keyboard)
    await state.finish()
