from typing import List

from sqlalchemy import or_, and_, distinct
from sqlalchemy.sql.elements import Extract

from utils.db_api.database import db
from utils.db_api.models import City, Address, Info, StockText, BonusCards, User


async def get_cities() -> List[City]:
    return await City.query.gino.all()


async def get_addresses(city_name) -> List[Address]:
    city_urk = "%{}%".format(city_name)

    request = await db.select([Address.id, Address.address_name]). \
        select_from(City.join(Address, City.id == Address.city_id)). \
        where(or_(City.city_name == city_name, City.city_name_rus.like(city_urk))).gino.all()

    return request


async def get_info(address):
    info = await db.select([City.city_name, Address.address_name, Info.pharmacy_number,
                            Info.schedule, Info.phone_number, Info.latitude, Info.longitude]
                           ).select_from(City.join(Address, City.id == Address.city_id)
                                         .join(Info, Address.id == Info.address_id)
                                         ).where(Info.address_id == address).gino.all()
    city_name = info[0][0]
    address_name = info[0][1]
    pharmacy_number = info[0][2]
    schedule = info[0][3]
    phone_number = info[0][4]

    answer = f'м. {city_name}\n' \
             f'{address_name}\n' \
             f'Режим роботи аптеки:\n' \
             f'{schedule}\n' \
             f'{pharmacy_number}\n' \
             f'{phone_number}'

    return answer


async def get_hash(address):
    hash_ = await db.select([Info.hash]
                            ).select_from(Info.join(Address, Address.id == Info.address_id)
                                          ).where(Address.id == address).gino.all()

    photo_name = hash_[0][0]

    return photo_name


async def get_cityID(city_name):
    city_id = await db.select([City.id]).where(City.city_name == city_name).gino.scalar()
    return city_id


async def get_addressID(phone_number):
    address_id = await db.select([Address.id]).where(Address.phone_number == phone_number).gino.scalar()
    return address_id


async def get_location(city_name) -> List[Address]:
    city_urk = "%{}%".format(city_name)

    location = await db.select([Address.id, Address.address_name, Address.latitude, Address.longitude]
                               ).select_from(City.join(Address, City.id == Address.city_id)
                                             ).where(or_(City.city_name == city_name,
                                                         City.city_name_rus.like(city_urk))).gino.all()
    return location


async def get_gmaps_url(address):
    info = await db.select([Info.latitude, Info.longitude]
                           ).select_from(Address.join(Info, Address.id == Info.address_id)
                                         ).where(Info.address_id == address).gino.all()
    latitude = info[0][0]
    longitude = info[0][1]

    return f'http://www.google.com/maps?q={latitude},+{longitude}'


async def get_CardsAndChatID(table_name: db.Model):
    request = await db.select([table_name.card, table_name.chat_id]).gino.all()

    return request


async def add_CardAndChatID(table_name: db.Model, card, chat_id):
    table = table_name(card=card, chat_id=chat_id)

    await table.create()


async def update_CardsAndChatID(table_name: db.Model, card, chat_id):
    request = await db.update(table_name).where(table_name.chat_id == chat_id).values(card=card).gino.all()

    return request


async def delete_CardFromTable(table_name: db.Model, card):
    request = await db.delete(table_name).where(table_name.card == card).gino.all()

    return request


async def truncate_table(table_name: db.Model):
    request = await table_name.delete.gino.status()

    return request


async def add_StockText(text):
    table = StockText(text=text)

    await table.create()


async def get_StockText():
    request = await db.select([StockText.text]).gino.all()

    return request[0][0]


async def add_statistic(table: db.Model, date, chat_id):
    table = table(date=date, chat_id=chat_id)

    await table.create()


# async def update_period(date):
#     request = await db.update(Period).where(Period.date == date).values(count_clicks=Period.count_clicks + 1).gino.all()
#
#     return request


async def get_clicks_in_range(table: db.Model, date1, date2):
    request = await db.select([db.func.count(table.date)
                              .filter(and_(date2 >= table.date,
                                           date1 <= table.date))]).gino.scalar()

    return request


async def get_users_in_range(table: db.Model, date1, date2):
    request = await db.select([db.func.count(distinct(table.chat_id))
                              .filter(and_(date2 >= table.date,
                                           date1 <= table.date))]).gino.scalar()

    return request


async def get_clicks_today(table: db.Model, date):
    request = await db.select([db.func.count(table.date)
                              .filter(date == table.date)]).gino.scalar()

    return request


async def get_users_today(table: db.Model, date):
    request = await db.select([db.func.count(distinct(table.chat_id))
                              .filter(date == table.date)]).gino.scalar()

    return request


async def get_clicks_current_month(table: db.Model, month, year):
    request = await db.select([db.func.count(table.date)
                              .filter(and_(Extract("month", table.date) == month),
                                      and_(Extract("year", table.date) == year))]).gino.scalar()

    return request


async def get_users_current_month(table: db.Model, month, year):
    request = await db.select([db.func.count(distinct(table.chat_id))
                              .filter(and_(Extract("month", table.date) == month),
                                      and_(Extract("year", table.date) == year))]).gino.scalar()

    return request


async def get_clicks_last_month(table: db.Model, month, year):
    request = await db.select([db.func.count(table.date)
                              .filter(and_(Extract("month", table.date) == month - 1),
                                      and_(Extract("year", table.date) == year))]).gino.scalar()

    return request


async def get_users_last_month(table: db.Model, month, year):
    request = await db.select([db.func.count(distinct(table.chat_id))
                              .filter(and_(Extract("month", table.date) == month - 1),
                                      and_(Extract("year", table.date) == year))]).gino.scalar()

    return request


async def add_bonus_card(card, date, chat_id):
    table = BonusCards(card=card, chat_id=chat_id, date=date)

    await table.create()


async def get_bonus_card(chat_id):
    r = await db.select([BonusCards.card]).where(BonusCards.chat_id == chat_id).gino.all()

    return r


# async def swipe_data(date):
#     r = await db.select([Users.chat_id]).gino.all()
#     for i in r:
#         table = User(chat_id=i[0], date=date)
#         await table.create()

async def delete_Blocked_User(chat_id):
    request = await db.delete(User).where(User.chat_id == chat_id).gino.all()

    return request
