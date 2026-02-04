import asyncio
from create_bot import bot, dp
from handlers.query_handler import query_router
from database.query_manager import db_manager
from logger import logger


async def main():

    dp.include_router(query_router)

    try:
        logger.info("Starting bot")
        await bot.delete_webhook()
        await dp.start_polling(bot)
    finally:
        await db_manager.close()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
