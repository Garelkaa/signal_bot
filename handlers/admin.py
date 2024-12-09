import asyncio
from signature import BotSettings
from aiogram import F, types
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types.input_file import FSInputFile
from keyboards.admin_kb import AdminReplyKb as kb

class Admin:
    def __init__(self, bot: BotSettings):
        self.bot = bot.bot
        self.dp = bot.dp
        self.db = bot.db

    async def register_handlers(self):
        self.dp.message(F.text == "/adm")(self.adm_panel)
        self.dp.callback_query(F.data == "stats")(self.show_stats)
        self.dp.callback_query(F.data == "spam")(self.start_spam)
        self.dp.callback_query(F.data == "export_user")(self.export_users)

    async def adm_panel(self, m: types.Message):
        if await self.db.get_user_status(m.from_user.id):
            await m.answer("⚙️ Панель администратора", reply_markup=await kb.admin_panel())
        else: 
            await m.answer("У вас недостаточно прав!")

    async def show_stats(self, cq: types.CallbackQuery):
        user_count = await self.db.get_user_count()
        await cq.message.answer(f"📊 Статистика:\n\n👥 Количество пользователей: {user_count}")
        await cq.answer()

    async def start_spam(self, cq: types.CallbackQuery):
        await cq.message.answer("📢 Введите текст для рассылки.")
        self.dp.message(F.text)(self.send_spam)
        await cq.answer()

    async def send_spam(self, m: types.Message):
        spam_text = m.text
        users = await self.db.get_all_users()
        success, failed = 0, 0

        for user in users:
            try:
                await self.bot.send_message(chat_id=user["uid"], text=spam_text)
                success += 1
            except TelegramRetryAfter as e:
                await asyncio.sleep(e.retry_after)
            except Exception:
                failed += 1

        await m.answer(f"✅ Рассылка завершена:\nУспешно: {success}\nОшибки: {failed}")

    async def export_users(self, cq: types.CallbackQuery):
        users = await self.db.get_all_users()
        file_content = "Список пользователей:\n\n"
        for user in users:
            file_content += f"ID: {user['uid']}, Username: {user['uname']}\n"

        file_path = "/tmp/export_users.txt"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(file_content)

        input_file = FSInputFile(path=file_path)
        await cq.message.answer_document(document=input_file)
        await cq.answer()
