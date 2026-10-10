from bot.states.StateManager import StateManager
from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery

name="change_notify_time"

async def exec(bot: AsyncTeleBot, query: CallbackQuery, args):
    await bot.edit_message_text(
        chat_id=query.message.chat.id,
        text=f"💬 Введіть за скільки *хвилин* до заняття вас попереджати:",
        message_id=query.message.message_id,
        parse_mode="MarkdownV2"
    )

    StateManager.set(
        user_id=query.from_user.id, 
        data={
            "action": "change_notify_time",
            "args": []
    })