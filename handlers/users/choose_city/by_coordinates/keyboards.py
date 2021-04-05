from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Emoji import emoji
from handlers.users.choose_city.by_buttons.keyboards import sorting_by_address
from handlers.users.choose_city.sorting_by_city import sorted_addresses
from keyboards.inline.callback_datas import make_callback_data
from utils.db_api.db_commands import get_gmaps_url


async def address_near_keyboard(closest_shops, city):
    CURRENT_LEVEL = 3

    markup: InlineKeyboardMarkup = InlineKeyboardMarkup()

    buttons = []
    listMax = []
    listMin = []

    # for address_ in closest_shops:
    #     if len(address_) <= 16:
    #         listMin.append(address_)  # 1 buttons
    #     else:
    #         listMax.append(address_)  # 2 buttons

    result = []

    result.extend(
        list(zip(*[iter(closest_shops)] * 1)) + ([tuple(closest_shops[-(len(closest_shops) % 1):])] if len(closest_shops) % 1 > 0 else []))
    for row in result:
        row_buttons = []
        for element in row:
            row_buttons.append(InlineKeyboardButton(text=f'{element[1]} ({element[2]} м.)',
                                                    callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                                                     city=city, address=element[0])))
        buttons.append(row_buttons)

    markup.inline_keyboard = buttons

    markup.row(
        InlineKeyboardButton(
            text='Показати всі',
            callback_data=make_callback_data(level=CURRENT_LEVEL + 1, city=city)
        ))
    return markup


async def all_address_keyboard(city):
    # Текущий уровень - 1
    CURRENT_LEVEL = 1

    markup: InlineKeyboardMarkup = InlineKeyboardMarkup()

    buttons = []
    main_list = await sorted_addresses(city)
    listMax = []
    listMin = []
    for address_ in main_list:
        if len(address_[0]) >= 22.5:
            listMax.append(address_)  # 1 buttons
        else:
            listMin.append(address_)  # 2 buttons

    result = []

    result.extend(
        list(zip(*[iter(listMin)] * 2)) + ([tuple(listMin[-(len(listMin) % 2):])] if len(listMin) % 2 > 0 else []))
    result.extend(
        list(zip(*[iter(listMax)] * 1)) + ([tuple(listMax[-(len(listMax) % 1):])] if len(listMax) % 1 > 0 else []))
    for row in result:
        row_buttons = []
        for element in row:
            row_buttons.append(InlineKeyboardButton(text=element[0],
                                                    callback_data=make_callback_data(level=CURRENT_LEVEL + 1,
                                                                                     city=city, address=element[1])))
        buttons.append(row_buttons)

    newList = sorted(buttons, key=sorting_by_address)
    markup.inline_keyboard = newList

    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 0.
    markup.row(
        InlineKeyboardButton(
            text=f'Повернутися в меню{emoji.left_hand}',
            callback_data=make_callback_data(level=CURRENT_LEVEL + 4))
    )
    return markup


# Создаем функцию, которая отдает клавиатуру с кнопками "купить" и "назад" для выбранного товара
async def info_near_keyboard(address):
    markup = InlineKeyboardMarkup()

    markup.row(
        InlineKeyboardButton(
            text='Відкрити Google Maps', url=(await get_gmaps_url(address)))
    )
    return markup
