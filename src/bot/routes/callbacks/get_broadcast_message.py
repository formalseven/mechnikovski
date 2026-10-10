from bot.states.StateManager import StateManager
from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery

name="get_broadcast_message"

async def exec(bot: AsyncTeleBot, query: CallbackQuery, args):
    type, = args
    await bot.edit_message_text(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        text=f"📤 Надішли повідомлення для розилки:" if type == "msg" else "📤 Надішли текст для Так/Ні опитування:"
    )

    StateManager.set(
        query.from_user.id,
        {
            "action": "send_broadcast_message" if type == "msg" else "send_broadcast_survey",
            "args": ()
        }
    )