# Monetag Earning Telegram Bot

## Features
- Users earn points by watching Monetag ads in a Telegram Mini App
- Points tracked and managed by a Python backend (aiogram + FastAPI)
- Withdraw system (manual, for now)
- Developer: https://t.me/aenzk

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your Telegram bot token in `.env`:
   ```env
   BOT_TOKEN=your_telegram_bot_token_here
   WEBAPP_URL=http://localhost:8000
   ```
3. Start the FastAPI backend (for webapp and API):
   ```bash
   uvicorn bot.api:app --reload --host 0.0.0.0 --port 8000
   ```
4. Start the Telegram bot:
   ```bash
   python bot/bot.py
   ```
5. Deploy `webapp/index.html` to a static host (or serve via FastAPI for production).

## Notes
- The webapp uses Monetag ad integration and communicates with the backend for rewards.
- All user points are stored in a local SQLite database.
- For production, secure the API and use HTTPS.
