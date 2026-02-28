import json
import os
from client import MistralAIClient

class AgenticLoop:
    def __init__(self, client: MistralAIClient):
        self.client = client
        self.history = [
            {"role": "system", "content": """You are a highly skilled AI App Builder and Agent. Your goal is to help the user build applications, write code, and solve complex problems. 

You reason step-by-step. When you generate code that should be saved to a file, use a code block with a filename comment on the first line, like this:
```python
# filename: hello.py
print("Hello World")
```
The system will detect these and provide an easy way to save them."""}
        ]

    def run(self, user_input):
        self.history.append({"role": "user", "content": user_input})
        
        # Simple reasoning loop for now: Think -> Action/Response
        # Extension: Tool use can be added here
        
        response = self.client.chat(self.history)
        assistant_content = response.choices[0].message.content
        
        self.history.append({"role": "assistant", "content": assistant_content})
        return assistant_content

    def clear_history(self):
        self.history = [self.history[0]]
