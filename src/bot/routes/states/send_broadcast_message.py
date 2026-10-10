from telebot import types
from telebot.async_telebot import AsyncTeleBot
from database.Database import Database
from bot.states.StateManager import StateManager

name="send_broadcast_message"

async def exec(bot: AsyncTeleBot, message: types.Message, args):
    users = await Database.query(
        Database.db.table("users").select("name", "id").execute()
    )

    count = 0
    for user in users:
        try:
            await bot.copy_message(
                chat_id=user.get("id"),
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
            count += 1
        except Exception as err:
            print(f"Broadcast message wasn't delivered to {user.get('name')}")

    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("🧑‍💻 Назад в меню", callback_data="menu")
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"🟢 Ваше повідомлення було *успішно* надіслано {count}/{len(users)} користувачам",
        reply_markup=markup,
        parse_mode="MarkdownV2"
    )

    StateManager.delete(message.from_user.id)