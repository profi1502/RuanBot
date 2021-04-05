from gino import Gino
from gino.schema import GinoSchemaVisitor

from data.config import POSTGRES_URI

db = Gino()


async def create_db():
    await db.set_bind(POSTGRES_URI)

    gino = db.gino
    # Create tables
    gino: GinoSchemaVisitor

    # await gino.drop_all()
    await gino.create_all()
