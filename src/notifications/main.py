from . import notify
from dotenv import dotenv_values
import os
from telebot.async_telebot import AsyncTeleBot

config = {
    **dotenv_values(),
    **os.environ
}

async def start_notifications(bot: AsyncTeleBot):
    await notify.notify(bot)