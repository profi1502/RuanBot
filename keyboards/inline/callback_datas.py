from aiogram.utils.callback_data import CallbackData

menu_cd = CallbackData("show_menu", "level", "city", "address")


def make_callback_data(level, city="0", address=0):
    return menu_cd.new(level=level, city=city, address=address)


post_callback = CallbackData('create_post', 'action')
