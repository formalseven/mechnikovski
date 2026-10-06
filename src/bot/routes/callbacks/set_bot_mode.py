from database.Database import Database
from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery
from telebot import types

name="set_bot_mode"

async def exec(bot: AsyncTeleBot, query: CallbackQuery, args):
    mode, = args
    await Database.query(
        Database.db.table("config").upsert({ 
            "online_mode": int(mode) == 1,
            "id": 1
        }).execute()
    )
    print(f"User {query.from_user.id} has changed the mode to {'online' if int(mode) == 1 else 'offline'}")

    config = (await Database.query(
        Database.db.table("config").select("*").execute()
    ))[0]
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton(f"Змінити режим на {'офлайн' if config.get('online_mode') else 'онлайн'}", callback_data=f"set_bot_mode:{'0' if config.get('online_mode') else '1'}")   
    )
    markup.row(
        types.InlineKeyboardButton("Розпочати тест", callback_data="test")
    )
    await bot.edit_message_text(
        f"😎 Вітаю в панелі *адміністратора*\!\n\n"
        f"⏰ Режим роботи \- *{'онлайн' if config.get('online_mode') else 'офлайн'}*\n"
        f"💼 Адміни \- {', '.join(f'`{admin}`' for admin in config.get('admins'))}",
        chat_id=query.message.chat.id,
        message_id=query.message.id,
        parse_mode="MarkdownV2",
        reply_markup=markup
    )
    await bot.answer_callback_query(callback_query_id=query.id, text=f"Ви успішно змінили режим на {'онлайновий' if int(mode) == 1 else 'офлайновий'}")
    