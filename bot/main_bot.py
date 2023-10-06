from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, F
from django.conf import settings
from . import bot_keyboards as kb

storage=MemoryStorage()
bot = Bot(token=settings.TOKEN, parse_mode='HTML')
dp = Dispatcher(storage=storage)

@dp.message(F.text == '/start' )
async def command_start(message : types.Message):
    await message.answer("""
✅✅✅ Бул жерден сиз үйүңүзгө же жумушунузга жеткирүү буйуртсаныз болот 🚀🚀🚀
✅✅✅ Здесь вы можете заказать доставку на дом 🏠 🏠🏠 или на работу 👨‍🚒👨‍🚒👨‍🚒

Буйуртма үчүн менюну басыңыз 📌📌📌
Для заказа нажмите меню 📌📌📌
    """, reply_markup=kb.get_start_kb())

@dp.message()
async def echo_message(message : types.Message):
    await message.answer('Извините я вас не понимаю. Если хотите что то заказать то нажмите на команду /start')   


async def main():
    await dp.start_polling(bot)