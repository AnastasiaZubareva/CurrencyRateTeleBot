from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests
from config import API_KEY, TOKEN
from currencyList import CURRENCY_LIST

URL = "https://api.fastforex.io/fetch-one"


bot = TeleBot(TOKEN)

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(row_width=3)
    for currency_name in CURRENCY_LIST.keys():
        item_button = KeyboardButton(currency_name)
        markup.add(item_button)
    bot.send_message(message.chat.id, "Choose a currency", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in CURRENCY_LIST.keys())
def send_price(message):
    currency_name = message.text
    ticker = CURRENCY_LIST[currency_name]
    price = get_curRate((get_currency_json(api_key=API_KEY, currFrom=currency_name)))
    bot.send_message(message.chat.id, f"Сurrent rate {currency_name} to RUB is {price}")


def get_currency_json(api_key: str, currFrom: str) -> requests.Response:
    url = URL
    params = {
        "from": currFrom,
        "to": "RUB",
        "api_key": api_key
    }
    response = requests.get(url, params=params)
    return response


def get_curRate(response: requests.Response) -> float:
    curRate = response.json()["result"]["RUB"]
    return curRate

bot.infinity_polling()
