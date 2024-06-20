import logging
from aiogram import Bot, Dispatcher

# Объявляем переменные
TOKEN = 'сюда токен бота'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()
