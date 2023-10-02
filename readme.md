# Hotel Search Telegram Bot

## Overview
This Telegram bot allows users to search for hotels based on different criteria such as price and distance from the city center. It utilizes the Telegram Bot API, Python, and the Hotels.com API via RapidAPI to provide a convenient way for users to find the perfect hotel for their needs.

## Commands

### `/highprice`
- **Description**: This command allows users to search for expensive hotels.
- **Usage**: `/highprice`
- **Functionality**: The bot will return a list of hotels with high prices, providing details such as hotel name, price per night, photos of hotel, and a brief description. The data is fetched from the Hotels.com API via RapidAPI.

### `/lowprice`
- **Description**: This command allows users to search for cheap hotels.
- **Usage**: `/lowprice`
- **Functionality**: The bot will return a list of hotels with low prices, providing details such as hotel name, price per night, photos of hotel, and a brief description. The data is fetched from the Hotels.com API via RapidAPI.

### `/bestdeal`
- **Description**: This command allows users to search for the best deals on hotels, considering both price and distance from the city center.
- **Usage**: `/bestdeal`
- **Functionality**: The bot will return a list of hotels that offer the best combination of affordable prices and proximity to the city center. It will provide details such as hotel name, price per night, distance from the center, photos of hotel, and a brief description. The data is fetched from the Hotels.com API via RapidAPI.

### `/history`
- **Description**: This command allows user to view all hotels which he searched for and information about them
- **Usage**: `/history`
- **Functionality**: The bot will return message with time of searching results of search and command that user used(`/highprice` for example)

## How to Use
1. Start a chat with the bot on Telegram with command `/search`.
2. Use the `/highprice` command to find expensive hotels.
3. Use the `/lowprice` command to find cheap hotels.
4. Use the `/bestdeal` command to find the best deals on hotels.

## Installation and Setup
To run this bot on your own server, follow these steps:

1. Clone this repository to your local machine.
2. Create a Telegram bot using the [BotFather](https://core.telegram.org/bots#botfather) on Telegram.
3. Obtain your bot's API token.
4. Sign up for RapidAPI and obtain the Hotels.com API key.
5. Install the required Python libraries, such as `python-telegram-bot` and `requests` for making API calls.
6. Set up your bot using the Telegram API token and configure the Hotels.com API key.
7. Deploy your bot on a server or hosting platform.
8. Run the bot script.

## Contributing
Feel free to contribute to the development of this bot by submitting pull requests or reporting issues on the GitHub repository.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author
Mori0x

## Acknowledgments
Special thanks to the Telegram Bot API, RapidAPI, and the Python community for making this project possible.
