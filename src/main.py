from notifications.main import start_notifications
from bot.main import start_bot
import asyncio

async def start():
    await start_bot(start_notifications)

asyncio.run(start())