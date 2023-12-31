from dotenv import load_dotenv, find_dotenv
import os

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()


BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
PATH = os.getcwd() + '\\data.txt'
DEFAULT_COMMANDS = (
    ('search', "Start searching hotels"),
    ('help', "Show instruction"),
    ('history', "Show history of searching"),
)
