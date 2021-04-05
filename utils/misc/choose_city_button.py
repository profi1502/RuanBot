from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.users.choose_city.sorting_by_city import sorted_cities

buttons = []


async def m():
    main_list = await sorted_cities()
    listMax = []
    listMin = []
    for city in main_list:
        if len(city) > 12.5:
            listMax.append(city)
        else:
            listMin.append(city)

    result = []

    result.extend(
        list(zip(*[iter(listMin)] * 3)) + ([tuple(listMin[-(len(listMin) % 3):])] if len(listMin) % 3 > 0 else []))
    result.extend(
        list(zip(*[iter(listMax)] * 2)) + ([tuple(listMax[-(len(listMax) % 2):])] if len(listMax) % 2 > 0 else []))

    for row in result:
        row_buttons = []
        for element in row:
            row_buttons.append(InlineKeyboardButton(text=element, callback_data=f'showAddress {element}'f'showAddress {element}'))
        buttons.append(row_buttons)

    newList = sorted(buttons, key=lambda x: x[0].text)
    choose_city = InlineKeyboardMarkup(inline_keyboard=newList)
    return choose_city
