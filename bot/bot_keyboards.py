from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from bot.models import Category, Product, Cart, CartItem
from asgiref.sync import sync_to_async

class CategoryCallback(CallbackData, prefix="category"):
    id: int
    action: str

class ProductCallback(CallbackData, prefix="product"):
    id: int
    action: str

class CartCallback(CallbackData, prefix="cart"):
    id: int
    action: str

def get_kozu():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Заказать', callback_data='order_kozu'),InlineKeyboardButton(text='Назад', callback_data='get_start')],
    ], row_width=2)
    return ikb

def get_start_kb(user_id):
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Меню', callback_data='get_menu')],
        [InlineKeyboardButton(text='Козу гриль', callback_data='get_kozu')],
        [InlineKeyboardButton(text='Корзинка', callback_data=CartCallback(id=user_id, action='get').pack())],
    ])
    return ikb

@sync_to_async
def category_menukb():
    categories = Category.objects.all()
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=i.name, callback_data=CategoryCallback(id=i.id, action='get').pack()) for i in categories],
        [InlineKeyboardButton(text='Назад', callback_data='get_start')]
    ], row_width=2)
    return ikb

@sync_to_async
def category_productskb(id,user_id):
    category = Category.objects.get(id=id)
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{i.title}", callback_data=ProductCallback(id=i.id, action='get').pack()) for i in Product.objects.all().filter(category = category)],
        [InlineKeyboardButton(text='Назад', callback_data='get_menu'), InlineKeyboardButton(text='Корзинка', callback_data=CartCallback(id=user_id, action='get').pack())]
    ], row_width=2) 
    return [ikb, category]

def get_product_detailkb(id,back_id):
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Убрать', callback_data=ProductCallback(id=id, action='remove_one').pack()),InlineKeyboardButton(text='Добавить', callback_data=ProductCallback(id=id, action='add_one').pack())],
        [InlineKeyboardButton(text='Назад', callback_data=CategoryCallback(id=back_id, action='get').pack())],
    ])
    return ikb

def get_zakazkb(user_id):
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Подтвердить заказ', callback_data=CartCallback(id=user_id, action='confirm').pack()),InlineKeyboardButton(text='Отменить заказ', callback_data=CartCallback(id=user_id, action='delete').pack())],
        [InlineKeyboardButton(text='Назад', callback_data='get_start')],
    ])
    return ikb

#!admin keyboards
def get_adminkb():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Добавить товар', callback_data='add_product'),InlineKeyboardButton(text='Все товары', callback_data='get_all_product')],
        [InlineKeyboardButton(text='Назад', callback_data='back')],
    ])
    return ikb

def get_create_productkb():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Сохранить товар', callback_data='save_product'),InlineKeyboardButton(text='Удалить товар', callback_data='delete_product')],
    ])
    return ikb