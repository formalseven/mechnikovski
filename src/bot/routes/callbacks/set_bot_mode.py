from database.Database import Database
from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery
from telebot import types

name="set_bot_mode"

async def exec(bot: AsyncTeleBot, query: CallbackQuery, args):
    mode, = args
    user = (await Database.query(
        Database.db.table("users").upsert({ 
            "online_mode": int(mode) == 1,
            "id": query.from_user.id
        }).execute()
    ))[0]
    print(f"User {query.from_user.id} has changed the mode to {'online' if int(mode) == 1 else 'offline'}")

    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton(f"🔄 Змінити режим на {'офлайн' if user.get('online_mode') else 'онлайн'}", callback_data=f"set_bot_mode:{'0' if user.get('online_mode') else '1'}")   
    )
    markup.row(
        types.InlineKeyboardButton("⏳ Змінити час попередження", callback_data="change_notify_time")
    )
    await bot.edit_message_text(
        f"📊 Твое меню:\n\n"
        f"⏰ Режим роботи бота \- *{'онлайн' if user.get('online_mode') else 'офлайн'}*\n"
        f"💼 Сповіщувати за _{user.get('notify_time')}_ хвилин",
        chat_id=query.message.chat.id,
        message_id=query.message.id,
        parse_mode="MarkdownV2",
        reply_markup=markup
    )
    await bot.answer_callback_query(callback_query_id=query.id, text=f"Ви успішно змінили режим на {'онлайновий' if int(mode) == 1 else 'офлайновий'}")