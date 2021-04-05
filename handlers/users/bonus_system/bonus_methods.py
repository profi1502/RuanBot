import asyncio
from datetime import datetime

import pytz
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from asyncpg import UniqueViolationError

from Emoji import emoji
from data.config import admins
from keyboards.default import main_keyboard
from keyboards.inline.bonus import rg_card
from keyboards.inline.bonus.keyboard import bonus_gift_keyboard, bonus_keyboard
from keyboards.inline.callback_datas import post_callback
from loader import dp
from utils.db_api.db_commands import update_CardsAndChatID, add_statistic, get_bonus_card
from utils.db_api.google_tables import bonus_data
from utils.db_api.google_tables.bonus_data import getChatID, get_user_card, checkParameter
from utils.db_api.models import MailingBefore17, MailingAfter17, Bonuses, BonusCards, CheckBalance
from utils.misc.ruan import Ruan


@dp.message_handler(text=f'Повернутися в меню{emoji.left_hand}', state='*')
async def show_contacts(message: Message, state: FSMContext):
    await message.edit_text(f'Обирайте{emoji.arrow_down}', reply_markup=main_keyboard)
    await state.finish()


@dp.callback_query_handler(post_callback.filter(action=f'back_to_bonuses'))
async def show_contacts(call: CallbackQuery):
    await call.message.edit_text(f'Для того, щоб перевірити бонуси, Вам необхідно мати бонусну картку. '
                                 'Детальніше про те, де можливо отримати бонусну картку за '
                                 '<a href="https://apteka-ruan.com.ua/bonusnaya-programma">посиланням</a>.\n\n',
                                 reply_markup=bonus_keyboard, disable_web_page_preview=True)


async def set_timer_for_mail(action, chat_id, card):
    tz_kiev = pytz.timezone('Europe/Kiev')
    time_kiev = datetime.now(tz_kiev)

    await bonus_data.update(card=card, chat_id=chat_id)

    try:
        if int(time_kiev.hour) >= 17:
            await action(table_name=MailingAfter17, card=card, chat_id=chat_id)
        else:
            await action(table_name=MailingBefore17, card=card, chat_id=chat_id)
    except UniqueViolationError:
        print(None)


@dp.callback_query_handler(post_callback.filter(action='yes'), state='*')
async def update_card_yes(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        pass

    await set_timer_for_mail(action=update_CardsAndChatID, chat_id=str(call.from_user.id), card=data['card'])

    await call.message.delete()
    await call.message.answer('Дякуємо за реєстрацію. Бонуси будуть нараховані на картку '
                              f'{data["card"]} протягом доби, Ви отримаєте повідомлення😉', reply_markup=main_keyboard)
    await state.finish()


@dp.callback_query_handler(post_callback.filter(action='yes_without_gt'), state='*')
async def update_card_yes(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        pass
    try:

        await update_CardsAndChatID(table_name=BonusCards, chat_id=str(call.from_user.id), card=data['card'])
        await call.message.delete()
        await call.message.answer('Ви успішно оновили карту😉', reply_markup=main_keyboard)
        await state.finish()

    except UniqueViolationError:
        await call.message.delete()
        await call.message.answer('Вказана картка вже зареєстрована😕', reply_markup=main_keyboard)
        await state.finish()


@dp.callback_query_handler(post_callback.filter(action='no'), state='*')
async def update_card_no(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(f'Обирайте{emoji.arrow_down}', reply_markup=main_keyboard)
    await state.finish()


@dp.callback_query_handler(post_callback.filter(action='check_bonus'))
async def check_bonus(call: CallbackQuery):
    await call.message.delete()
    chat_id = str(call.from_user.id)
    if chat_id in await getChatID():
        if await checkParameter(chat_id) == 'Y':
            await call.message.answer(
                f'На вашу картку - <code>{await get_user_card(chat_id)}</code> вже нараховано було 50 бонусів.',
                reply_markup=main_keyboard)
        else:
            await call.message.answer(
                f'Ваша картка - <code>{await get_user_card(chat_id)}</code> вже зареєстрована. Бонуси будуть нараховані протягом доби.',
                reply_markup=main_keyboard)
    else:
        await call.message.answer('Ваша картка не зарєєстрована.',
                                  reply_markup=rg_card.keyboard)


@dp.callback_query_handler(post_callback.filter(action='check_balance'))
async def check_balance(callback: CallbackQuery):
    await callback.answer()
    chat_id = str(callback.from_user.id)
    card_list = await get_bonus_card(chat_id)
    ruan = Ruan(ruan_url='http://ruan.ddns.net', ruan_user='TelegramBot', ruan_password='TelegramBot')

    if callback.from_user.id in admins:
        print(None)
    else:
        date = datetime.now().date()
        await add_statistic(CheckBalance, date, callback.from_user.id)

    if len(card_list) != 0:
        await callback.message.delete()
        await callback.message.answer(
            f'Мої бонуси: <code>{ruan.check_balance(card_list[0][0])}</code> балів',
            reply_markup=main_keyboard)
    else:
        await callback.message.edit_text('Для перевірки балів необхідно додати картку!',
                                         reply_markup=rg_card.keyboard_without_gt)


@dp.callback_query_handler(post_callback.filter(action='gift_bonus'))
async def gift_balance(callback: CallbackQuery):
    await callback.answer()
    if callback.from_user.id in admins:
        print(None)
    else:
        date = datetime.now().date()
        await add_statistic(Bonuses, date, callback.from_user.id)

    await callback.message.edit_text(f'Для того, щоб отримати бонуси, Вам необхідно мати бонусну картку. '
                                     'Детальніше про те, де можливо отримати бонусну картку за '
                                     '<a href="https://apteka-ruan.com.ua/help/programma-loyalnosti/bonusnaya-programma/">посиланням</a>.\n\n'
                                     f'{emoji.warning}50 бонусних балів буде нараховано на вказану картку протягом доби. '
                                     f'<b>Важливо!</b> Бонуси нараховуються один раз!',
                                     reply_markup=bonus_gift_keyboard, disable_web_page_preview=True)
