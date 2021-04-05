import time
from typing import Union

from aiogram import types
from aiogram.types import Message, CallbackQuery

from Emoji import emoji
from keyboards.default import main_keyboard
from keyboards.inline import show_other
from keyboards.inline.callback_datas import post_callback
from loader import dp, bot
from utils.db_api.db_commands import get_info, get_hash
from utils.misc import rate_limit
from utils.misc.calc_distance import choose_shortest
from utils.misc.cityInfo import get_city
from .keyboards import address_near_keyboard, info_near_keyboard, all_address_keyboard
from ..by_buttons.handlers import list_cities


@rate_limit(5)
@dp.callback_query_handler(post_callback.filter(action='show_other_city'))
async def show_cities(message: Message):
    await list_cities(message)


@rate_limit(5, 'За координатами')
@dp.message_handler(content_types=types.ContentType.LOCATION)
async def show_near_cities(message: Message):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    closest_shops = await choose_shortest(location)

    await list_near_addresses(message, city=get_city(latitude=latitude, longitude=longitude),
                              closest_shops=closest_shops)


async def list_near_addresses(message: Union[CallbackQuery, Message], city, closest_shops, **kwargs):
    markup = await address_near_keyboard(closest_shops, city)

    if isinstance(message, Message):
        if len(closest_shops) != 0:
            await message.answer(f"Обирайте{emoji.arrow_down}", reply_markup=markup)

        elif len(closest_shops) == 0:
            await message.answer('У вашому місті немає аптек руан(', reply_markup=show_other.keyboard)

        else:
            await message.answer('На жаль у вашому районі немає аптеки поблизу, оберіть аптеки вручну!',
                                 reply_markup=show_other.choose_manually)

    # Если CallbackQuery - изменяем это сообщение
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


# Функция, которая отдает уже кнопку Купить товар по выбранному товару
async def show_near_info(callback: CallbackQuery, city, address):
    address_id = int(address)

    markup = await info_near_keyboard(address_id)

    # Берем запись о нашем товаре из базы данных
    info = await get_info(address_id)
    photo_name = await get_hash(address_id)
    try:
        await bot.send_photo(chat_id=callback.from_user.id,
                             photo=open(f'/src/pharmacy_photos/{photo_name}.jpg', 'rb'),
                             caption=info, reply_markup=markup)
    except FileNotFoundError:
        await bot.send_message(chat_id=callback.from_user.id, text="Вибачте, але дана аптека зараз не працює (")

    await callback.message.delete()

    time.sleep(0.9)
    await bot.send_message(chat_id=callback.from_user.id,
                           text=f'Обирайте{emoji.arrow_down}', reply_markup=main_keyboard)


async def show_all_addresses(callback: CallbackQuery, city, address):
    markup = await all_address_keyboard(city)

    # Изменяем сообщение, и отправляем новые кнопки с подкатегориями
    await callback.message.edit_reply_markup(markup)


async def back_to_menu(callback: CallbackQuery, city, address):
    await bot.send_message(chat_id=callback.from_user.id,
                           text=f'Обирайте{emoji.arrow_down}', reply_markup=main_keyboard)

    await callback.message.delete()
