from telebot import types
from telebot.async_telebot import AsyncTeleBot
from database.Database import Database
from bot.states.StateManager import StateManager

name="change_notify_time"

async def exec(bot: AsyncTeleBot, message: types.Message, args):
    time = message.text

    if not time.isdigit():
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Ну а можна нормальне число ввести, та й не морочити мені голову⁉️",
            reply_to_message_id=message.message_id
        )
        return

    time = int(time)

    if time > 30:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Ти шо❓ Хочеш згадати, а потім знову забути❓ А ну давай нормальне число уводь❗️",
            reply_to_message_id=message.message_id
        )
        return

    await Database.query(
        Database.db.table("users").upsert({ 
            "notify_time": time,
            "id": message.from_user.id
        }).execute()
    )
    
    await bot.send_message(
        message.chat.id,
        f"🫡 Окей, тепер буду попереджати тебе за _{time}_ хвилин\n"
        f"Якщо хочеш знову потрапити в *панель керування* відправ \- \/menu",
        parse_mode="MarkdownV2"
    )

    StateManager.delete(message.from_user.id)