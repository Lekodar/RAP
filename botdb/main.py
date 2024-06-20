import asyncio
import utils
from config import bot, dp


# Функция для запуска бота

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
