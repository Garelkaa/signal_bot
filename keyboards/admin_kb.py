from aiogram.utils.keyboard import InlineKeyboardBuilder

class AdminReplyKb:
    @staticmethod
    async def admin_panel():
        buttons = [
            # ("📊 Статистика", "stats"),
            ("📢 Рассылка", "spam"),
            ("🔗 Реферальные ссылки", "ref_link"),
            ("👥 Управление администраторами", "manage_admins"),
            ("📂 Выгрузка пользователей", "export_user"),
        ]

        builder = InlineKeyboardBuilder()
        
        for text, callback_data in buttons:
            builder.button(text=text, callback_data=callback_data)

        return builder.adjust(1).as_markup()

    @staticmethod
    async def ref_panel():
        buttons = [
            ("Ссылка для бота", "bot_link"),
            ("Ссылка для казино", "casino_link"),

        ]

        builder = InlineKeyboardBuilder()
        
        for text, callback_data in buttons:
            builder.button(text=text, callback_data=callback_data)

        return builder.adjust(1).as_markup()
    
    @staticmethod
    async def add_link_keyboard(ref_type: str):
        buttons = [
            ("➕ Добавить ссылку", f"add_link:{ref_type}"),
            ("🗑 Удалить ссылку", f"delete_link:{ref_type}")
        ]

        builder = InlineKeyboardBuilder()
        
        for text, callback_data in buttons:
            builder.button(text=text, callback_data=callback_data)

        return builder.adjust(1).as_markup()
    
    @staticmethod
    async def manage_admins_keyboard():
        buttons = [
            ("➕ Добавить администратора", "add_admin"),
            ("🗑 Удалить администратора", "delete_admin"),
            ("🔙 Назад", "admin_panel")
        ]

        builder = InlineKeyboardBuilder()
        
        for text, callback_data in buttons:
            builder.button(text=text, callback_data=callback_data)

        return builder.adjust(1).as_markup()
