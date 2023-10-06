from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_start_kb():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Меню', callback_data='get_all_products')],
        [InlineKeyboardButton(text='Козу гриль', callback_data='get_kozu')],
        [InlineKeyboardButton(text='Корзинка', callback_data='get_cart')],
    ])
    return ikb