from aiogram import Router
from aiogram.types import Message
from LLM import gigachat_instance
from logger import logger

echo_router = Router()

@echo_router.message()
async def echo(message: Message):
    logger.info("get message in echo")
    for i in range(5):
        try:
            resp = await gigachat_instance.ask_question(message.text)
            await message.answer(text=resp, parse_mode=None)
            return
        except Exception as e:
            logger.error(f"Error echo handler: {e}\nStart {i + 2} iteration")
