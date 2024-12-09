from aiogram.utils.keyboard import InlineKeyboardBuilder

class AdminReplyKb:
    @staticmethod
    async def admin_panel():
        buttons = [
            ("📊 Статистика", "stats"),
            ("📢 Рассылка", "spam"),
            ("🔗 Реферальные ссылки", "ref_link"),
            ("📂 Выгрузка пользователей", "export_user"),
        ]

        builder = InlineKeyboardBuilder()
        
        for text, callback_data in buttons:
            builder.button(text=text, callback_data=callback_data)

        return builder.adjust(1).as_markup()
