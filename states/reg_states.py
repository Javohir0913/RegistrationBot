from aiogram.fsm.state import State, StatesGroup


class RegisterStates(StatesGroup):
    regName = State()
    regEmail = State()
    regBirth_date = State()
    regPhone = State()
