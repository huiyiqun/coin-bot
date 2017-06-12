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
    reply_msg = bot.send_message(chat_id=update.message.chat_id,
                                 text=f'Following message will be updated:\n\n{format_exchange(api.prices()[0])}')
    if update.message.chat_id in subscribed_chat:
        # delete old subscription
        bot.delete_message(
            chat_id=update.message.chat_id,
            message_id=subscribed_chat[update.message.chat_id])
    subscribed_chat[update.message.chat_id] = reply_msg.message_id


def polling_price(bot, job):
    prices, time = api.prices()
    text = format_exchange(prices)
    for chat_id, msg_id in subscribed_chat.items():
        bot.edit_message_text(chat_id=chat_id, message_id=msg_id,
                              text=f'{text}\n\nupdated at {time}')


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('price', price))
updater.dispatcher.add_handler(CommandHandler('subscribe', subscribe))
updater.job_queue.put(Job(polling_price, 10.0), next_t=0.0)
updater.start_polling()
