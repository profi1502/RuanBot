import asyncio
from datetime import datetime

import pytz
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from asyncpg import UniqueViolationError

from keyboards.default import main_keyboard
from keyboards.inline.bonus import change_card, cancel
from keyboards.inline.callback_datas import post_callback
from loader import dp, bot
from states.BonuSystem import Bonus
from utils.db_api.db_commands import add_bonus_card, get_bonus_card
from utils.misc.ruan import Ruan


@dp.callback_query_handler(post_callback.filter(action='add_replace_card'))
async def enter_card(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer('Будь ласка, введіть номер бонусної картки.\n\nПриклад: <code>2398230000000</code>',
                              reply_markup=cancel.keyboard)

    await Bonus.EnterCardWithoutGT.set()


@dp.message_handler(state=Bonus.EnterCardWithoutGT, content_types='text')
async def register_card(message: Message, state: FSMContext):
    await message.answer(text='Початок завантаження', reply_markup=ReplyKeyboardRemove())
    ruan = Ruan(ruan_url='http://ruan.ddns.net', ruan_user='TelegramBot', ruan_password='TelegramBot')

    chat_id = str(message.from_user.id)
    card_list = await get_bonus_card(chat_id)
    new_card = message.text
    card: str
    new_card: str

    await message.bot.send_message(chat_id=chat_id, text='Йде обробка даних')
    await bot.send_chat_action(chat_id=chat_id, action="upload_document")

    # равно двум потому по выдает кавычки ""
    if len(ruan.check_card(new_card)) == 2:
        await message.answer('Нажаль дана картка не зареєстрована. Якщо у Вас виникли питання, '
                             'будь ласка напишіть нам на адресу info@apteka-rua.com.ua',
                             reply_markup=main_keyboard)
        await state.finish()

    else:
        await state.update_data(card=new_card)

        if len(new_card) == 13:
            if new_card.startswith('239823'):

                # если юзер ввел карту, которая уже есть в базе то мы его шлем нафиг
                if new_card not in card_list:

                    if len(card_list) != 0:
                        await message.answer(
                            f'Ви бажаєте змінити картку, яку зареєстрували раніше <code>{card_list[0][0]}</code>? '
                            f'Номер карти для перевірки балів буде змінений на <code>{new_card}</code>.',
                            reply_markup=change_card.keyboard_without_gt)

                    else:
                        date = datetime.now().date()
                        try:
                            await add_bonus_card(card=new_card, date=date, chat_id=chat_id)
                            await message.answer('Ваша картка успішно добавлена😉',
                                                 reply_markup=main_keyboard)
                            await state.finish()
                        except UniqueViolationError:
                            await message.answer('Вказана картка вже зареєстрована😕', reply_markup=main_keyboard)
                            await state.finish()

                else:
                    await message.answer('Вказана картка вже зареєстрована😕', reply_markup=main_keyboard)
                    await state.finish()

            else:
                await message.answer(
                    'Нажаль Ваша картка - не бонусна. Бонусна картка починається з цифр 239823.....\n\n'
                    'Спробуйте ще раз:', reply_markup=cancel.keyboard)
        else:
            await message.answer('Номер картки повинен складатися з 13 цифр.....\n\n'
                                 'Спробуйте ще раз:', reply_markup=cancel.keyboard)
