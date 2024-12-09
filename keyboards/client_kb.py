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
