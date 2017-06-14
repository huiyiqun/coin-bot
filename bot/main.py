import logging
import configparser

from telegram.ext import Updater, CommandHandler, Job
from .api.coindesk import CoinDeskAPI

api = CoinDeskAPI(['CNY', 'USD'])
subscribed_chat = {}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)

with open('config.ini') as f:
    config = configparser.RawConfigParser()
    config.read_file(f)

updater = Updater(token=config['main']['TOKEN'])


def format_exchange(prices):
    return '\n'.join([
        f'{currency}: {exchange}' for currency, exchange in prices.items()
    ])


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Hello!")


def price(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=format_exchange(api.prices()[0]))


def subscribe(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Subscribed')
    if not update.message.chat_id in subscribed_chat:
        subscribed_chat[update.message.chat_id] = None


def polling_price(bot, job):
    prices, time = api.prices()
    text = format_exchange(prices)
    for chat_id, msg_id in subscribed_chat.items():
        msg = bot.send_message(chat_id=chat_id, disable_notification=True,
                               text=f'{text}\n\nupdated at {time}')
        if subscribed_chat[chat_id] is not None:
            # delete stale message
            bot.delete_message(
                chat_id=chat_id,
                message_id=subscribed_chat[chat_id])
        subscribed_chat[chat_id] = msg.message_id


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('price', price))
updater.dispatcher.add_handler(CommandHandler('subscribe', subscribe))
updater.job_queue.put(Job(polling_price, 10.0), next_t=0.0)
updater.start_polling()
