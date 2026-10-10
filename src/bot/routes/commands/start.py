from telebot import types, async_telebot

name = "/start"

async def exec(bot: async_telebot.AsyncTeleBot, message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("Група 1", callback_data="set_group:1"),
        types.InlineKeyboardButton("Група 2", callback_data="set_group:2")
    )
    await bot.send_message(
        message.chat.id, 
        f"Привіт, *{message.from_user.first_name}*\! 👋\n"
        f"📊 Обери свою групу кнопками нижче, щоб отримувати правильний розклад:",
        parse_mode="MarkdownV2",
        reply_markup=markup
    )