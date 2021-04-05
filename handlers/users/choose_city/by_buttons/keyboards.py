from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from natsort import natsorted

from Emoji import emoji
from keyboards.inline.callback_datas import make_callback_data
from utils.db_api.db_commands import get_addresses, get_gmaps_url

#  метод который возвращает рядок с кнопками
from handlers.users.choose_city.sorting_by_city import sorted_cities, sorted_addresses


def make_row(city_name, callback_data, markup: InlineKeyboardMarkup):
    return markup.row(InlineKeyboardButton(text=city_name, callback_data=callback_data))


def sorting_by_address(input):

    if 'селище' in input[0].text or 'вул.' in input[0].text or 'бул.' in input[0].text or 'ж/м' in input[0].text \
            or 'пр.' in input[0].text or 'пр-т' in input[0].text or 'пл.' in input[0].text \
            or 'провулок' in input[0].text:

        address_name = input[0].text.replace('вул. ', '').replace('бул. ', '') \
            .replace('ж/м ', '').replace('пр. ', '') \
            .replace('пр-т ', '').replace('пл. ', ''). \
            replace('провулок ', '').replace('селище ', '').strip()

        if address_name[0].isdigit():
            return 'я'
        elif address_name[0] == 'І':
            return 'И'
        elif address_name[0] == 'I':
            return 'И'

        else:
            return address_name
    else:
        return input[0].text


def sorting_city(input):
    if input[0].text[0] == 'І':
        return 'И'
    elif input[0].text[0] == 'і':
        return 'и'
    else:
        return input[0].text


async def city_keyboard():
    # Указываем, что текущий уровень меню - 0
    CURRENT_LEVEL = 0

    # Создаем Клавиатуру
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup()

    buttons = []
    main_list = await sorted_cities()
    listMax = []
    listMin = []
    for city_ in main_list:
        if len(city_) >= 11:
            listMax.append(city_)  # 2 buttons
        else:
            listMin.append(city_)  # 3 buttons

    result = []

    result.extend(
        list(zip(*[iter(listMin)] * 3)) + ([tuple(listMin[-(len(listMin) % 3):])] if len(listMin) % 3 > 0 else []))
    result.extend(
        list(zip(*[iter(listMax)] * 2)) + ([tuple(listMax[-(len(listMax) % 2):])] if len(listMax) % 2 > 0 else []))

    for row in result:
        row_buttons = []
        for element in row:
            row_buttons.append(InlineKeyboardButton(text=element,
                                                    callback_data=make_callback_data(level=CURRENT_LEVEL + 1,
                                                                                     city=f'city  {element}')))
        buttons.append(row_buttons)

    newList = sorted(buttons, key=sorting_city)
    markup.inline_keyboard = newList

    markup.row(
        InlineKeyboardButton(
            text=f'Повернутися в меню{emoji.left_hand}',
            callback_data=make_callback_data(level=CURRENT_LEVEL + 5))
    )

    return markup


# Создаем функцию, которая отдает клавиатуру с доступными подкатегориями, исходя из выбранной категории
async def address_keyboard(city):
    # Текущий уровень - 1
    CURRENT_LEVEL = 1

    # Забираем список товаров с РАЗНЫМИ подкатегориями из базы данных с учетом выбранной категории и проходим по ним

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

    newList = natsorted(buttons, key=sorting_by_address)
    markup.inline_keyboard = newList

    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1)
        )
    )
    return markup


# Создаем функцию, которая отдает клавиатуру с кнопками "купить" и "назад" для выбранного товара
async def info_keyboard(address):
    markup = InlineKeyboardMarkup()

    markup.row(
        InlineKeyboardButton(
            text="Відкрити Google Maps", url=(await get_gmaps_url(address)))
    )
    return markup
