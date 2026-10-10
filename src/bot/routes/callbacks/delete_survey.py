from bot.states.StateManager import StateManager
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from bot.states.surveys import surveys

name="delete_survey"

async def exec(bot: AsyncTeleBot, query: types.CallbackQuery, args):
    survey_id,  = args
    
    await surveys.delete(int(survey_id))
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("🧑‍💻 Назад в меню", callback_data="menu")
    )

    await bot.edit_message_text(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        text=f"🫡 Дані про опитування видалені!",
        reply_markup=markup
    )