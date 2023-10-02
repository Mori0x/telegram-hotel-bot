import telebot
from telebot import types
from config_data import config

bot = telebot.TeleBot(config.BOT_TOKEN)


def inline_keyboard(message):
    keyboard_ph = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Yes', callback_data='yes')  # кнопка «Да»
    keyboard_ph.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='No', callback_data='no')
    keyboard_ph.add(key_no)
    question = 'Do you want to see photos'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard_ph)
