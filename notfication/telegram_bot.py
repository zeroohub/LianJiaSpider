# -*- coding: utf-8 -*-

import telegram
from env import TELEGRAM_BOT_TOKEN
chat_id = 525052106


def send_message(text):
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    bot.send_message(chat_id, text)
