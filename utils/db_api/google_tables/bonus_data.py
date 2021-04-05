import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime

from utils.db_api.google_tables.config import gc
from utils.db_api.models import BonusCards

SPREADSHEET_ID = '1tFu8p2TbYW-18E39h77hBzYBujNwFItjSN1Uk4CXIlk'

sh = gc.open_by_key(SPREADSHEET_ID)
worksheet = sh.sheet1


async def run_blocking_io(func, *args):
    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, func, *args)
    return result


async def put(card, chat_id):
    card = card
    date = datetime.today().strftime('%d/%m/%Y')
    status = 'N'
    chat_id = chat_id
    values = [card, date, status, chat_id]
    await run_blocking_io(worksheet.append_row, values)


async def parse():
    for row in sh.worksheet("Cards").get('A2:D'):
        card = row[0]
        date = row[1]
        status = row[2]
        chat_id = row[3]

        bonus = BonusCards(card=card, date=date, status=status, chat_id=chat_id)

        await bonus.create()


async def update(card, chat_id):
    date = datetime.today().strftime('%d/%m/%Y')
    status = 'N'

    index = await get_chatID_inx(chat_id)

    values = [card, date, status, chat_id]

    # прибавляем 2 так как в списке отчет идет с нуля, а в таблице с 1 (и учитываем, что у нас первая строка хедеры).
    await run_blocking_io(sh.worksheet('Cards').batch_update, [{
        'range': f'A{index + 2}',
        'values': [values]
    }])


async def checkParameter(chat_id):
    for row in sh.worksheet('Cards').get_all_records():
        if str(row['Айди']) == str(chat_id):
            return row['Статус']


async def get_user_card(chat_id):
    for row in sh.worksheet('Cards').get_all_records():
        if str(row['Айди']) == str(chat_id):
            return row['Карта']


async def get_chatID_inx(chat_id):
    ls = []
    for row in sh.worksheet("Cards").get('A2:D'):
        ci = row[3]
        ls.append(ci)

    try:
        return ls.index(chat_id)
    except ValueError:
        return None


async def getChatID():
    ls = []
    for row in sh.worksheet('Cards').get_all_records():
        ls.append(str(row['Айди']))
    return ls


async def get_cards():
    ls = []
    for row in sh.worksheet('Cards').get_all_records():
        ls.append(str(row['Карта']))
    return ls
