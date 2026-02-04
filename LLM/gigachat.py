import re
from gigachat.models import Chat, Messages, MessagesRole
from logger import logger

class gigachat_class:
    def __init__(self, client, default_prompt):
        self.client = client
        self.default_prompt = default_prompt

    def _extract_clean_text(self, text: str) -> str:
        text = re.sub(r'```[a-z]*\n', '', text)
        text = re.sub(r'\n```', '', text)
        text = text.strip()
        return text

    async def ask_question(self, message: str) -> str:
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
            reply = response.choices[0].message.content
            return self._extract_clean_text(reply)

        except Exception as e:
            logger.error(f"Ошибка gigachat {e}")
            return ''