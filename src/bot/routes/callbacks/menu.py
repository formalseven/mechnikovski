from telebot import types, async_telebot
from database.Database import Database

name = "menu"

async def exec(bot: async_telebot.AsyncTeleBot, query: types.CallbackQuery, args):
    config = (await Database.query(
        Database.db.table("config").select("*").execute()
    ))[0]
    if not query.from_user.id in config.get("admins"):
        await bot.send_message(
            chat_id=query.message.chat.id,
            text=f"🤦 Ви не є адміністратором",
            parse_mode="MarkdownV2"
        )
        return
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("🔔 Надіслати оповіщення", callback_data="send_broadcast")
    )
    markup.row(
        types.InlineKeyboardButton("▶️ Розпочати тест", callback_data="test")
    )
    await bot.edit_message_text(
        chat_id=query.message.chat.id, 
        message_id=query.message.message_id,
        text=f"😎 Вітаю в панелі *адміністратора*\!\n\n"
        f"💼 Адміни \- {', '.join(f'`{admin}`' for admin in config.get('admins'))}",
        parse_mode="MarkdownV2",
        reply_markup=markup
    )