from telebot import types
from telebot.async_telebot import AsyncTeleBot
from database.Database import Database
import random
from bot.states.surveys import surveys
from bot.states.StateManager import StateManager

name="send_broadcast_survey"

async def exec(bot: AsyncTeleBot, message: types.Message, args):
    users = await Database.query(
        Database.db.table("users").select("name", "id").execute()
    )
    survey_id = random.randint(1, 100000)
    await surveys.set(survey_id, {
        "yes": 0,
        "no": 0
    })
    quest_markup = types.InlineKeyboardMarkup()
    quest_markup.add(
        types.InlineKeyboardButton("🟢 Так", callback_data=f"answer_survey:{survey_id}:yes"),
        types.InlineKeyboardButton("🔴 Ні", callback_data=f"answer_survey:{survey_id}:no")
    )

    count = 0
    for user in users:
        try:
            await bot.copy_message(
                chat_id=user.get("id"),
                from_chat_id=message.chat.id,
                message_id=message.message_id,
                reply_markup=quest_markup
            )
            count += 1
        except Exception as err:
            print(f"Broadcast message wasn't delivered to {user.get('name')}")

    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("📊 Подивитись результати", callback_data=f"survey_results:{survey_id}:{count}")
    )
    markup.row(
        types.InlineKeyboardButton("🧑‍💻 Назад в меню", callback_data="menu")
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"🟢 Ваше опитування було *успішно* надісланий {count}/{len(users)} користувачам",
        reply_markup=markup,
        parse_mode="MarkdownV2"
    )

    StateManager.delete(message.from_user.id)