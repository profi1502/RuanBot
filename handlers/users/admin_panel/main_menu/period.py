import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from Emoji import emoji
from keyboards.default import main_keyboard
from keyboards.inline.admin_panel import cancel
from keyboards.inline.admin_panel.statistic.keyboard import stat_keyboard
from keyboards.inline.admin_panel.statistic.period import keyboard
from keyboards.inline.callback_datas import post_callback
from loader import dp
from states.Period import PeriodState
from utils.db_api.admin_db_methods import count_users
from utils.db_api.db_commands import get_clicks_in_range, get_clicks_today, get_clicks_current_month, \
    get_clicks_last_month, get_users_current_month, get_users_today, get_users_last_month, get_users_in_range
from utils.db_api.models import User, PharmacyNear, StocksActive, OrderMedicineOnline, Bonuses, BonusPoints, \
    CheckBalance, Contacts


@dp.message_handler(text='Назад', state='*')
async def get_message(message: Message, state: FSMContext):
    await message.answer(text='Успешный выход.', reply_markup=ReplyKeyboardRemove())

    await message.answer(text=f'Обирайте{emoji.arrow_down}', reply_markup=keyboard)
    await state.finish()


def period_message(bonus_points_click_method, bonus_points_user_method,
                   check_balance_cm, check_balance_um,
                   pharmacy_near_cm, pharmacy_near_um,
                   stock_active_cm, stock_active_um,
                   contacts_cm, contacts_um,
                   order_medicine_online_cm, order_medicine_online_um,
                   bonuses_cm, bonuses_um,
                   added_user_method):
    return \
        f'Кількість <b>натискань</b> на кнопку "Бонусні бали": ' \
        f'<code>{bonus_points_click_method}</code>\n' \
        f'Кількість <b>юзерів</b> натиснувших "Бонусні бали"": ' \
        f'<code>{bonus_points_user_method}</code>\n\n' \
 \
        f'Кількість <b>натискань</b> на кнопку "Перевірити баланс": ' \
        f'<code>{check_balance_cm}</code>\n' \
        f'Кількість <b>юзерів</b> натиснувших "Перевірити баланс": ' \
        f'<code>{check_balance_um}</code>\n\n' \
 \
        f'Кількість <b>натискань</b> на кнопку "Бонуси у подарунок": ' \
        f'<code>{bonuses_cm}</code>\n' \
        f'Кількість <b>юзерів</b> натиснувших "Бонуси у подарунок": ' \
        f'<code>{bonuses_um}</code>\n\n' \
 \
        f'Кількість <b>натискань</b> на кнопку "Аптеки поблизу": ' \
        f'<code>{pharmacy_near_cm}</code>\n' \
        f'Кількість <b>юзерів</b> натиснувших "Аптеки поблизу": ' \
        f'<code>{pharmacy_near_um}</code>\n\n' \
 \
        f'Кількість <b>натискань</b> на кнопку "Діючі акції": ' \
        f'<code>{stock_active_cm}</code>\n' \
        f'Кількість <b>юзерів</b> натиснувших "Діючі акції": ' \
        f'<code>{stock_active_um}</code>\n\n' \
 \
        f'Кількість <b>натискань</b> на кнопку "Зв\'язатися з нами": ' \
        f'<code>{contacts_cm}</code>\n' \
        f'Кількість <b>юзерів</b> натиснувших "Зв\'язатися з нами": ' \
        f'<code>{contacts_um}</code>\n\n' \
 \
        f'Кількість <b>натискань</b> на кнопку "Замовити ліки онлайн": ' \
        f'<code>{order_medicine_online_cm}</code>\n' \
        f'Кількість <b>юзерів</b> натиснувших "Замовити ліки онлайн": ' \
        f'<code>{order_medicine_online_um}</code>\n\n' \
 \
        f'Кількість добавлених юзерів: <code>{added_user_method}</code>'


@dp.callback_query_handler(post_callback.filter(action='period_today'))
async def period_today(call: CallbackQuery):
    date = datetime.datetime.now().date()
    await call.message.delete()
    list_of_things = []
    for cls, date in [
        [BonusPoints, date],
        [CheckBalance, date],
        [PharmacyNear, date],
        [StocksActive, date],
        [Contacts, date],
        [OrderMedicineOnline, date],
        [Bonuses, date]
    ]:
        for func in (get_clicks_today, get_users_today):
            thing = await func(cls, date)
            list_of_things.append(thing)

    await call.message.answer(f'За сьогодні:\n\n' +
                              period_message(*list_of_things,
                                             # получаем юзеров у которых дата добавления равна переданной дате
                                             await get_clicks_today(User, date)),
                              reply_markup=main_keyboard)


