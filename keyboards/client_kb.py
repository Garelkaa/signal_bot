from aiogram.utils.keyboard import InlineKeyboardBuilder

class ReplyKb:
    @staticmethod
    async def accept(casino_link):
        buttons = [
            ("Регистрация 🔗", casino_link),
        ]

        builder = InlineKeyboardBuilder()
        for text, url in buttons:
            builder.button(text=text, url=url)
        
        builder.button(text="Я зарегистрировался ✅", callback_data="acknowledge_instructions")

        return builder.adjust(1).as_markup()

    @staticmethod
    async def registration():
        builder = InlineKeyboardBuilder()
        builder.button(text="Я ознакомился ✅", callback_data="acknowledge_registration")
        return builder.adjust(1).as_markup()

    @staticmethod
    async def main_menu(web_app_url: str, casino_link: str):
        buttons = [
            ("📖 Инструкция", "instruction"),
        ]

        builder = InlineKeyboardBuilder()

        # Add standard buttons
        for text, callback_data in buttons:
            builder.button(text=text, callback_data=callback_data)
        
        builder.button(text="Регистрация 🔗", url=f"{casino_link}")

        # Add the web app button
        builder.button(
            text="🌟 ПОЛУЧИТЬ СИГНАЛ 🌟", web_app={"url": web_app_url}
        )

        return builder.adjust(2).as_markup()

    @staticmethod
    async def subscription(required_channel: str):
        builder = InlineKeyboardBuilder()
        builder.button(
            text="Подписаться на канал",
            url=f"https://t.me/{required_channel.lstrip('@')}"
        )
        builder.button(
            text="Проверить подписку",
            callback_data="check_subscription"
        )
        return builder.adjust(1).as_markup()
