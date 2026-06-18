from openai import OpenAI

from src.config.settings import settings


class LLMClient:

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openai_api_key
        )


    def chat(self, message: str) -> str:

        response = self.client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content":
                    "You are Jarvis, a helpful personal assistant."
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return response.choices[0].message.content