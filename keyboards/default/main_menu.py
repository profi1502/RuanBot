from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from Emoji import emoji

main_keyboard = ReplyKeyboardMarkup(
    # KeyboardButton(f'{emoji.gift} Бонуси у подарунок'),
    keyboard=[
        [
            KeyboardButton(f'💎 Бонусні бали'),
        ],
        [
            KeyboardButton(f'{emoji.magnifying_glass} Аптеки поблизу'),
            KeyboardButton(f'{emoji.shop} Діючі акції'),
        ],
        [
            KeyboardButton(f'{emoji.phone} Зв\'язатися з нами'),
            KeyboardButton(f'{emoji.networks} Соц. мережі'),
        ],
        [
            KeyboardButton(f'{emoji.pill} Замовити ліки онлайн'),
        ],
        [
            KeyboardButton(f'{emoji.pharmacy} Власне аптечне виробництво'),
        ],
    ],
    resize_keyboard=True,
)
