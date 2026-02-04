import asyncio
from create_bot import bot, dp
from handlers.echo_for_test import echo_router
from logger import logger


async def main():

    dp.include_router(echo_router)

    try:
        logger.info("Starting bot")
        await bot.delete_webhook()
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
