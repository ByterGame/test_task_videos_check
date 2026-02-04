import re
from logger import logger
from gigachat.models import Chat, Messages, MessagesRole
from typing import Optional

class gigachat_class:
    def __init__(self, client, default_prompt: str):
        self.client = client
        self.default_prompt = default_prompt
    
    def _extract_sql(self, text: str) -> Optional[str]:
        text = text.replace("```sql", "").replace("```", "").strip()
        
        patterns = [
            r'(SELECT .*?;)',
            r'(SELECT .*)',
            r'(select .*;)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                sql = match.group(1).strip()
                return sql


    async def ask_question(self, message: str, max_retries: int = 5) -> Optional[str]:

        for attempt in range(max_retries):
            try:
                messages = [
                    Messages(role=MessagesRole.SYSTEM, content=self.default_prompt),
                    Messages(role=MessagesRole.USER, content=message)
                ]
                
                chat = Chat(
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1000,
                )
                
                response = self.client.chat(chat)
                reply = response.choices[0].message.content.strip()
                logger.info(f"REPLY {reply}")
                sql = self._extract_sql(reply)
                
                if sql:
                    return sql
                
            except Exception as e:
                logger.error(f"Error in ask_question: {e}")
                if attempt == max_retries - 1:
                    logger.error(f"wasted attempts to get the request for the question {message}")
        
        return None