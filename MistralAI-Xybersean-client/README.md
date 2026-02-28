# Mistral AI - Xybersean Client & App Builder

An agentic CLI tool designed for the Mistral Worldwide Hacks. Powered by **Mistral Large 3**.

## Features

- **Agentic Reasoning**: Step-by-step thinking for complex problem solving.
- **App Builder**: Detects generated code blocks and offers to save them to your local filesystem automatically.
- **Rich Interface**: Beautiful terminal output with markdown rendering.

## Setup

1. **Prerequisites**: Ensure you have Python 3.10+ installed.
2. **Environment**:
   - Create a `.env` file (copy `.env.example`).
   - Add your `MISTRAL_API_KEY`.
3. **Install Dependencies**:

   ```bash
   pip install mistralai rich python-dotenv
   ```

   (Or use the provided venv if you used the setup script).

## Usage

Run the client:

```bash
python main.py
```

*(Or use `MyMistral` if you set up the alias)*

### Commands

- `/help`: Detailed help instructions.
- `/clear`: Reset the conversation history and tokens.
- `/stats`: View your current session API token usage.
- `/save_chat`: Download your current chat history to `chat_log.json`.
- `/exit` or `/quit`: Close the client.

### App Builder Flow

When the agent generates code, it will use a special format:

```python
# filename: my_script.py
print("Hello!")
```

The CLI will automatically detect this and ask:
`App Builder: Save generated code to my_script.py? [y/n]`

Confirm with `y` to save it directly to the current directory.
