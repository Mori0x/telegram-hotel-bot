import telebot
from telebot import types
from config_data import config

bot = telebot.TeleBot(config.BOT_TOKEN)


def reply_keyboard(message):
    keyboard = types.ReplyKeyboardMarkup()
    key_low = types.KeyboardButton(text='/lowprice')
    keyboard.add(key_low)
    key_high = types.KeyboardButton(text='/highprice')
    keyboard.add(key_high)
    key_deal = types.KeyboardButton(text='/bestdeal')
    keyboard.add(key_deal)
    key_history = types.KeyboardButton(text='/history')
    keyboard.add(key_history)
    question = 'Choose mode of searching'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
