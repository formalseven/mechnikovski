from telebot import types, async_telebot
from bot.states.StateManager import StateManager

name="/test"

async def exec(bot: async_telebot.AsyncTeleBot, message: types.Message):
    await bot.send_message(message.chat.id, "🔐 Введіть пароль для доступу до панелі тестування:")

    StateManager.set(message.from_user.id, {
        "action": "check_admin_pass",
        "args": []
    })