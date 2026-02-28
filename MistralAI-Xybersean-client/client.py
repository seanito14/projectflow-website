import os
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()

class MistralAIClient:
    def __init__(self):
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY not found in environment variables.")
        
        self.client = Mistral(api_key=api_key)
        self.model = os.getenv("MISTRAL_MODEL", "mistral-large-latest")

    def chat(self, messages, stream=False):
        if stream:
            return self.client.chat.stream(
                model=self.model,
                messages=messages
            )
        else:
            return self.client.chat.complete(
                model=self.model,
                messages=messages
            )
