from aiogram import F, types

from signature import BotSettings

from keyboards.client_kb import ReplyKb as kb

class Client:
    def __init__(self, bot: BotSettings):
        self.bot = bot.bot
        self.dp = bot.dp
        self.db = bot.db

    async def register_handlers(self):
        self.dp.message(F.text.startswith("/start"))(self.start_handler)
        self.dp.callback_query(F.data == "acknowledge_instructions")(self.acknowledge_instructions_handler)

    async def start_handler(self, m: types.Message):
        user_exists = await self.db.user_exists(m.from_user.id)
        
        if user_exists:
            await m.answer(
                "👋 Добро пожаловать в SIGNAL BOT MINES!\n\n"
                "🎮 Mines — это азартная игра в 1win, основанная на классическом «Сапёре».\n"
                "✨ Цель игры — открывать безопасные ячейки, избегая ловушек.\n\n"
                "🤖 Наш бот, работающий на нейросети, способен предсказывать расположение звёзд с точностью до 92%.\n\n"
                "📊 Используйте меню для навигации и получения сигналов!"
            )
            return

        command_parts = m.text.split(maxsplit=1)
        if len(command_parts) == 1:
            await m.answer("❗️ Регистрация возможна только по ссылке, выданной администратором.")
        else:
            code = await self.db.get_ref_code(command_parts[1])
            if code:
                instructions = (
                    "👋 Добро пожаловать в SIGNAL BOT MINES!\n\n"
                    "📌 Основная информация:\n"
                    "Бот предоставляет сигналы на основе вашего ID, депозита и суммы ставки. "
                    "Алгоритм прогнозирования построен на основе нейросети.\n\n"
                    "📖 Инструкция:\n"
                    "1️⃣ Если вы уже сделали первую ставку без бота, пополните баланс на ту же сумму "
                    "и сделайте ставку по прогнозу бота.\n"
                    "2️⃣ Если вы проиграли хотя бы две первые ставки, пополните баланс на ту же сумму и обновите бота.\n\n"
                    "После выполнения этих шагов переходите к следующему этапу!"
                )
                await m.answer(instructions, reply_markup=await kb.accept())
            else:
                await m.answer("⛔️ Неверная или недействительная ссылка для регистрации.")

    async def acknowledge_instructions_handler(self, cq: types.CallbackQuery):
        user_exists = await self.db.user_exists(cq.from_user.id)
        
        if user_exists:
            await cq.message.delete()
            await cq.message.answer(
                "👋 Добро пожаловать в SIGNAL BOT MINES!\n\n"
                "🎮 Mines — это азартная игра в 1win, основанная на классическом «Сапёре».\n"
                "✨ Цель игры — открывать безопасные ячейки, избегая ловушек.\n\n"
                "🤖 Наш бот, работающий на нейросети, способен предсказывать расположение звёзд с точностью до 92%.\n\n"
                "📊 Используйте меню для навигации и получения сигналов!"
            )
            await cq.answer()
            return
        
        await self.db.add_user(
            uid=cq.from_user.id,
            uname=cq.from_user.username if cq.from_user.username else cq.from_user.first_name
        )
        await cq.message.delete()
        await cq.message.answer(
            "🎉 Вы успешно зарегистрированы в SIGNAL BOT MINES!\n\n"
            "🎮 Mines — это азартная игра в 1win, основанная на классическом «Сапёре».\n"
            "✨ Цель игры — открывать безопасные ячейки, избегая ловушек.\n\n"
            "🤖 Наш бот, работающий на нейросети, способен предсказывать расположение звёзд с точностью до 92%.\n\n"
            "📊 Используйте меню для навигации и получения сигналов!"
        )
        await cq.answer()
