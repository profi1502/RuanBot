from data.letter_priorities import lp
from utils.db_api.db_commands import get_cities, get_addresses
from natsort import natsorted


async def sorted_cities():
    ls = await get_cities()

    dc = {}

    #  делаем словарь: город - приоритет
    for name in ls:
        dc[name.city_name] = lp[name.city_name[:1]]
    ls_sorted = []
    #  сортируем по прироритету и по алфавиту
    for i in sorted(dc.items(), key=lambda x: (x[1], x[0])):
        ls_sorted.append(i[0])

    return ls_sorted


async def sorted_addresses(city):
    ls = await get_addresses(city)

    dc = {}
    ls_sorted = []
    #  делаем словарь: адрес имя и айди - приоритет

    for address in ls:
        # address[0] - address_id
        # address[1] - address_name

        addr_info = f'{address[1]} - {address[0]}'
        # костыль с селище
        if 'селище' in address[1] or 'вул.' in address[1] or 'бул.' in address[1] or 'ж/м' in address[1] \
                or 'просп.' in address[1] or 'мкр.' in address[1] or 'пл.' in address[1] \
                or 'пров.' in address[1] or 'ш.' in address[1] \
                or 'майдан' in address[1] or 'наб.' in address[1]:

            address_name = address[1].replace('вул.', '').replace('бул.', '') \
                .replace('ж/м', '').replace('мкр.', '') \
                .replace('просп.', '').replace('пл.', '')\
                .replace('пров.', '').replace('ш.', '')\
                .replace('майдан', '').replace('наб.', '')\
                .replace('селище', '').strip()

            dc[addr_info] = lp[address_name[:1]]

        else:
            dc[addr_info] = lp[address.address_name[:1]]

    #  сортируем по прироритету и по алфавиту
    for i in natsorted(dc.items(), key=lambda x: (x[1], x[0].split(' - ')[0])):
        ls_sorted.append(i[0].split(' - '))

    return ls_sorted
