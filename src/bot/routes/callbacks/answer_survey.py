from bot.states.StateManager import StateManager
from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery
from bot.states.surveys import surveys

name="answer_survey"

async def exec(bot: AsyncTeleBot, query: CallbackQuery, args):
    survey_id, answer = args
    if not await surveys.exists(survey_id):
        await bot.edit_message_text(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            text=f"😢️️️️️️ Мені шкода, але відповіді більше не приймаються"
        )
        return
    
    await surveys.hincrby(int(survey_id), answer, 1)
    
    try:
        await bot.edit_message_text(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            text=f"☺️️️️️️️ Дякую за вашу відповідь!"
        )
    except:
        await bot.delete_message(query.message.chat.id, query.message.message_id)
        await bot.send_message(
            chat_id=query.message.chat.id,
            text=f"☺️️️️️️️ Дякую за вашу відповідь!"
        )