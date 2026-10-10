from telebot.async_telebot import AsyncTeleBot
from telebot import types

name="send_broadcast"

async def exec(bot: AsyncTeleBot, query: types.CallbackQuery, args):
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("💬 Звичайне повідомлення", callback_data="get_broadcast_message:msg")
    )
    markup.row(
        types.InlineKeyboardButton("🔘 Так/Ні опитування", callback_data="get_broadcast_message:survey")
    )
    
    await bot.edit_message_text(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        text=f"🌀 Вибери тип оповіщення:",
        reply_markup=markup
    )