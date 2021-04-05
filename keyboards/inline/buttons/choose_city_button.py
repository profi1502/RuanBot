# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#
# from utils.db_api.pharmacy_db_methods import get_city1, sortByAlphabet1
#
# buttons = []
#
#
# async def m():
#     listMax = [(await get_city1())[x][0] for x in range(len((await get_city1()))) if len((await get_city1())[x][0]) > 10]
#     listMin = [(await get_city1())[x][0] for x in range(len((await get_city1()))) if len((await get_city1())[x][0]) < 10]
#
#     result = []
#
#     result.extend(
#         list(zip(*[iter(listMin)] * 3)) + ([tuple(listMin[-(len(listMin) % 3):])] if len(listMin) % 3 > 0 else []))
#     result.extend(
#         list(zip(*[iter(listMax)] * 2)) + ([tuple(listMax[-(len(listMax) % 2):])] if len(listMax) % 2 > 0 else []))
#
#     for row in result:
#         row_buttons = []
#         for element in row:
#             row_buttons.append(InlineKeyboardButton(text=element, callback_data=f'showAddress {element}'))
#         buttons.append(row_buttons)
#
#     buttons.sort(key=sortByAlphabet1(buttons))
#     newList = sorted(buttons)
#     print(newList)
#     choose_city = InlineKeyboardMarkup(inline_keyboard=buttons)
#     return choose_city
