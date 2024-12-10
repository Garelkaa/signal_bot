from aiogram.utils.keyboard import InlineKeyboardBuilder


class ReplyKb:
    @staticmethod
    async def accept():
        buttons = [
            ("Ознакомлен ✅", "acknowledge_instructions")
        ]

        builder = InlineKeyboardBuilder()
        
        for text, callback_data in buttons:
            builder.button(text=text, callback_data=callback_data)

        return builder.adjust(1).as_markup()
    
    
    @staticmethod
    async def registration(casino_link):
        buttons = [
            ("Регистрация 🔗", f"{casino_link}"),
        ]

        builder = InlineKeyboardBuilder()
        
        for text, data in buttons:
            builder.button(text=text, url=data)
        
        builder.button(text="Я зарегистрировался ✅", callback_data="acknowledge_registration")

        return builder.adjust(1).as_markup()