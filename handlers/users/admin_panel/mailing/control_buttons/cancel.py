from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.inline.admin_panel.admin_menu import admin_keyboard
from keyboards.inline.admin_panel.mailing.message_menu import variants
from keyboards.inline.admin_panel.mailing.main_keyboard import mailing_keyboard
from loader import dp
from states.NewPost import NewPost


# здесь находятся все кнопки отмены для вкладки "Зробити розсилку"

@dp.message_handler(text='Отмена', state='*')
async def destroy_mailing_admin_panel(message: Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    await message.answer(text='Вы отменили добавление URL-кнопок', reply_markup=mailing_keyboard)
    await data['cash']['message'].send_copy(chat_id=message.from_user.id,
                                            reply_markup=await variants(data['cash']))


@dp.message_handler(text='Отменить', state='*')
async def cancel_mail(message: Message, state: FSMContext):
    await message.answer('Создание рассылки отменено.', reply_markup=ReplyKeyboardRemove())
    await message.answer('Здесь вы можете создавать посты, '
                         'просматривать статистику и выполнять другие задачи.', reply_markup=admin_keyboard)

    await state.finish()


@dp.message_handler(text='Очистить', state='*')
async def delete_message(message: Message, state: FSMContext):
    await message.answer(f'Сообщение удалено.')
    await state.finish()
    await NewPost.EnterMessage.set()
