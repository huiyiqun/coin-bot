import logging
import configparser

from telegram.ext import Updater, CommandHandler

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


dispatcher.add_handler(CommandHandler('start', start))
updater.start_polling()
