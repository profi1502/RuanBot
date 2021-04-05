import os
from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InputMediaPhoto, ReplyKeyboardRemove

from Emoji import emoji
from data.config import admins

from keyboards.default import pharmacy_near_keyboard, main_keyboard
from keyboards.inline.bonus.keyboard import bonus_keyboard
from keyboards.inline.buttons import order_keyboard
from keyboards.inline.buttons import social_network_keyboard
from keyboards.inline.buttons import website_keyboard
from loader import dp
from utils.db_api import db_commands
from utils.db_api.db_commands import add_statistic
from utils.db_api.models import OrderMedicineOnline, StocksActive, PharmacyNear, BonusPoints, Contacts
from utils.misc import rate_limit


@rate_limit(5, 'Бонусы')
@dp.message_handler(text=f'💎 Бонусні бали')
async def show_bonus(message: Message):

    if message.from_user.id in admins:
        print(None)
    else:
        date = datetime.now().date()
        await add_statistic(BonusPoints, date, message.from_user.id)

    await message.answer('Бонуси', reply_markup=ReplyKeyboardRemove())
    await message.answer(f'Для того, щоб перевірити бонуси, Вам необхідно мати бонусну картку. '
                         'Детальніше про те, де можливо отримати бонусну картку за '
                         '<a href="https://apteka-ruan.com.ua/help/programma-loyalnosti/bonusnaya-programma/">посиланням</a>.',
                         reply_markup=bonus_keyboard, disable_web_page_preview=True)


@rate_limit(5, 'Аптеки поблизу')
@dp.message_handler(text=f'{emoji.magnifying_glass} Аптеки поблизу')
async def show_near_pharmacy(message: Message):

    if message.from_user.id in admins:
        print(None)
    else:
        date = datetime.now().date()
        await add_statistic(PharmacyNear, date, message.from_user.id)

    await message.answer(f'Обирайте{emoji.arrow_down}', reply_markup=pharmacy_near_keyboard)


@rate_limit(5, 'Діючі акції')
@dp.message_handler(text=f'{emoji.shop} Діючі акції')
async def show_stocks(message: Message):

    if message.from_user.id in admins:
        print(None)
    else:
        date = datetime.now().date()
        await add_statistic(StocksActive, date, message.from_user.id)

    path = '/src/stocks/photos'
    files = [f for f in os.listdir(path)
             if os.path.isfile(os.path.join(path, f))]

    try:
        caption = await db_commands.get_StockText()
    except IndexError:
        caption = 'None'

    if files:

        media = [InputMediaPhoto(open(f'/src/stocks/photos/{files[0]}', 'rb'), None, caption)]
        files.__delitem__(0)

        for photo in files:
            media.append(InputMediaPhoto(open(f'/src/stocks/photos/{photo}', 'rb')))

        await message.answer_media_group(media)
    else:
        await message.answer('На даний момент акцій не виявлено :(')


@rate_limit(5, 'Зв\'язатися з нами')
@dp.message_handler(text=f'{emoji.phone} Зв\'язатися з нами')
async def show_contacts(message: Message):
    if message.from_user.id in admins:
        print(None)
    else:
        date = datetime.now().date()
        await add_statistic(Contacts, date, message.from_user.id)

    await message.answer(f'{emoji.pager} 0 800 75 80 18\n{emoji.envelope_with_arrow} info@apteka-ruan.com.ua')


@rate_limit(5, 'Соц. мережі')
@dp.message_handler(text=f'{emoji.networks} Соц. мережі')
async def show_social_network(message: Message):
    await message.answer('Підписуйтесь на наші соц. мережі, щоб завжди бути в курсі подій)',
                         reply_markup=social_network_keyboard)


@rate_limit(5, 'Замовити ліки онлайн')
@dp.message_handler(text=f'{emoji.pill} Замовити ліки онлайн')
async def show_link(message: Message):

    if message.from_user.id in admins:
        print(None)
    else:
        date = datetime.now().date()
        await add_statistic(OrderMedicineOnline, date, message.from_user.id)

    await message.answer(f'Замовити ліки онлайн можна на нашому сайті{emoji.arrow_down}',
                         reply_markup=website_keyboard)


@rate_limit(5, 'Власне аптечне виробництво')
@dp.message_handler(text=f'{emoji.pharmacy} Власне аптечне виробництво')
async def show_pharmacy_production(message: Message):
    await message.answer('Виготовлення <b>лікарських та лікувально-косметичних засобів</b> за індивідуальнім '
                         'замовленням в '
                         f'умовах власного аптечного виробництва{emoji.arrow_down}', reply_markup=order_keyboard)


@rate_limit(5, 'Повернутися в меню')
@dp.message_handler(text=f'Повернутися в меню{emoji.left_hand}', state='*')
async def back_to_menu(message: Message, state: FSMContext):
    await message.answer(f'Обирайте{emoji.arrow_down}', reply_markup=main_keyboard)

    await state.finish()