@dp.callback_query_handler(post_callback.filter(action='period_current_month'))
async def period_today(call: CallbackQuery):
    date = datetime.datetime.now().date()
    await call.message.delete()
    list_of_things = []
    for cls, month, year in [
        [BonusPoints, date.month, date.year],
        [CheckBalance, date.month, date.year],
        [PharmacyNear, date.month, date.year],
        [StocksActive, date.month, date.year],
        [Contacts, date.month, date.year],
        [OrderMedicineOnline, date.month, date.year],
        [Bonuses, date.month, date.year],
    ]:
        for func in (get_clicks_current_month, get_users_current_month):
            thing = await func(cls, month, year)
            list_of_things.append(thing)

    await call.message.answer(f'За цей місяць:\n\n' +
                              period_message(*list_of_things,
                                             await get_clicks_current_month(User, date.month, date.year)),
                              reply_markup=main_keyboard)


@dp.callback_query_handler(post_callback.filter(action='period_last_month'))
async def period_today(call: CallbackQuery):
    date = datetime.datetime.now().date()
    await call.message.delete()

    if date.month == 1:
        list_of_things = []
        for cls, month, year in [
            [BonusPoints, 13, date.year - 1],
            [CheckBalance, 13, date.year - 1],
            [PharmacyNear, 13, date.year - 1],
            [StocksActive, 13, date.year - 1],
            [Contacts, 13, date.year - 1],
            [OrderMedicineOnline, 13, date.year - 1],
            [Bonuses, 13, date.year - 1],
        ]:
            for func in (get_clicks_last_month, get_users_last_month):
                thing = await func(cls, month, year)
                list_of_things.append(thing)

        await call.message.answer(f'За минулий місяць:\n\n' +
                                  period_message(*list_of_things,
                                                 await get_clicks_last_month(User, 13, date.year - 1)),
                                  reply_markup=main_keyboard)
    else:
        list_of_things = []
        for cls, month, year in [
            [BonusPoints, date.month, date.year],
            [CheckBalance, date.month, date.year],
            [PharmacyNear, date.month, date.year],
            [StocksActive, date.month, date.year],
            [Contacts, date.month, date.year],
            [OrderMedicineOnline, date.month, date.year],
            [Bonuses, date.month, date.year],
        ]:
            for func in (get_clicks_last_month, get_users_last_month):
                thing = await func(cls, month, year)
                list_of_things.append(thing)

        await call.message.answer(f'За минулий місяць:\n\n' +
                                  period_message(*list_of_things,
                                                 await get_clicks_last_month(User, date.month, date.year)),
                                  reply_markup=main_keyboard)


@dp.callback_query_handler(post_callback.filter(action='period_any'))
async def period_any(call: CallbackQuery):
    await call.message.edit_text('Отправь мне диапазон дат:')
    await call.message.answer('Приклад: <code>2010.10.23-2015.12.23</code>', reply_markup=cancel.keyboard)
    await PeriodState.EnterDate.set()


@dp.message_handler(state=PeriodState.EnterDate, content_types='text')
async def get_new_message(message: Message, state: FSMContext):
    date_range = message.text
    try:
        date1_text = ''.join(date_range.split('-')[0].split('.'))
        date2_text = ''.join(date_range.split('-')[1].split('.'))

        date1 = datetime.datetime.strptime(date1_text, '%Y%m%d').date()
        date2 = datetime.datetime.strptime(date2_text, '%Y%m%d').date()

        list_of_things = []
        for cls, date1, date2 in [
            [BonusPoints, date1, date2],
            [CheckBalance, date1, date2],
            [PharmacyNear, date1, date2],
            [StocksActive, date1, date2],
            [Contacts, date1, date2],
            [OrderMedicineOnline, date1, date2],
            [Bonuses, date1, date2],
        ]:
            for func in (get_clicks_in_range, get_users_in_range):
                thing = await func(cls, date1, date2)
                list_of_things.append(thing)

        await message.answer(f'За {date_range}:\n\n' +
                             period_message(*list_of_things,
                                            await get_clicks_in_range(User, date1, date2)),
                             reply_markup=main_keyboard)
        await state.finish()
    except ValueError:
        await message.answer(f'Ви невірно ввели дату, спробуйте ще раз!'
                             f'\n\nПриклад: <code>2010.10.23-2015.12.23</code>')


@dp.callback_query_handler(post_callback.filter(action='count_users'))
async def count_users_admin_panel(call: CallbackQuery):
    await call.answer(f'Кількість підписників: {await count_users()}', show_alert=True)


@dp.callback_query_handler(post_callback.filter(action='period'))
async def count_users_admin_panel(call: CallbackQuery):
    await call.message.edit_text(f'Обирайте{emoji.arrow_down}', reply_markup=keyboard)


@dp.callback_query_handler(post_callback.filter(action='back_to_period'))
async def back_to_period(call: CallbackQuery):
    await call.message.edit_text(f'Обирайте{emoji.arrow_down}', reply_markup=stat_keyboard)
