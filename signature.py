from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings

from db.models import CreateDatabase
from db.requests import UserReq


class BotSettings:
    def __init__(self):
        self.bot = Bot(token=settings.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        self.dp = Dispatcher(storage=MemoryStorage())
        self.db_manager = CreateDatabase(database_url=settings.get_db_url(), echo=False)
        self.db = UserReq(db_session_maker=self.db_manager.get_session)
        