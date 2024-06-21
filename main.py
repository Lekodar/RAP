import asyncio
import utils
from config import bot, dp
from aiogram import Bot, Dispatcher
from utils import set_main_menu


# Функция для запуска бота

async def main():
    await dp.start_polling(bot)
    await set_main_menu(bot)

dp.startup.register(set_main_menu)

if __name__ == "__main__":
    asyncio.run(main())
