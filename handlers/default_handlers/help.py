from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=['help'])
def help_bot(message):
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, '\n'.join(text))