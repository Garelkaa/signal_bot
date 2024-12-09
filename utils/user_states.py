from aiogram.fsm.state import State, StatesGroup

    
class FSMUserReg(StatesGroup):
    code = State()
