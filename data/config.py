import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
INSTAGRAM_URL = str(os.getenv("INSTAGRAM_URL"))
FACEBOOK_URL = str(os.getenv("FACEBOOK_URL"))
RUAN_URL = str(os.getenv("RUAN_URL"))
ORDER_URL = str(os.getenv("ORDER_URL"))

admin_id = os.getenv("ADMIN_ID")
DB_HOST = os.getenv("DB_HOST")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")

admins = [
    455958693, 107177807
]

ip = os.getenv("ip")

#  db - это название базы данных в сервисе в docker-compose.yml
POSTGRES_URI = f"postgres://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}
