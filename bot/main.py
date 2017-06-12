import logging
import configparser

from telegram.ext import Updater, CommandHandler, Job
from .api.coindesk import CoinDeskAPI

api = CoinDeskAPI(['CNY', 'USD'])
subscribed_chat = set()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)

with open('config.ini') as f:
    config = configparser.RawConfigParser()
    config.read_file(f)

updater = Updater(token=config['main']['TOKEN'])


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Hello!")


def price(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=api.prices())


def subscribe(bot, update):
    subscribed_chat.add(update.message.chat_id)


def polling_price(bot, job):
    prices = api.prices()
    for chat_id in subscribed_chat:
        bot.send_message(chat_id=chat_id, text=prices)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('price', price))
updater.dispatcher.add_handler(CommandHandler('subscribe', subscribe))
updater.job_queue.put(Job(polling_price, 60.0), next_t=0.0)
updater.start_polling()
