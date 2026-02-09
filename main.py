import asyncio
from aiogram import Bot, Dispatcher

from app.config import settings
from app.bot.routers import router
from app.db.init_db import init_db


async def main():
    await init_db()

    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(router)

    print("🤖 MONOSTONE_bot запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
