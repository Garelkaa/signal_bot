from aiogram.fsm.state import State, StatesGroup

    
class FSMUserReg(StatesGroup):
    code = State()
    
class FSMAddCodeRefAdmin(StatesGroup):
    code = State()
    
class FSMAddOrKickAdmin(StatesGroup):
    uid = State()
