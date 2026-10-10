from bot.states.StateManager import StateManager
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from bot.states.surveys import surveys

name="survey_results"

async def exec(bot: AsyncTeleBot, query: types.CallbackQuery, args):
    survey_id, count = args
    
    results = await surveys.get(int(survey_id))

    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("🔄 Оновити результати", callback_data=f"survey_results:{survey_id}:{count}")
    )
    markup.row(
        types.InlineKeyboardButton("❌ Видалити дані", callback_data=f"delete_survey:{survey_id}")
    )

    await bot.edit_message_text(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        text=f"📊 Результати опитування:\n\n"
        f"🟢 Позитивні відповіді \- *{results.get('yes')}*\n"
        f"🔴 Негативні відповіді \- *{results.get('no')}*\n"
        f"⚪️ Всього опитаних \- *{count}*",
        parse_mode="MarkdownV2",
        reply_markup=markup
    )