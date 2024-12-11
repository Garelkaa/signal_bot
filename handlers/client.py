from aiogram import F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from signature import BotSettings
from keyboards.client_kb import ReplyKb as kb

REQUIRED_CHANNEL = "@bbytestsignalbot"  # Замените на имя вашего канала

class Client:
    def __init__(self, bot: BotSettings):
        self.bot = bot.bot
        self.dp = bot.dp
        self.db = bot.db

    async def register_handlers(self):
        self.dp.message(F.text.startswith("/start"))(self.start_handler)
        self.dp.callback_query(F.data == "acknowledge_registration")(self.confirm_registration_handler)
        self.dp.callback_query(F.data == "acknowledge_instructions")(self.acknowledge_instructions_handler)
        self.dp.callback_query(F.data == "check_subscription")(self.check_subscription_handler)
        self.dp.callback_query(F.data == "instruction")(self.instruction)

    async def check_subscription(self, user_id):
        try:
            member = await self.bot.get_chat_member(REQUIRED_CHANNEL, user_id)
            return member.status in ("member", "administrator", "creator")
        except Exception:
            return False

    async def ask_for_subscription(self, message):
        await message.answer(
            "❗️Для использования бота необходимо подписаться на наш канал.",
            reply_markup=await kb.subscription(REQUIRED_CHANNEL)
        )

    async def start_handler(self, m: types.Message):
        is_subscribed = await self.check_subscription(m.from_user.id)
        random_casino_link = await self.db.get_random_casino_link()

        if not is_subscribed:
            await self.ask_for_subscription(m)
            return

        user_exists = await self.db.user_exists(m.from_user.id)

        if user_exists:
            await m.answer(
                "👋 Добро пожаловать в SIGNAL BOT MINES!\n\n"
                "🎮 Mines — это азартная игра в 1win, основанная на классическом «Сапёре».\n"
                "✨ Цель игры — открывать безопасные ячейки, избегая ловушек.\n\n"
                "🤖 Наш бот, работающий на нейросети, способен предсказывать расположение звёзд с точностью до 92%.\n\n"
                "📊 Используйте меню для навигации и получения сигналов!",
                reply_markup=await kb.main_menu("https://rad-seahorse-749aaa.netlify.app/", f"{random_casino_link}")
            )
            return

        command_parts = m.text.split(maxsplit=1)
        ref_code = None

        if len(command_parts) > 1:
            ref_code = await self.db.get_ref_code("t.me/onewintestbot?start=" + command_parts[1])

        instructions = (
            "❕1. Зарегистрируйтесь в букмекерской конторе 1WIN\n"
            "Если не открывается воспользуйтесь любым бесплатным ВПН сервисом, к примеру: Planet VPN, Vpnify, FREE VPN fast. Регион - Швеция)\n"
            "- ❗️Введите промокод - Florin12 - он даст +500% к депозиту❗️\n"
            "\n"
            "-❗️Без регистрации и промокода доступ к использованию бота будет закрыт❗️\n"
            "\n"
            "❕2. Если у вас уже есть аккаунт 1WIN обязательно выйдите с него и создайте новый, иначе бот выдаст вам не верный сигнал. \n"
            "Так как выдача сигнала происходит с помощью идентификации вашего ID аккаунта 1WIN, суммы ставки, общего депозита \n"
            "(суммы которую вы закинули на аккаунт), и количества Мин\n"
            "\n"
            "❕3. Пополните ваш баланс (запомните сумму, она вам пригодится)\n"
            "❕4. Перейдите в раздел игр 1WIN и выберите игру «mines»\n"
            "❕5. Установите количество ловушек (запомните это число, оно пригодится вам для использования бота!)\n"
            "❕6. Зайдите в нашего бота и выберете пункт «Получить сигнал». Дальше выставите снизу такие параметры как: Ваш ID аккаунта \n"
            "(он находится в правом верхнем углу), сумма депозита, сумма ставки, количество мин\n"
            "\n"
            "❕7. В случае если бот ошибся и выдал неправильный сигнал советуем удвоить ставку\n"
            "Желаем всем удачи и ждём отзывов о работе бота!"
        )

        await m.answer(
            "Добро пожаловать!\n\n"
            "1️⃣ Нажмите на кнопку ниже, чтобы зарегистрироваться на сайте.\n"
            "2️⃣ После регистрации подтвердите её в боте.\n\n" + instructions,
            reply_markup=await kb.registration()
        )

    async def confirm_registration_handler(self, cq: types.CallbackQuery):
        is_subscribed = await self.check_subscription(cq.from_user.id)

        if not is_subscribed:
            await cq.message.delete()
            await self.ask_for_subscription(cq.message)
            return

        user_exists = await self.db.user_exists(cq.from_user.id)
        random_casino_link = await self.db.get_random_casino_link()

        if not user_exists:
            await self.db.add_user(
                uid=cq.from_user.id,
                uname=cq.from_user.username if cq.from_user.username else cq.from_user.first_name
            )

        instructions = (
            "❕1. Зарегистрируйтесь в букмекерской конторе 1WIN (ссылка снизу 👇)\n"
            "Если не открывается воспользуйтесь любым бесплатным ВПН сервисом, к примеру: Planet VPN, Vpnify, FREE VPN fast. Регион - Швеция\n"
            "- ❗️Введите промокод - Florin12 - он даст +500% к депозиту❗️\n"
            "\n"
            "-❗️Без регистрации и промокода доступ к использованию бота будет закрыт❗️\n"
            "❕2. Дальше перейдите в раздел «Инструкция» и следуйте по всем остальным пунктам"
        )

        await cq.message.delete()
        await cq.message.answer(instructions, reply_markup=await kb.accept(random_casino_link))
        await cq.answer()

    async def acknowledge_instructions_handler(self, cq: types.CallbackQuery):
        is_subscribed = await self.check_subscription(cq.from_user.id)
        random_casino_link = await self.db.get_random_casino_link()

        if not is_subscribed:
            await cq.message.delete()
            await self.ask_for_subscription(cq.message)
            return

        await cq.message.delete()
        await cq.message.answer(
            "🎉 Вы успешно завершили регистрацию и готовы использовать бот!\n\n"
            "🎮 Mines — это азартная игра в 1win, основанная на классическом «Сапёре».\n"
            "✨ Цель игры — открывать безопасные ячейки, избегая ловушек.\n\n"
            "🤖 Наш бот, работающий на нейросети, способен предсказывать расположение звёзд с точностью до 92%.\n\n"
            "📊 Используйте меню для навигации и получения сигналов!",
            reply_markup=await kb.main_menu("https://rad-seahorse-749aaa.netlify.app/", f"{random_casino_link}")
        )
        await cq.answer()
        
    async def instruction(self, cq: types.CallbackQuery):
        is_subscribed = await self.check_subscription(cq.from_user.id)

        if not is_subscribed:
            await cq.message.delete()
            await self.ask_for_subscription(cq.message)
            return

        await cq.message.answer(
            """❕1. Зарегистрируйтесь в букмекерской конторе 1WIN 
Если не открывается воспользуйтесь любым бесплатным ВПН сервисом, к примеру: Planet VPN, Vpnify, FREE VPN fast. Регион - Швеция)
- ❗️Введите промокод - Florin12 - он даст +500% к депозиту❗️

-❗️Без регистрации и промокода доступ к использованию бота будет закрыт❗️

❕2. Если у вас уже есть аккаунт 1WIN обязательно выйдите с него и создайте новый, иначе бот выдаст вам не верный сигнал. Так как выдача сигнала происходит с помощью идентификации вашего ID аккаунта 1WIN, суммы ставки, общего депозита (суммы которую вы закинули на аккаунт), и количества Мин

❕3. Пополните ваш баланс (запомните сумму, она вам пригодится)

❕4. Перейдите в раздел игр 1WIN и выберите игру «mines»

❕5. Установите количество ловушек (запомните это число, оно пригодиться вам для использования бота!)

❕6. Зайдите в нашего бота и выберете пунк «Получить сигнал». Дальше выставите снизу такие параметры как: Ваш ID аккаунта (он находиться в правом верхнем углу), сумма депозита, сумма ставки, кол-во мин

❕7. В случае если бот ошибся и выдал неправильный сигнал советуем удвоить ставку
Желаем всем удачи и ждём отзывов о работе бота!"""
        )
        await cq.answer()

    async def check_subscription_handler(self, cq: types.CallbackQuery):
        is_subscribed = await self.check_subscription(cq.from_user.id)

        if is_subscribed:
            await cq.message.answer("✅ Вы успешно подписаны на канал и можете продолжить использование бота! Введите еще раз <code>/start</code>")
        else:
            await cq.message.answer("❌ Вы не подписаны на канал. Подпишитесь для использования бота.")
