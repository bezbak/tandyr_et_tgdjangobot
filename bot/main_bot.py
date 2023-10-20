from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from django.conf import settings
from . import bot_keyboards as kb
from . import texts as txt
from . import bot_db_handlers as db
from . import statesform as st


storage=MemoryStorage()

bot = Bot(token=settings.TOKEN, parse_mode='HTML')
dp = Dispatcher(storage=storage)

#! main handlers##############################

@dp.message(F.text == '/start')
async def command_start(message : types.Message):
    user = await db.start_user(message.from_user.id, message.from_user.username)
    if user.is_admin:
        await message.answer(text = "Вы зашли в админ панель", reply_markup=kb.get_adminkb())
    else:
        await message.answer(text = txt.text1, reply_markup=kb.get_start_kb(message.from_user.id))

@dp.callback_query(F.data == 'get_menu')
async def get_menu(callback: types.CallbackQuery):
    ikb = await kb.category_menukb()
    await callback.answer()
    await callback.message.answer(text = txt.text2, reply_markup=ikb)

@dp.callback_query(F.data == 'get_kozu')
async def get_menu(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(text = txt.text3, reply_markup=kb.get_kozu())

@dp.callback_query(F.data == 'get_start')
async def get_menu(callback: types.CallbackQuery):
    callback.answer()
    user = await db.start_user(callback.message.from_user.id, callback.message.from_user.username)
    if user.is_admin:
        await callback.message.answer(text = "Вы зашли в админ панель", reply_markup=kb.get_adminkb())
    else:
        await callback.message.answer(text = txt.text1, reply_markup=kb.get_start_kb(callback.from_user.id))

#! products handlers##############################

@dp.callback_query(kb.CategoryCallback.filter(F.action == 'get'))
async def get_menu(callback: types.CallbackQuery, callback_data: kb.CategoryCallback):
    res = await kb.category_productskb(callback_data.id, callback.from_user.id)
    await callback.answer()
    await callback.message.answer(text = f'⭐️⭐️ <b> {res[1].name} </b>⭐️⭐️', reply_markup=res[0])

@dp.callback_query(kb.ProductCallback.filter(F.action == 'get'))
async def get_menu(callback: types.CallbackQuery, callback_data: kb.ProductCallback):
    res = await db.product_detail(callback_data.id)
    category = await db.category_get_by_product(res.id)
    await callback.answer()
    await callback.message.answer( text=f"<b>{res.title}</b>\n{res.price}", reply_markup=kb.get_product_detailkb(res.id,category.id))


@dp.callback_query(kb.ProductCallback.filter(F.action == 'add_one'))
async def get_menu(callback: types.CallbackQuery, callback_data: kb.ProductCallback):
    res = await db.product_add_or_remove_to_cart(callback_data.id, callback.from_user.id, 'add_one')
    await callback.answer(text=f"Вы добавили один продукт, колличество: {res.quantity}")

@dp.callback_query(kb.ProductCallback.filter(F.action == 'remove_one'))
async def get_menu(callback: types.CallbackQuery, callback_data: kb.ProductCallback):
    res = await db.product_add_or_remove_to_cart(callback_data.id, callback.from_user.id, 'remove_one')
    await callback.answer(text=f"Вы убрали один продукт, колличество: {res.quantity}") if res.quantity != 0 else await callback.answer(text=f"Больше нельза удалить, колличество: {res.quantity}") 

#! cart handlers##############################

@dp.callback_query(kb.CartCallback.filter(F.action == 'get'))
async def get_cart(callback: types.CallbackQuery, callback_data: kb.CartCallback):
    await callback.answer('Загрузка...')
    cart_list = await db.cart_get(callback.from_user.id)
    await callback.message.answer(cart_list, reply_markup=kb.get_zakazkb(callback.from_user.id))

@dp.callback_query(kb.CartCallback.filter(F.action == 'confirm'))
async def confirm_cart(callback: types.CallbackQuery, callback_data: kb.CartCallback):
    await callback.answer('')
    await callback.message.answer('Мы приняли ваш заказ. Ожидайте ответа от менеджера', reply_markup=kb.get_start_kb(callback.from_user.id))
    cart_list = await db.cart_confirm(callback.from_user.id)
    user_id = await db.get_admin_user()
    await bot.send_message(user_id,cart_list)
    await db.cart_delete(callback.from_user.id)

@dp.callback_query(F.data == 'order_kozu')
async def confirm_kozu(callback: types.CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Мы приняли ваш заказ. Ожидайте ответа от менеджера', reply_markup=kb.get_start_kb(callback.from_user.id))
    user_id = await db.get_admin_user()
    await bot.send_message(user_id,f'Новый заказ на козу гриль\nАккаунт @{callback.from_user.username}')



@dp.callback_query(kb.CartCallback.filter(F.action == 'confirm'))
async def delete_cart(callback: types.CallbackQuery, callback_data: kb.CartCallback):
    await callback.answer('')
    await callback.message.answer('Вы отменили заказ', reply_markup=kb.get_start_kb(callback.from_user.id))
    await db.cart_delete(callback.from_user.id)
    

#! admin handlers##############################

@dp.callback_query(F.data == 'add_product')
async def create_product(callback: types.CallbackQuery, state:FSMContext):
    await callback.message.answer('Напишите название товара: ')
    await callback.answer()
    await state.set_state(st.ProductState.get_image)
    
@dp.message(st.ProductState.get_image)
async def add_image(message: types.Message, state:FSMContext):
    await message.answer('Отправьте фото товара: ')
    await state.update_data(title = message.text)
    await state.set_state(st.ProductState.get_price)

@dp.message(st.ProductState.get_price)
async def add_price(message: types.Message, state:FSMContext):
    await message.answer('Напишите цену товара: ')
    await state.update_data(image = message.photo[-1].file_id)
    await state.set_state(st.ProductState.get_category)

@dp.message(st.ProductState.get_category)
async def add_category(message: types.Message, state:FSMContext):
    await message.answer('Напишите категорию товара: ')
    await state.update_data(price = int(message.text))
    await state.set_state(st.ProductState.get_finish)


@dp.message(st.ProductState.get_finish)
async def check_product(message: types.Message, state:FSMContext):
    await state.update_data(category = message.text)
    context_data = await state.get_data()
    await message.answer_photo(photo=context_data['image'], caption=f"<b>{context_data['title']}</b>\nЦена {context_data['price']} сом\nКатегория {context_data['category']}", reply_markup=kb.get_create_productkb())
    

@dp.callback_query(F.data == 'save_product')
async def save_product(callback: types.CallbackQuery, state:FSMContext):
    context_data = await state.get_data()
    print(f"\n\n\n\n\n\n{context_data}\n\n\n\n\n")
    await db.category_create_or_get(context_data['category'])
    await db.product_create(context_data)
    await state.clear()
    await callback.message.answer('Продукт создан успешно!!!', reply_markup=kb.get_adminkb())
    await callback.answer()

@dp.message()
async def echo_message(message : types.Message):
    await message.answer('Извините я вас не понимаю. Если хотите что то заказать то нажмите на команду /start') 

async def main():
    await dp.start_polling(bot, skip_updates=True)
    print('Бот вышел в онлайн')
    