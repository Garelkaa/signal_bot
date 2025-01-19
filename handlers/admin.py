import asyncio
from aiogram import F, types
from aiogram.exceptions import TelegramRetryAfter
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from keyboards.admin_kb import AdminReplyKb as kb
from utils.user_states import FSMAddCodeRefAdmin, FSMManageAdmins
from signature import BotSettings

from utils.user_states import SpamUser


class Admin:
    def __init__(self, bot: BotSettings):
        self.bot = bot.bot
        self.dp = bot.dp
        self.db = bot.db

    async def register_handlers(self):
        self.dp.message(F.text == "/adm")(self.adm_panel)
        self.dp.callback_query(F.data == "stats")(self.show_stats)
        self.dp.callback_query(F.data == "spam")(self.start_spam)
        self.dp.message(SpamUser.TEXT)(self.send_spam)
        self.dp.callback_query(F.data == "export_user")(self.export_users)
        self.dp.callback_query(F.data == "ref_link")(self.panel_ref)
        self.dp.callback_query(F.data == "bot_link")(self.bot_ref_link)
        self.dp.callback_query(F.data == "casino_link")(self.casino_ref_link)
        self.dp.callback_query(F.data.startswith("add_link:"))(self.add_link_start)
        self.dp.message(FSMAddCodeRefAdmin.code)(self.save_new_link)
        self.dp.callback_query(F.data.startswith("delete_link:"))(self.delete_link_start)
        self.dp.message(FSMAddCodeRefAdmin.select)(self.delete_link)
        self.dp.callback_query(F.data == "manage_admins")(self.show_admins_panel)
        self.dp.callback_query(F.data == "add_admin")(self.start_add_admin)
        self.dp.message(FSMManageAdmins.add)(self.add_admin)
        self.dp.callback_query(F.data == "delete_admin")(self.start_delete_admin)
        self.dp.message(FSMManageAdmins.delete)(self.delete_admin)


    async def adm_panel(self, m: types.Message):
        if await self.db.get_user_status(m.from_user.id):
            await m.answer("⚙️ Панель администратора", reply_markup=await kb.admin_panel())
        else:
            await m.answer("У вас недостаточно прав!")


    async def show_stats(self, cq: types.CallbackQuery):
        user_count = await self.db.get_user_count()
        await cq.message.answer(f"📊 Статистика:\n\n👥 Количество пользователей: {user_count}")
        await cq.answer()


    async def start_spam(self, cq: types.CallbackQuery, state: FSMContext):
        await cq.message.answer("📢 Введите текст для рассылки.")
        await state.set_state(SpamUser.TEXT)


    async def send_spam(self, m: types.Message, state: FSMContext):
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
        await state.clear()


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


    async def panel_ref(self, call: types.CallbackQuery):
        await call.message.answer("Выберите тип реферальной ссылки.", reply_markup=await kb.ref_panel())


    async def bot_ref_link(self, call: types.CallbackQuery):
        bot_links = await self.db.get_referer_links("bot")
        if not bot_links:
            await call.message.answer(
                "⚠️ Бот-ссылки отсутствуют.",
                reply_markup=await kb.add_link_keyboard("bot")
            )
            await call.answer()
            return

        message = "🔗 <b>Ссылки на бота:</b>\n\n"
        for ref in bot_links:
            message += f"• {ref['name']} — Количество людей: {ref['count_people']}\n"

        await call.message.answer(
            message,
            parse_mode="HTML",
            reply_markup=await kb.add_link_keyboard("bot")
        )
        await call.answer()


    async def casino_ref_link(self, call: types.CallbackQuery):
        casino_links = await self.db.get_referer_links("casino")
        if not casino_links:
            await call.message.answer(
                "⚠️ Казино-ссылки отсутствуют.",
                reply_markup=await kb.add_link_keyboard("casino")
            )
            await call.answer()
            return

        message = "🎰 <b>Ссылки на казино:</b>\n\n"
        for ref in casino_links:
            message += f"• {ref['name']} — Количество людей: {ref['count_people']}\n"

        await call.message.answer(
            message,
            parse_mode="HTML",
            reply_markup=await kb.add_link_keyboard("casino"))
        await call.answer()


    async def add_link_start(self, call: types.CallbackQuery, state: FSMContext):
        ref_type = call.data.split(":")[1]
        await state.update_data(ref_type=ref_type)
        await state.set_state(FSMAddCodeRefAdmin.code)
        await call.message.answer(f"Введите название новой ссылки для типа '{ref_type}':")
        await call.answer()


    async def save_new_link(self, m: types.Message, state: FSMContext):
        data = await state.get_data()
        ref_type = data.get("ref_type")
        link_name = m.text

        await self.db.add_referer_link(link_name, ref_type)
        await m.answer(f"✅ Ссылка '{link_name}' успешно добавлена для типа '{ref_type}'.")
        await state.clear()


    async def delete_link_start(self, call: types.CallbackQuery, state: FSMContext):
        ref_type = call.data.split(":")[1]
        await state.update_data(ref_type=ref_type)

        links = await self.db.get_referer_links(ref_type)
        if not links:
            await call.message.answer("⚠️ Нет доступных ссылок для удаления.")
            await call.answer()
            return

        message = "🗑 <b>Доступные ссылки для удаления:</b>\n\n"
        for ref in links:
            message += f"• {ref['name']}\n"

        await state.set_state(FSMAddCodeRefAdmin.select)
        await call.message.answer(
            f"{message}\nВведите название ссылки, которую нужно удалить:",
            parse_mode="HTML"
        )
        await call.answer()


    async def delete_link(self, m: types.Message, state: FSMContext):
        data = await state.get_data()
        ref_type = data.get("ref_type")
        link_name = m.text.strip()

        success = await self.db.delete_referer_link(link_name, ref_type)
        if success:
            await m.answer(f"✅ Ссылка '{link_name}' успешно удалена.")
        else:
            await m.answer(f"⚠️ Не удалось найти ссылку '{link_name}' для типа '{ref_type}'.")
        await state.clear()

    async def show_admins_panel(self, call: types.CallbackQuery):
        message = "👥 Управление администраторами\n"
        admins = await self.db.get_all_admins()
        if not admins:
            message += '"⚠️ Администраторы отсутствуют."'
            await call.message.answer(message, reply_markup=await kb.manage_admins_keyboard())
            return
            
        for admin in admins:
            message += f"• {admin['id']} — @{admin['username']}\n"
        
        await call.message.answer(message, reply_markup=await kb.manage_admins_keyboard())
        
        await call.answer()

    async def start_add_admin(self, call: types.CallbackQuery, state: FSMContext):
        await state.set_state(FSMManageAdmins.add)
        await call.message.answer("Введите ID нового администратора:")
        await call.answer()

    async def add_admin(self, m: types.Message, state: FSMContext):
        admin_id = m.text.strip()
        success = await self.db.add_admin(int(admin_id))
        if success:
            await m.answer(f"✅ Администратор с ID {admin_id} успешно добавлен.")
        else:
            await m.answer(f"⚠️ Не удалось добавить администратора с ID {admin_id}. Возможно, он уже существует.")
        await state.clear()

    async def start_delete_admin(self, call: types.CallbackQuery, state: FSMContext):
        admins = await self.db.get_all_admins()
        if not admins:
            await call.message.answer("⚠️ Администраторы отсутствуют.")
            await call.answer()
            return

        message = "🗑 <b>Список администраторов для удаления:</b>\n\n"
        for admin in admins:
            message += f"• {admin['id']} — @{admin['username']}\n"

        await state.set_state(FSMManageAdmins.delete)
        await call.message.answer(
            f"{message}\nВведите ID администратора, которого нужно удалить:",
            parse_mode="HTML"
        )
        await call.answer()

    async def delete_admin(self, m: types.Message, state: FSMContext):
        admin_id = m.text.strip()
        success = await self.db.delete_admin(int(admin_id))
        if success:
            await m.answer(f"✅ Администратор с ID {admin_id} успешно удалён.")
        else:
            await m.answer(f"⚠️ Не удалось найти администратора с ID {admin_id}.")
        await state.clear()
