# Nuun Bot

A Telegram bot for posting questions to a channel with place-based filtering.

## Features

- 📚 **Dir Waydiin**: Post questions with place, class, and subject filtering
- 🌐 **Hel Waydiin**: Launch external Mini App
- 📍 Place filtering: SL (Somaliland), SOM (Somalia), PL (Puntland), ALL
- 📚 Class selection: 7aad, 8aad, Sare 3aad, Sare 4aad
- 📖 Dynamic subject selection based on class
- ✅ Preview before posting
- 🎨 Beautiful channel formatting with flags and quotes
- 🇸🇴 Somali footers
- 🗄️ Database-based status management
- 🔄 /restore command for session recovery

## Installation

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate` (Linux) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your credentials

## Running

### Local (Polling Mode):