from aiogram.fsm.state import State, StatesGroup


class VoiceStates(StatesGroup):
    get_name = State()
