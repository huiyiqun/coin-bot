import logging
import configparser

from telegram.ext import Updater, CommandHandler
from .api.coindesk import CoinDeskAPI

api = CoinDeskAPI(['CNY', 'USD'])

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)

with open('config.ini') as f:
    config = configparser.RawConfigParser()
    config.read_file(f)

updater = Updater(token=config['main']['TOKEN'])
dispatcher = updater.dispatcher


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Hello!")


def price(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=api.prices())


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('price', price))
updater.start_polling()
