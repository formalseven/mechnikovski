from telebot import types, async_telebot
from database.Database import Database

name = "/menu"

async def exec(bot: async_telebot.AsyncTeleBot, message: types.Message):
    user = (await Database.query(
        Database.db.table("users").select("online_mode", "notify_time").eq(
            "id", message.from_user.id
        ).execute()
    ))[0]

    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton(f"🔄 Змінити режим на {'офлайн' if user.get('online_mode') else 'онлайн'}", callback_data=f"set_bot_mode:{'0' if user.get('online_mode') else '1'}")
    )
    markup.row(
        types.InlineKeyboardButton("⏳ Змінити час попередження", callback_data="change_notify_time")
    )
    await bot.send_message(
        message.chat.id, 
        f"📊 Твое меню:\n\n"
        f"⏰ Режим роботи бота \- *{'онлайн' if user.get('online_mode') else 'офлайн'}*\n"
        f"💼 Сповіщувати за _{user.get('notify_time')}_ хвилин",
        parse_mode="MarkdownV2",
        reply_markup=markup
    )