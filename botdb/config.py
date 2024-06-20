import logging
from aiogram import Bot, Dispatcher

# Объявляем переменные
TOKEN = ''
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()
