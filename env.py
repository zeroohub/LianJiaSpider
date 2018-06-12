# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


MONGO_URI = os.getenv('MONGO_URI')
MONGO_DB = os.getenv('MONGO_DB')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
