import os
from gigachat import GigaChat
from LLM.gigachat import gigachat_class
from logger import logger

client = GigaChat(
                credentials=os.getenv("GIGACHAT_API_KEY"),
                verify_ssl_certs=False,
                model="GigaChat",
                timeout=30
            )

gigachat_instance = gigachat_class(client, "default_prompt")

logger.info("gigachat was initialized")
