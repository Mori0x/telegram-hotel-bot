from loader import bot
from states.users_information import UserInfoState
from keyboards import reply, inline
from telebot.types import Message
from handlers import default_handlers
import database
from loguru import logger
from config_data import config


logger.add(config.PATH, format="{time} {message}", level='INFO')


@bot.message_handler(commands=['search'])
def start(message: Message):
    reply.reply_keyboard(message)
    bot.set_state(message.from_user.id, UserInfoState.mode)


@bot.message_handler(state=UserInfoState.mode)
def choosing_mode(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text == '/history':
            database.show(message)
    bot.send_message(message.from_user.id, 'What city?(in English)')
    bot.set_state(message.from_user.id, UserInfoState.city_name)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['mode'] = message.text
        logger.info(data['mode'])


@bot.message_handler(state=UserInfoState.city_name)
def if_best_deal(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city_name'] = message.text.lower()
        if data['mode'] == '/bestdeal':
            bot.send_message(message.from_user.id, "Input price range per night in dollars(min-max)")
            bot.set_state(message.from_user.id, UserInfoState.price_range)
        else:
            data['price_range'] = [0, 0]
            data['distance_range'] = [0, 0]
            get_city(message)


@bot.message_handler(state=UserInfoState.price_range)
def distance_range(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['price_range'] = message.text.split('-')
        if data['mode'] == '/bestdeal':
            bot.send_message(message.from_user.id, "Input distance range(min-max)")
            bot.set_state(message.from_user.id, UserInfoState.distance_range)


@bot.message_handler(state=UserInfoState.distance_range)
def get_city(message: Message):
    bot.send_message(message.from_user.id, "How many hotels?")
    bot.set_state(message.from_user.id, UserInfoState.hotels_count)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['distance_range'] = message.text.split('-')


@bot.message_handler(state=UserInfoState.hotels_count)
def get_checkin(message: Message):
    bot.send_message(message.from_user.id, 'date of check in (yyyy-mm-dd)')
    bot.set_state(message.from_user.id, UserInfoState.check_in)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['hotels_count'] = message.text


@bot.message_handler(state=UserInfoState.check_in)
def get_checkout(message: Message):
    bot.send_message(message.from_user.id, 'date of check out (yyyy-mm-dd)')
    bot.set_state(message.from_user.id, UserInfoState.check_out)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['check_in'] = message.text


@bot.message_handler(state=UserInfoState.check_out)
def get_photos(message: Message):
    inline.inline_keyboard(message)
    bot.set_state(message.from_user.id, UserInfoState.photos)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['check_out'] = message.text


@bot.callback_query_handler(func=lambda call: True)
@bot.message_handler(state=UserInfoState.photos)
def check_photos(call):
    if call.data == "yes":
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['photos'] = True
        bot.send_message(call.message.chat.id, 'How many photos?')
        bot.set_state(call.from_user.id, UserInfoState.photos_counts)
    else:
        bot.send_message(call.message.chat.id, 'Analyzing...')
        bot.set_state(call.from_user.id, UserInfoState.null)
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['photos'] = False
            data['photos_counts'] = 0

            my_id = default_handlers.hotels.check(data['city_name'])
            if my_id == False:
                bot.send_message(call.message.chat.id, 'Check city name and try again /search')
            else:
                info, count = default_handlers.hotels.hotels_info(my_id, data['check_in'], data['check_out'], data['mode'], data['price_range'][0], data['price_range'][1])
                default_handlers.hotels.check_photos_count(data['hotels_count'], count, call.message, info, data['photos'],
                                                           data['photos_counts'], data['distance_range'][0], data['distance_range'][1])


@bot.message_handler(state=UserInfoState.photos_counts)
def photos_count(message: Message):
    bot.send_message(message.from_user.id, 'Analyzing...')
    bot.set_state(message.from_user.id, UserInfoState.null)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if data['photos']:
            data['photos_counts'] = message.text
        my_id = default_handlers.hotels.check(data['city_name'])
        if my_id == False:
            bot.send_message(message.from_user.id, 'Check city name and try again /search')
        else:
            info, count = default_handlers.hotels.hotels_info(my_id, data['check_in'], data['check_out'], data['mode'], data['price_range'][0], data['price_range'][1])
            default_handlers.hotels.check_photos_count(data['hotels_count'], count, message, info, data['photos'], data['photos_counts'], data['distance_range'][0], data['distance_range'][1])


@bot.message_handler(content_types=['text'])
def checking(message: Message):
    if message.text == '/help':
        default_handlers.help.help_bot(message)
    elif message.text == '/history':
        database.show(message)
    elif message.text != '/search':
        bot.send_message(message.from_user.id, 'Start searching, type /search')

