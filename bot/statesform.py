from aiogram.fsm.state import StatesGroup, State

class ProductState(StatesGroup):
    get_title = State()
    get_price = State()
    get_category = State()
    get_image = State()
    get_finish = State()