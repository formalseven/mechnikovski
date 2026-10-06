from database.Database import Database
from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery

name="set_group"

async def exec(bot: AsyncTeleBot, query: CallbackQuery, args):
    group, = args
    print(group)
    await Database.query(
        Database.db.table("users").upsert({ 
            "id": query.from_user.id,
            "name": query.from_user.first_name,
            "group": group
        }).execute()
    )
    print(f"User {query.from_user.id} has chosen {group} group")
    await bot.edit_message_text(
        f"✅ Тебе зареєстровано як студента *{group}\-ї групи*\.\n"
        f"Щоб змінити групу, знову напиши \/start\.",
        chat_id=query.message.chat.id,
        message_id=query.message.id,
        parse_mode="MarkdownV2"
    )
    