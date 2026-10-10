from database.Database import Database
from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery
import datetime
from zoneinfo import ZoneInfo
from utils.get_current_week import get_current_week
TZ = ZoneInfo("Europe/Kyiv") 

DAYS_NAMES = (
    "Понеділок", 
    "Вівторок", 
    "Середа", 
    "Четвер",
    "П'ятниця", 
    "Субота", 
    "Неділя"
)

name="test"

async def exec(bot: AsyncTeleBot, query: CallbackQuery, _):
    users = await Database.query(
        Database.db.table("users").select("group", "id").execute()
    )
    
    g1 = sum(1 for g in users if g["group"] == 1)
    g2 = sum(1 for g in users if g["group"] == 2)
    
    now = datetime.datetime.now(TZ)
    test_start = (now + datetime.timedelta(minutes=10)).strftime("%H:%M")
    for user in users:
        await bot.send_message(chat_id=user.get("id"), text=(
            f"⏰ *Нагадування\! Через 10 хвилин пара\!*\n\n"
            f"📘 *Предмет:* Тест\n"
            f"🕒 *Початок о:* {test_start}\n"
            f"🔗 *Посилання:* [Приєднатися](https://zoom.us)"
        ),
        parse_mode="MarkdownV2",
        disable_web_page_preview=True)
    week = get_current_week(now.date())
    
    status_text = (
        "📊 *ЗВІТ ПРО СТАН СИСТЕМИ*\n"
        "━━━━━━━━━━━━━━━\n"
        f"👥 *Підписників:* `{len(users)}` \(Група 1: `{g1}`, Група 2: `{g2}`\)\n"
        f"📅 *День:* {DAYS_NAMES[now.weekday()]}\n"
        f"📆 *Навчальний тиждень:* `{week}`\n"
        f"🕒 *Час \(Київ\):* `{now.strftime('%H:%M:%S')}`\n"
        f"🧪 *Тестова пара:* `{test_start}` \- сповіщення прийде за \~1 хв"
    )
    await bot.send_message(query.message.chat.id, status_text, parse_mode="MarkdownV2")
    