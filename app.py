from datetime import datetime

from aiogram import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers import dp
import filters
import middlewares

from handlers.users.parsing import daily_parsing
from utils.db_api.db_commands import truncate_table
from utils.db_api.google_tables import bonus_data
from utils.db_api.google_tables.pharmacy_db_methods import parse_city, parse_address, parse_info
from utils.db_api.models import City, Address, Info, BonusCards
from utils.notify_admins import on_startup_notify
from handlers.users.bonus_system.Mailing import Before17, After17
from loader import bot, storage
from utils.db_api.database import create_db


async def on_startup(dispatcher):
    filters.setup(dispatcher)
    middlewares.setup(dispatcher)

    await create_db()

    # await truncate_table(Info)
    #
    # await truncate_table(Address)
    #
    # await truncate_table(City)
    #
    # await truncate_table(BonusCards)
    # await bonus_data.parse()
    #
    # await parse_city()
    # await parse_address()
    # await parse_info()

    # date = datetime.now().date()
    # await swipe_data(date)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(daily_parsing.job, 'cron', hour=3, minute=0, timezone='Europe/Kiev')
    scheduler.add_job(Before17.job, 'cron', hour=19, minute=0, timezone='Europe/Kiev')
    scheduler.add_job(After17.job, 'cron', hour=10, minute=0, timezone='Europe/Kiev')
    scheduler.start()

    await on_startup_notify(dispatcher)


async def on_shutdown(dispatcher):
    await bot.close()
    await storage.close()

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
