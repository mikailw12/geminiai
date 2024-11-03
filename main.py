import asyncio
import logging
import handlers
import config
from aiogram import Bot, Dispatcher
import database

bot = None

async def main():
    global bot
    bot = Bot(token=config.TOKEN)
    dp = Dispatcher()
    dp.include_router(handlers.router)
    database.Base.metadata.create_all(database.engine)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')

