import asyncio
from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from asyncpg import UniqueViolationError

from Emoji import emoji
from handlers.users.bonus_system.bonus_methods import set_timer_for_mail
from keyboards.default import main_keyboard
from keyboards.inline.bonus import change_card, cancel
from keyboards.inline.callback_datas import post_callback
from loader import dp, bot
from states.BonuSystem import Bonus
from utils.db_api.db_commands import add_CardAndChatID, add_bonus_card
from utils.db_api.google_tables import bonus_data
from utils.db_api.google_tables.bonus_data import getChatID, get_cards
from utils.misc.ruan import Ruan


@dp.callback_query_handler(post_callback.filter(action='get_bonus'))
async def enter_card(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer('Будь ласка, введіть номер бонусної картки.\n\nПриклад: <code>2398230000000</code>',
                              reply_markup=cancel.keyboard)

    await Bonus.EnterCard.set()


@dp.message_handler(state=Bonus.EnterCard, content_types='text')
async def register_card(message: Message, state: FSMContext):
    await message.answer(text='Початок завантаження', reply_markup=ReplyKeyboardRemove())
    ruan = Ruan(ruan_url='http://ruan.ddns.net', ruan_user='TelegramBot', ruan_password='TelegramBot')

    chat_id = str(message.from_user.id)
    card = await bonus_data.get_user_card(chat_id)
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

    elif await bonus_data.checkParameter(chat_id) is not None and await bonus_data.checkParameter(chat_id) == 'Y':

        await message.answer(f'Ми нарахували Вам бонуси раніше на картку '
                             f'<code>{card}</code>{emoji.wink_smile}', reply_markup=main_keyboard)
        await state.finish()
    else:
        await state.update_data(card=new_card)

        if len(new_card) == 13:
            if new_card.startswith('239823'):

                # если юзер ввел карту, которая уже есть в базе то мы его шлем нафиг
                if new_card not in await get_cards():

                    if chat_id in await getChatID():
                        await message.answer(
                            f'Ви бажаєте змінити картку, яку зареєстрували раніше <code>{card}</code>? '
                            f'Номер карти для зараховування балів буде змінений на <code>{new_card}</code>.',
                            reply_markup=change_card.keyboard)

                    else:

                        await bonus_data.put(new_card, chat_id)
                        await set_timer_for_mail(action=add_CardAndChatID, chat_id=str(message.from_user.id),
                                                 card=new_card)
                        date = datetime.now().date()
                        try:
                            await add_bonus_card(card=new_card, date=date, chat_id=chat_id)

                            await message.answer('Дякуємо за реєстрацію. Бонуси будуть нараховані на картку '
                                                 f'<code>{new_card}</code> протягом доби, Ви отримаєте повідомлення😉',
                                                 reply_markup=main_keyboard)
                            await state.finish()
                        except UniqueViolationError:
                            await message.answer('Дякуємо за реєстрацію. Бонуси будуть нараховані на картку '
                                                 f'<code>{new_card}</code> протягом доби, Ви отримаєте повідомлення😉',
                                                 reply_markup=main_keyboard)
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