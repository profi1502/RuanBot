from datetime import datetime

from aiogram import types
from asyncpg import UniqueViolationError

from utils.db_api.database import db
from utils.db_api.models import User


async def add_new_user() -> User:
    user = types.User.get_current()
    new_user = User()
    new_user.date = datetime.now().date()
    new_user.chat_id = user.id

    try:
        await new_user.create()
        return new_user
    except UniqueViolationError:
        print('Such user already exists!')


async def count_users() -> int:
    total = await db.func.count(User.id).gino.scalar()
    return total
