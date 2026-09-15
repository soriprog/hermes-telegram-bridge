# Hermes Telegram Bridge

A custom Telegram bot bridge connecting Telegram chats directly to the **Hermes AI Agent** framework via OpenAI-compatible endpoints.

## Features
- Connects Telegram bots to Hermes LLM core.
- Asynchronous message handling (`python-telegram-bot`).
- Secure environment configuration (`python-dotenv`).
- Structured logging (`bot.log`).

## Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/soriprog/hermes-telegram-bridge.git
   cd hermes-telegram-bridge
   ```
2. Create and activate a virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate
   pip install -r requirements.txt # or install python-telegram-bot openai python-dotenv
   ```
3. Create a `.env` file based on `.env.example`:
   ```env
   TELEGRAM_TOKEN=your_telegram_bot_token
   HERMES_CUSTOM_API_KEY=your_hermes_api_key
   ```
4. Run the bot:
   ```bash
   python bot.py
   ```
