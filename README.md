# LinguaLink

LinguaLink is a Telegram bot that provides real-time, multi-language translation in group chats. It allows users in a group to communicate seamlessly, each in their own native language.

## Features

- **Real-time Translation**: Messages are translated instantly.
- **Multi-Language Support**: Each user can set their own preferred language.
- **Group Chat Integration**: Works within Telegram group chats.
- **Private Translations**: Translations are sent as private messages to keep the main chat clean.
- **Persistent Settings**: User language preferences are saved and reloaded on restart.

## How It Works

The project consists of two main components:
1.  **Telegram Bot (`telegram_bot.py`)**: This is the main application that interacts with users on Telegram. It handles commands, manages user language settings, and sends/receives messages.
2.  **Translation Server (`translation_server.py`)**: A FastAPI server that exposes a `/translate` endpoint. It receives translation requests from the bot, uses the Google Gemini API to perform the translation, and returns the result.

This architecture decouples the bot from the translation service, making the system more modular and scalable.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/saroatov2910/LinguaLink.git
    cd LinguaLink
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your API keys:**
    - Open the `src/config.py` file.
    - Set your `TELEGRAM_BOT_TOKEN` and `GEMINI_API_KEY`.

## Usage

1.  **Start the translation server:**
    ```bash
    uvicorn src.translation_server:app --reload
    ```

2.  **Start the Telegram bot (in a separate terminal):**
    ```bash
    python3 src/telegram_bot.py
    ```

3.  **Interact with the bot on Telegram:**
    - Add the bot to a group chat.
    - Each user should send `/start` to the bot in a private message to allow the bot to message them.
    - Each user should set their language using the `/setlang` command in the group chat (e.g., `/setlang he`).
    - Start chatting! The bot will automatically translate messages and send them privately.

## Bot Commands

- `/start`: Displays a welcome message.
- `/setlang <language_code>`: Sets your preferred language (e.g., `/setlang en` for English, `/setlang es` for Spanish).
