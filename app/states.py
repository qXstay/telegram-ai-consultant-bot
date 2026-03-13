from aiogram.fsm.state import State, StatesGroup


class LeadForm(StatesGroup):
    name = State()
    contact = State()
    task = State()
    comment = State()
