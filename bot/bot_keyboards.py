from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

class ProductCallback(CallbackData, prefix="product"):
    foo: str
    bar: int

def get_start_kb():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Меню', callback_data='get_menu')],
        [InlineKeyboardButton(text='Козу гриль', callback_data='get_kozu')],
        [InlineKeyboardButton(text='Корзинка', callback_data='get_cart')],
    ])
    return ikb