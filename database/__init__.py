from loader import bot
from handlers import custom_handlers
from config_data import config


def show(message):
    with open(config.PATH, 'r', encoding='utf-8') as data:
        data = data.readlines()
        data.append(' ')
        if len(data) == 0:
            bot.send_message(message.from_user.id, "You haven't searching yet, type /search to start searching")
            custom_handlers.getting_info.checking(message)
        results = ''
        counter = -1
        for action in data:
            counter += 1
            if len(action) < 60:
                if counter != 0:
                    bot.send_message(message.from_user.id, f'time: {time}, command: {command} results: {results}', disable_web_page_preview=True)
                    results = ''
                time = action[:10] + ' ' + action[11:19]
                command = action[32:]
            else:
                results = results + action[31:] + ' '
