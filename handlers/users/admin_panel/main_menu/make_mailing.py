from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline.admin_panel.mailing.main_keyboard import mailing_keyboard
from keyboards.inline.admin_panel.mailing.message_menu import variants
from loader import bot, dp
from states.NewPost import NewPost


#  запрашиваем и получаем сообение по нажатию на кнопку "Зробити розсилку"

@dp.callback_query_handler(text_contains='make_mailing')
async def enter_message(call: CallbackQuery):
    await call.message.delete()
    await bot.send_message(chat_id=call.from_user.id, text='Отправьте боту то, что хотите опубликовать. '
                                                           'Это может быть всё, что угодно – текст, фото, видео, даже стикеры.',
                           reply_markup=mailing_keyboard)
    await NewPost.EnterMessage.set()


@dp.message_handler(state=NewPost.EnterMessage, content_types='any')
async def get_message(message: Message, state: FSMContext):
    cash = {}
    await state.update_data(cash=cash)

    async with state.proxy() as data:
        data['cash']['message'] = message

    await message.send_copy(chat_id=message.from_user.id, reply_markup=await variants(data['cash']))
