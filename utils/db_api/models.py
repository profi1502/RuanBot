from sqlalchemy import Column, Integer, Sequence, BigInteger, String, sql, DateTime

from utils.db_api.database import db


class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True, autoincrement=True)
    date = Column(DateTime)
    chat_id = Column(BigInteger, unique=True)
    query: sql.select


class Users(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('users_id_seq'), primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, unique=True)
    query: sql.select


class City(db.Model):
    __tablename__ = 'city'

    id = Column(Integer, Sequence('city_id_seq'), primary_key=True, autoincrement=True)
    city_name = Column(String(30))
    city_name_rus = Column(String(200))

    query: sql.select


class Address(db.Model):
    __tablename__ = 'address'

    id = Column(Integer, Sequence('address_id_seq'), primary_key=True, autoincrement=True)
    city_id = Column(Integer, db.ForeignKey('city.id', ondelete='CASCADE'))
    address_name = Column(String(200))
    latitude = Column(String(50))
    longitude = Column(String(50))

    phone_number = Column(String(20))

    query: sql.select


class Info(db.Model):
    __tablename__ = 'info'

    id = Column(Integer, Sequence('info_id_seq'), primary_key=True, autoincrement=True)
    address_id = Column(Integer, db.ForeignKey('address.id', ondelete='CASCADE'))
    pharmacy_number = Column(String(100))
    schedule = Column(String(100))
    phone_number = Column(String(100))
    latitude = Column(String(50))
    longitude = Column(String(50))
    hash = Column(String(30))
    query: sql.select


class BonusCards(db.Model):
    __tablename__ = 'bonus_cards'
    id = Column(Integer, Sequence('bonus_cards_id_seq'), primary_key=True, autoincrement=True)
    card = Column(String(50), unique=True)
    date = Column(DateTime)
    chat_id = Column(String(50), unique=True)
    query: sql.select


class MailingBefore17(db.Model):
    __tablename__ = 'mailing_before17'
    id = Column(Integer, Sequence('mailing_before17_id_seq'), primary_key=True, autoincrement=True)
    card = Column(String(50))
    chat_id = Column(String(50), unique=True)
    query: sql.select


class MailingAfter17(db.Model):
    __tablename__ = 'mailing_after17'
    id = Column(Integer, Sequence('mailing_after1717_id_seq'), primary_key=True, autoincrement=True)
    card = Column(String(50))
    chat_id = Column(String(50), unique=True)
    query: sql.select


class StockText(db.Model):
    __tablename__ = 'stock_text'
    text = Column(String(5000))
    query: sql.select


class PharmacyNear(db.Model):
    __tablename__ = 'pharmacy_near'
    date = Column(DateTime)
    chat_id = Column(BigInteger)
    query: sql.select


class StocksActive(db.Model):
    __tablename__ = 'stocks_active'
    date = Column(DateTime)
    chat_id = Column(BigInteger)
    query: sql.select


class OrderMedicineOnline(db.Model):
    __tablename__ = 'order_medicine_online'
    date = Column(DateTime)
    chat_id = Column(BigInteger)
    query: sql.select


class Bonuses(db.Model):
    __tablename__ = 'bonuses'
    date = Column(DateTime)
    chat_id = Column(BigInteger)
    query: sql.select


class BonusPoints(db.Model):
    __tablename__ = 'bonus_points'
    date = Column(DateTime)
    chat_id = Column(BigInteger)
    query: sql.select


class CheckBalance(db.Model):
    __tablename__ = 'check_balance'
    date = Column(DateTime)
    chat_id = Column(BigInteger)
    query: sql.select


class Contacts(db.Model):
    __tablename__ = 'contacts'
    date = Column(DateTime)
    chat_id = Column(BigInteger)
    query: sql.select
