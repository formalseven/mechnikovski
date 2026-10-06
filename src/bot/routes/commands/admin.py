from telebot import types, async_telebot
from database.Database import Database

name = "/admin"

async def exec(bot: async_telebot.AsyncTeleBot, message: types.Message):
    config = (await Database.query(
        Database.db.table("config").select("*").execute()
    ))[0]
    if not message.from_user.id in config.get("admins"):
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"🤦 Ви не є адміністратором",
            parse_mode="MarkdownV2"
        )
        return
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton(f"Змінити режим на {'офлайн' if config.get('online_mode') else 'онлайн'}", callback_data=f"set_bot_mode:{'0' if config.get('online_mode') else '1'}")
    )
    markup.row(
        types.InlineKeyboardButton("Розпочати тест", callback_data="test")
    )
    await bot.send_message(
        message.chat.id, 
        f"😎 Вітаю в панелі *адміністратора*\!\n\n"
        f"⏰ Режим роботи \- *{'онлайн' if config.get('online_mode') else 'офлайн'}*\n"
        f"💼 Адміни \- {', '.join(f'`{admin}`' for admin in config.get('admins'))}",
        parse_mode="MarkdownV2",
        reply_markup=markup
    )