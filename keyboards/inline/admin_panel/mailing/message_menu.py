from aiogram.types import InlineKeyboardMarkup
from keyboards.inline.admin_panel.mailing.main_keyboard import delete_url_button, add_url_button, delete_stock_button, \
    add_stock_button, delete_contact_button, add_contact_button


async def variants(cash, markup=None):
    if not markup:
        markup = InlineKeyboardMarkup()

    if 'url_button' in cash:
        markup.add(delete_url_button)
    else:
        markup.add(add_url_button)

    if 'stocks' in cash:
        markup.add(delete_stock_button)
    else:
        markup.add(add_stock_button)

    if 'contacts' in cash:
        markup.add(delete_contact_button)
    else:
        markup.add(add_contact_button)

    return markup




