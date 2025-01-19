from aiogram.fsm.state import State, StatesGroup

    
class FSMUserReg(StatesGroup):
    code = State()
    

class FSMAddCodeRefAdmin(StatesGroup):
    code = State()
    select = State()
    

class FSMManageAdmins(StatesGroup):
    add = State()
    delete = State()
    edit = State()
    

class FSMAddOrKickAdmin(StatesGroup):
    uid = State()


class SpamUser(StatesGroup):
    TEXT = State()
