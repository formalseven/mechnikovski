from telebot.async_telebot import AsyncTeleBot
from dotenv import dotenv_values
import os
from bot.Router import route
import asyncio
from database.Database import Database

config = {
    **dotenv_values(),
    **os.environ
}

if not config.get("BOT_TOKEN"):
    raise Exception("BOT_TOKEN wasn't loaded!")

async def start_bot(start_notifications):
    try:
        await Database.init()
        bot = AsyncTeleBot(config.get("BOT_TOKEN"))
        route(bot)
        asyncio.create_task(start_notifications(bot))
        print("Info | Bot has started successfully")
        await bot.infinity_polling()
    except Exception as err:
        print(err)
    