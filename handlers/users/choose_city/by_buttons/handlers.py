import time
from typing import Union

from aiogram.types import Message, CallbackQuery

from Emoji import emoji
from keyboards.default import main_keyboard
from .keyboards import city_keyboard
from ..by_buttons.keyboards import info_keyboard, address_keyboard
from loader import dp, bot
from utils.db_api.db_commands import get_info, get_hash
from utils.misc import rate_limit


@rate_limit(5, 'Оберіть місто')
@dp.message_handler(text=f'Оберіть місто{emoji.keyboard}')
async def show_cities(message: Message):
    await list_cities(message)


async def list_cities(message: Union[CallbackQuery, Message], **kwargs):
    # Клавиатуру формируем с помощью следующей функции (где делается запрос в базу данных)
    markup = await city_keyboard()

    # Проверяем, что за тип апдейта. Если Message - отправляем новое сообщение
    if isinstance(message, Message):
        await message.answer(f'Оберіть місто{emoji.arrow_down}', reply_markup=markup)

    # Если CallbackQuery - изменяем это сообщение
    elif isinstance(message, CallbackQuery):
        call = message
        await call.answer()
        await call.message.edit_reply_markup(markup)


async def list_addresses(callback: CallbackQuery, city, **kwargs):
    await callback.answer()
    city_name = city.split('  ', 1)[1]

    markup = await address_keyboard(city_name)

    # Изменяем сообщение, и отправляем новые кнопки с подкатегориями
    await callback.message.edit_text(
        text=f"Оберіть адресу{emoji.arrow_down}", reply_markup=markup)


# Функция, которая отдает уже кнопку Купить товар по выбранному товару
async def show_info(callback: CallbackQuery, city, address):
    address_id = int(address)

    markup = await info_keyboard(address_id)

    # Берем запись о нашем товаре из базы данных
    info = await get_info(address_id)
    photo_name = await get_hash(address_id)
    try:
        await bot.send_photo(chat_id=callback.from_user.id,
                             photo=open(f'/src/pharmacy_photos/{photo_name}.jpg', 'rb'),
                             caption=info, reply_markup=markup)
    except FileNotFoundError:
        await bot.send_message(chat_id=callback.from_user.id,
                               text="Вибачте, але дана аптека тимчасово не працює (")

    await callback.message.delete()

    await bot.send_message(chat_id=callback.from_user.id,
                           text=f'Обирайте{emoji.arrow_down}', reply_markup=main_keyboard)
