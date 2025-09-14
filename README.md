# LinguaLink

LinguaLink is a Telegram bot + FastAPI server that provides real-time multi-language translation in Telegram groups. Each participant can write in their own language and others receive an in-group translated message.

## What’s inside

- FastAPI translation server backed by a local NLLB model (facebook/nllb-200-distilled-600M)
- Telegram bot (python-telegram-bot) for group handling and mentions
- Firestore storage for user language preferences and tracked group members

## Features

- Real-time translation in groups (in-group messages, not private DMs)
- Per-user target language with `/setlang`
- Optional auto-detect for sender language when not set
- Diagnostics with `/status` (server health, your language, tracked members)

## Requirements

- Python 3.9+
- A Telegram Bot token in `src/config.py` (TELEGRAM_BOT_TOKEN)
- Firebase service account JSON at `data/lingualink-d4685-firebase-adminsdk-*.json`

Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Supported language codes (short → NLLB): en, he, es, ru, ar, fr, de

Upload supported languages to Firestore (one-time):

```bash
python scripts/upload_settings.py
```

## Run

1) Start the translation server (FastAPI):

```bash
python run_main_server.py
# Open http://127.0.0.1:8000/docs to test the /translate endpoint
```

2) Start the Telegram bot (new terminal):

```bash
python -m src.bot.main
```

3) Telegram setup (once):

- In BotFather: /setprivacy → Disable (so the bot can read group messages)
- Add the bot to your group and allow it to send/read messages (admin recommended)

4) Use in the group:

- Each participant runs once: `/setlang en` (or he, es, ru, ar, fr, de)
- Then just chat normally. The bot sends a translated message per target language and mentions recipients.
- `/status` shows server health and your saved language.

## API quick test

POST http://127.0.0.1:8000/translate

Body (JSON):

```json
{ "text": "שלום", "source_lang": "he", "target_lang": "en" }
```

Response:

```json
{ "translated_text": "Hello" }
```

## Troubleshooting

- 404 on / → Root redirects to /docs now; use http://127.0.0.1:8000/docs
- `/status` → “Server: DOWN”: start the server (run_main_server.py)
- No translations: ensure each recipient set `/setlang`; sender can rely on auto-detect but recipients must have a target language
- 400 from /translate: unsupported language code — use one of en, he, es, ru, ar, fr, de
- Slow first translation: model warmup; the bot uses a 30s timeout

## Commands

- `/start` — welcome and instructions
- `/setlang <code>` — set your target language (en|he|es|ru|ar|fr|de)
- `/status` — server OK?, your language, tracked members count
