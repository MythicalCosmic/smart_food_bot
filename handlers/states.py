from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    start = State()
    set_language = State()
    menu = State()

class OrderStates(StatesGroup):
    type = State()
    location = State()
    location_confirmation = State()
    items = State()

class BasketStates(StatesGroup):
    basket = State()
    basket_checkout = State()
    basket_confimation = State()
    success = State()