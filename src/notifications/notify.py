from pathlib import Path
import json
import datetime
from zoneinfo import ZoneInfo
from utils.get_current_week import get_current_week
from notifications.sent_notifications import sent_notificatiotns
from database.Database import Database
import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot.formatting import escape_markdown
SLEEP_INTERVAL = 15 #seconds
TZ = ZoneInfo("Europe/Kyiv")
PARENT_DIR = Path(__file__).resolve().parent
schedule_path = PARENT_DIR / "schedule.json"

async def notify(bot: AsyncTeleBot):
    print("Info | Notification system has successfully started!")
    while True:
        try:
            users = await Database.query(
                Database.db.table("users").select("*").execute()
            )

            for user in users:
                notifications_lessons = get_notifications_lessons(notify_time=user.get("notify_time"))
                for lesson in notifications_lessons:
                    if lesson.get("group") == 0 or lesson.get("group") == user.get("group"):
                        await send_notification(lesson=lesson, chat_id=user.get("id"), bot=bot, online_mode=user.get("online_mode"))
        except Exception as error:
            print("Error | Notification error")
            print(error)
        await asyncio.sleep(SLEEP_INTERVAL)

def get_notifications_lessons(notify_time: int):
    active_lessons = get_active_lessons()
    notifications_lessons = []
    for lesson in active_lessons:
        hour, minute = map(int, lesson.get("time").split(":"))
        now = datetime.datetime.now(TZ)
        delta = datetime.timedelta(hours=hour, minutes=minute) - datetime.timedelta(hours=now.hour, minutes=now.minute)
        id = "|".join([lesson.get("name"), lesson.get("time"), str(lesson.get("group")), str(now.date().isoformat())])
        if delta.total_seconds() < 0:
            sent_notificatiotns.discard(id)
            continue
        if delta > datetime.timedelta(minutes=notify_time):
            continue
        if id in sent_notificatiotns:
            continue
        notifications_lessons.append(lesson)
        sent_notificatiotns.add(id)
        print(sent_notificatiotns)

    return notifications_lessons


def get_active_lessons(day=None):
    if not day:
        day = datetime.datetime.now(TZ).weekday()
    with open(schedule_path, encoding="utf-8") as file:
        schedule = json.load(file)
        day_lessons = schedule[day]
        week = get_current_week()
        return [
            l 
            for l in day_lessons
            if len(l.get("weeks")) == 0 or (
                l.get("weeks")[0] <= week <= l.get("weeks")[1]
            )
        ]

async def send_notification(lesson, chat_id: int, bot: AsyncTeleBot, online_mode: bool):
    text = (
        f"⏰ *Нагадування\! Через 10 хвилин пара\!*\n\n"
        f"📘 *Предмет:* {escape_markdown(lesson.get('name'))}\n"
        f"🕒 *Початок о:* {lesson.get('time')}\n"
        + (
        f"🔗 *Посилання:* [Приєднатися]({lesson.get('link')})" if online_mode else (
            f"*Аудиторія:* {lesson.get('room')}," +
            f"{' поверх' if isinstance(lesson.get('room'), int) else ''} {escape_markdown(str(lesson.get('floor')))}"
        ))
    )
    try:
        await bot.send_message(
            chat_id=chat_id, 
            text=text, 
            parse_mode="MarkdownV2", 
            disable_web_page_preview=True
        )
    except Exception:
        print(
            f"ERROR | Markdown notification failed. User ID = {chat_id}"
        )
        try:
            await bot.send_message(
                chat_id=chat_id, 
                text=text.replace("*", ""), 
                disable_web_page_preview=True
            )
        except Exception as err:
            print(f"ERROR | Sending notifications got error. User ID = {chat_id}")
            print(err)

    


        