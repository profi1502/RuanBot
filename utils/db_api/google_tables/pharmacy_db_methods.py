from __future__ import print_function

from utils.db_api.db_commands import get_cityID, get_addressID
from utils.db_api.google_tables.config import gc
from utils.db_api.models import City, Address, Info

SPREADSHEET_ID = '1i6QNxWANXFnSA2Hq6KTu66WcVSpXQeMX_29Gg2rffFQ'
sh = gc.open_by_key(SPREADSHEET_ID)


async def parse_city():
    rows = sh.worksheet("Города").get('A2:G')
    for row in rows:
        city_ukr = row[0]
        current_city = row
        city_rus_list = []
        transmitter = ''

        if len(current_city) > 1:
            city_rus_list.append(current_city)

        for i in city_rus_list:
            city_rus = ' '.join(i)
            transmitter = city_rus

        city = City(city_name=city_ukr, city_name_rus=transmitter)

        await city.create()


async def parse_address():
    rows = sh.worksheet("Лист1").get('A2:K')
    for row in rows:
        city_name = ' '.join(str(row[1]).replace('\n', '').split())
        address_name = ' '.join(str(row[3]).replace('\n', '').split())
        phone_number = ' '.join(str(row[6]).replace('\n', '').split())
        latitude = ' '.join(str(row[8]).replace('\n', '').split())
        longitude = ' '.join(str(row[9]).replace('\n', '').split())
        city_id = get_cityID(city_name)

        address = Address(city_id=city_id, address_name=address_name,
                          phone_number=phone_number, latitude=latitude, longitude=longitude)

        await address.create()


async def parse_info():
    rows = sh.worksheet("Лист1").get('A2:K')
    for row in rows:
        hash_ = row[0]
        pharmacy_number = ' '.join(str(row[2]).replace('\n', '').split())
        schedule = ' '.join(str(row[5]).replace('\n', '').split())
        phone_number = ' '.join(str(row[6]).replace('\n', '').split())
        latitude = ' '.join(str(row[8]).replace('\n', '').split())
        longitude = ' '.join(str(row[9]).replace('\n', '').split())

        address_id = await get_addressID(phone_number)

        city = Info(address_id=address_id, pharmacy_number=pharmacy_number, schedule=schedule,
                    phone_number=phone_number, latitude=latitude, longitude=longitude, hash=hash_)

        await city.create()
