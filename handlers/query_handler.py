from aiogram import Router
from aiogram.types import Message
from LLM import gigachat_instance
from database.query_manager import db_manager
from logger import logger

query_router = Router()

@query_router.message()
async def query_handler(message: Message):
    await message.chat.do("typing")
    sql_query = None
    for _ in range(5):
        sql_query = await gigachat_instance.ask_question(message.text)
        if sql_query:
            logger.info(f"SQL_QUERY {sql_query}")
            break
    
    if not sql_query:
        logger.warning("Failed to generate SQL query")
        await message.answer('-1')
        return
    
    result = await db_manager.execute_sql(sql_query)

    if result is None:
        logger.warning("Failed execute query")
        await message.answer('-1')
        return
    
    await message.answer(text=str(result))
