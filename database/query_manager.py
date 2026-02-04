import asyncpg
import os
from typing import Optional
from logger import logger

class DatabaseManager:
    def __init__(self):
        self.pool = None
    
    async def connect(self):
        if self.pool is None:
            try:
                self.pool = await asyncpg.create_pool(
                    user=os.getenv("POSTGRES_USER", "bot_user"),
                    password=os.getenv("POSTGRES_PASSWORD", "bot_password"),
                    database=os.getenv("POSTGRES_DB", "bot_db"),
                    host="postgres",
                    port=5432,
                    min_size=5,
                    max_size=20,
                    command_timeout=60
                )
                logger.info("pool created")
            except Exception as e:
                logger.error(f"Error in db_manager/connect {e}")
                raise
    
    async def execute_sql(self, sql_query: str) -> Optional[float]:
        if not self.pool:
            await self.connect()
        
        try:
            async with self.pool.acquire() as conn:
                result = await conn.fetchval(sql_query)
                if result is None:
                    logger.warning("result is None in execute_sql")
                    return None
                
                try:
                    result = float(result)
                    return result
                except (ValueError, TypeError):
                    logger.error(f"Result is not num: {result} (type: {type(result)})")
                    return None
                    
        except asyncpg.exceptions.PostgresError as e:
            logger.error(f"ErrorPostgreSQL: {e}")
            return None
        except Exception as e:
            logger.error(f"Query error in execute_sql: {e}")
            return None
    
    async def close(self):
        if self.pool:
            await self.pool.close()
            self.pool = None
            logger.info("Pool closed")

db_manager = DatabaseManager()