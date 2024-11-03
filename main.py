import asyncio
from aiogram import Dispatcher
from config import bot
import handlers
import database

dp = Dispatcher()
dp.include_router(handlers.router)

async def main():
    database.Base.metadata.create_all(database.engine)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')