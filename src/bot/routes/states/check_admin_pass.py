from telebot import types, async_telebot
from dotenv import dotenv_values
import os
from database.Database import Database
import datetime
from utils.get_current_week import get_current_week
from bot.states.StateManager import StateManager
from zoneinfo import ZoneInfo
TZ = ZoneInfo("Europe/Kyiv") 

config = {
    **dotenv_values(),
    **os.environ
}

DAYS_NAMES = (
    "Понеділок", 
    "Вівторок", 
    "Середа", 
    "Четвер",
    "П'ятниця", 
    "Субота", 
    "Неділя"
)

name="check_admin_pass"

async def exec(bot: async_telebot.AsyncTeleBot, message: types.Message):
    if config.get("SECRET_PASS") != message.text:
        await bot.send_message(
            message.chat.id,
            "❌ Невірний пароль. Доступ відхилено.",
            reply_to_message_id=message.id
        )
        StateManager.delete(message.from_user.id)
        return

    users = await Database.query(
        Database.db.table("users").select("group", "id").execute()
    )

    g1 = sum(1 for g in users if g["group"] == 1)
    g2 = sum(1 for g in users if g["group"] == 2)

    now = datetime.datetime.now()
    test_start = (now + datetime.timedelta(minutes=1)).strftime("%H:%M")
    #Add test notification
    for user in users:
        await bot.send_message(chat_id=user.get("id"), text=(
            f"⏰ *Нагадування\! Через 10 хвилин пара\!*\n\n"
            f"📘 *Предмет:* Тест\n"
            f"🕒 *Початок о:* {test_start}\n"
            f"🔗 *Посилання:* [Приєднатися](https://zoom.us)"
        ),
        parse_mode="MarkdownV2",
        disable_web_page_preview=True)
    week = get_current_week(now.date(TZ))

    status_text = (
        "📊 *ЗВІТ ПРО СТАН СИСТЕМИ*\n"
        "━━━━━━━━━━━━━━━\n"
        f"👥 *Підписників:* `{len(users)}` \(Група 1: `{g1}`, Група 2: `{g2}`\)\n"
        f"📅 *День:* {DAYS_NAMES[now.weekday()]}\n"
        f"📆 *Навчальний тиждень:* `{week}`\n"
        f"🕒 *Час \(Київ\):* `{now.strftime('%H:%M:%S')}`\n"
        f"🧪 *Тестова пара:* `{test_start}` \- сповіщення прийде за \~1 хв"
    )
    await bot.send_message(message.chat.id, status_text, parse_mode="MarkdownV2")

    StateManager.delete(message.from_user.id)