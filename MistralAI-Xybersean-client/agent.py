import json
import os
import tiktoken
from client import MistralAIClient

class AgenticLoop:
    def __init__(self, client: MistralAIClient):
        self.client = client
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.history = [
            {"role": "system", "content": """You are a highly skilled AI App Builder and Agent. Your goal is to help the user build applications, write code, and solve complex problems. 

You reason step-by-step. When you generate code that should be saved to a file, use a code block with a filename comment on the first line, like this:
```python
# filename: hello.py
print("Hello World")
```
The system will detect these and provide an easy way to save them."""}
        ]
        
        # Fallback encoding for token counting
        try:
            self.encoding = tiktoken.encoding_for_model("gpt-4") # Approximation for LLMs if Mistral tokenizer is unavailable
        except KeyError:
            self.encoding = tiktoken.get_encoding("cl100k_base")

    def run(self, user_input):
        self.history.append({"role": "user", "content": user_input})
        
        # Simple reasoning loop for now: Think -> Action/Response
        # Extension: Tool use can be added here
        
        response = self.client.chat(self.history)
        assistant_content = response.choices[0].message.content
        
        usage = response.usage
        prompt_tokens = 0
        completion_tokens = 0
        
        if usage:
            prompt_tokens = usage.prompt_tokens
            completion_tokens = usage.completion_tokens
        else:
            # Fallback counting
            prompt_text = "".join([m["content"] for m in self.history])
            prompt_tokens = len(self.encoding.encode(prompt_text))
            completion_tokens = len(self.encoding.encode(assistant_content))
            
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        
        usage_info = {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens
        }
        
        self.history.append({"role": "assistant", "content": assistant_content})
        return assistant_content, usage_info

    def clear_history(self):
        self.history = [self.history[0]]
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
