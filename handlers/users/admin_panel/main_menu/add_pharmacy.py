from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ContentType

from Emoji import emoji
from keyboards.inline.admin_panel.admin_menu import admin_keyboard
from keyboards.inline.admin_panel.stocks.publish_button import publish_button_pharmacy
from keyboards.inline.callback_datas import post_callback
from loader import dp
from states.Stocks import Stocks


@dp.callback_query_handler(post_callback.filter(action='add_pharmacy'), state=None)
async def enter_photo(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Надішліть нове фото аптеки <u>ЯК Фото</u>, '
                                  'Після чого натисніть кнопку "Я закінчив":\n\n'
                                  f'* Якщо ви не відправите фото і натиснете кнопку "Я закінчив",'
                                  f'то ви просто повернетеся в адмін панель)',
                                  reply_markup=publish_button_pharmacy)
    await Stocks.editPharmacyPhoto.set()


@dp.message_handler(state=Stocks.editPharmacyPhoto, content_types=ContentType.DOCUMENT)
async def get_photo(message: Message):
    document = message.document

    await document.download(f'/src/pharmacy_photos/{document.file_name}')


@dp.message_handler(text='Запостити аптеку', state='*')
async def destroy_mailing_admin_panel(message: Message, state: FSMContext):
    await message.answer('Додавання фото успішно завершено!', reply_markup=ReplyKeyboardRemove())
    await message.answer(f'Обирайте{emoji.arrow_down}', reply_markup=admin_keyboard)

    await state.finish()
