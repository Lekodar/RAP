import logging
from aiogram import Bot, Dispatcher

# Объявляем переменные
TOKEN = '7378310970:AAGyq1Ijap7xQxugfbZa-iSgfFyUlx0W72U'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()
