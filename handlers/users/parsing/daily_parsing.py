from utils.db_api.db_commands import truncate_table
from utils.db_api.google_tables import bonus_data
from utils.db_api.google_tables.pharmacy_db_methods import parse_city, parse_address, parse_info
from utils.db_api.models import City, Address, Info, BonusCards


async def job():
    await truncate_table(City)
    await parse_city()

    await truncate_table(Address)
    await parse_address()

    await truncate_table(Info)
    await parse_info()
