from keyboards.default import main_keyboard
from loader import bot
from utils.db_api.db_commands import get_CardsAndChatID, delete_CardFromTable
from utils.db_api.google_tables.bonus_data import checkParameter
from utils.db_api.models import MailingBefore17


async def job():
    table = MailingBefore17
    try:
        for cai in await get_CardsAndChatID(table):
            chat_id = cai[1]
            card = cai[0]

            if await checkParameter(chat_id) == 'Y':
                await bot.send_message(chat_id=chat_id,
                                       text=f'Вітаємо!\nЗа реєстрацію у боті ми '
                                            f'нарахували Вам 50 балів на картку: <code>{card}</code>',
                                       reply_markup=main_keyboard)
                await delete_CardFromTable(table, card)
    except IndexError:
        print('В базе данных нет пользователей')
