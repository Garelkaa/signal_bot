from signature import BotSettings
from aiogram import F, types

class Admin:
    def __init__(self, bot: BotSettings):
        self.bot = bot.bot
        self.dp = bot.dp
        self.db = bot.db
        
    async def register_handlers(self):
        self.dp.message(F.text == "/start")(self.start_handler)
        
    async def start_handler(self, m: types.Message, *args, **kwargs):
        print(args)
        await m.answer("Привет!")