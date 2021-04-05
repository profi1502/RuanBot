# Функция, которая обрабатывает ВСЕ нажатия на кнопки в этой менюшке
from aiogram.types import CallbackQuery

from handlers.users.choose_city.by_buttons.handlers import list_cities, list_addresses, show_info
from handlers.users.choose_city.by_coordinates.handlers import list_near_addresses, show_all_addresses, back_to_menu
from keyboards.inline.callback_datas import menu_cd
from loader import dp


@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    """
    :param call: Тип объекта CallbackQuery, который прилетает в хендлер
    :param callback_data: Словарь с данными, которые хранятся в нажатой кнопке
    """

    # Получаем текущий уровень меню, который запросил пользователь
    current_level = callback_data.get("level")

    # Получаем категорию, которую выбрал пользователь (Передается всегда)
    city = callback_data.get("city")

    # Получаем подкатегорию, которую выбрал пользователь (Передается НЕ ВСЕГДА - может быть 0)
    address = callback_data.get("address")

    # Прописываем "уровни" в которые будут отправляться новые кнопки пользователю
    levels = {
        #  by buttons
        "0": list_cities,
        "1": list_addresses,
        "2": show_info,

        #  by coordinates
        "3": list_near_addresses,
        "4": show_all_addresses,
        "5": back_to_menu
    }

    # Забираем нужную функцию для выбранного уровня
    current_level_function = levels[current_level]

    # Выполняем нужную функцию и передаем туда параметры, полученные из кнопки
    # это параметры которые мы должны были указать в levels, о так как там мы не поставили скобки, то тут
    await current_level_function(
        call,
        city=city,
        address=address
    )
