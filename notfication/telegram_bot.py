# -*- coding: utf-8 -*-

import telegram
from telegram.ext import Updater, CommandHandler
from env import TELEGRAM_BOT_TOKEN
chat_id = 525052106


def send_message(text):
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    bot.send_message(chat_id, text)


def get_houses(bot, update):
    from analysis.house_update import get_all_houses
    bot.send_message(chat_id=update.message.chat_id, text=get_all_houses())


def start_listen():
    updater = Updater(token=TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher
    get_houses_handler = CommandHandler('get_houses', get_houses)
    dispatcher.add_handler(get_houses_handler)
    updater.start_polling()


if __name__ == '__main__':
    start_listen()
