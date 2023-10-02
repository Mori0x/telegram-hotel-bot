import requests, json
from loader import bot
from config_data import config
from telebot import types
from loguru import logger


def check(city_name):
    try:

        url = "https://hotels4.p.rapidapi.com/locations/v3/search"

        querystring = {"q": city_name, "langid": "1033", "siteid": "300000001"}

        headers = {
            "X-RapidAPI-Key": config.RAPID_API_KEY,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        data = json.loads(response.text)

        return data['sr'][0]['gaiaId']
    except:
        return False


def show_hotels(my_id, check_in, check_out):
    url = "https://hotels4.p.rapidapi.com/properties/list"
    headers = {
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    querystring = {"destinationId": my_id, "pageNumber": "1", "pageSize": "25", "checkIn": check_in,
                   "checkOut": check_out, "adults1": "1", "sortOrder": "PRICE", "locale": "en_US",
                   "currency": "USD"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    info = json.loads(response.text)
    count = len(info['data']['body']['searchResults']['results'])
    return info, count


def photos_info(hotel_id):
    import requests

    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": hotel_id
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    data = json.loads(response.text)
    return data['data']['propertyInfo']['propertyGallery']['images']


def details(my_id):
    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": my_id
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    data = json.loads(response.text)
    address = data['data']['propertyInfo']['summary']['location']['address']['addressLine']
    return address


def hotels_info(my_id, check_in, check_out, mode, min_price, max_price):
    if mode == '/lowprice' or mode == '/bestdeal':
        phrase = 'LOW_TO_HIGH'
    elif mode == '/highprice':
        phrase = 'HIGH_TO_LOW'
    year_in, month_in, day_in = check_in.split('-')
    year_out, month_out, day_out = check_out.split('-')
    if int(min_price) == 0 and int(max_price) != 0:
        min_price = 1

    url = "https://hotels4.p.rapidapi.com/properties/v2/list"

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": str(my_id)},
        "checkInDate": {
            "day": int(day_in),
            "month": int(month_in),
            "year": int(year_in)
        },
        "checkOutDate": {
            "day": int(day_out),
            "month": int(month_out),
            "year": int(year_out)
        },
        "rooms": [{"adults": 1}],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": f"PRICE_{phrase}",
        "filters": {
            "price": {
                'max': int(max_price),
                'min': int(min_price)
            }
        }
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    data = json.loads(response.text)
    count = len(data['data']['propertySearch']['properties'])
    info = data['data']['propertySearch']['properties']
    return info, count


def check_photos_count(hotels_count, count, message, info, photos, photos_counts, min_distance, max_distance):
    hotels_count = int(hotels_count)
    just_one_moment = hotels_count
    if hotels_count > count:
        bot.send_message(message.from_user.id, f'This region has only {count} hotel(s)')
        hotels_count = count
    nums = []
    counter = 0
    hotels_count = [int(i) for i in range(int(hotels_count))]
    if int(max_distance) != 0:
        for num in range(count):
            distance = info[num]['destinationInfo']['distanceFromDestination']['value']
            if int(round(distance, 0)) in range(int(min_distance), int(max_distance)+1):
                counter += 1
                nums.append(num)
            if counter == just_one_moment:
                break
        hotels_count = nums
    for order in hotels_count:
        distance = info[order]['destinationInfo']['distanceFromDestination']['value']
        my_id = info[order]['id']
        name = info[order]['name']
        try:
            price = info[order]['price']['displayMessages'][1]['lineItems'][0]['value']
        except:
            bot.send_message(message.from_user.id, f'Hotel with number {order+1} ({name}) has no rooms for this dates')
            continue
        address = details(my_id)
        if photos:
            medias = []
            photos_data = photos_info(my_id)
            if int(photos_counts) > len(photos_data):
                bot.send_message(message.from_user.id, f'This hotel has only {len(photos_data)} photos')
                photos_counts = len(photos_data)
            for index in range(int(photos_counts)):
                link = photos_data[index]['image']['url']
                medias.append(types.InputMediaPhoto(link))
            bot.send_media_group(message.from_user.id, medias)
        bot.send_message(message.chat.id, f'Hotel: {name}, price: {price}, address: {address}, distance from center: {distance},'
                                               f' url: https://www.hotels.com/h{my_id}.Hotel-Information', disable_web_page_preview=True)
        logger.info(f'Hotel: {name}, price: {price}, address: {address}, distance from center: {distance},'
                                               f' url: https://www.hotels.com/h{my_id}.Hotel-Information')