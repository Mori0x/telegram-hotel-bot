from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    city_name = State()
    hotels_count = State()
    photos = State()
    photos_counts = State()
    check_in = State()
    check_out = State()
    mode = State()
    search_status = State()
    price_range = State()
    distance_range = State()
    null = State()