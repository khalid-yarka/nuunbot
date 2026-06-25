from flask import Flask, request
import telebot
from config import Config
from database.queries import Database
from status.manager import StatusManager
from router import Router
from utils.logger import logger

app = Flask(__name__)

# Load config
config = Config()
config.validate()

# Initialize bot
bot = telebot.TeleBot(config.BOT_TOKEN)

# Initialize database
db = Database(config.DATABASE_PATH)

# Initialize status manager
status = StatusManager(db)

# ==========================================
# SINGLE DOOR: Everything goes through Router
# ==========================================
router = Router(bot, db, status, config)

# ============ WEBHOOK ENDPOINT ============

@app.route(config.WEBHOOK_PATH, methods=['POST'])
def webhook():
    """Handle incoming Telegram updates"""
    try:
        json_str = request.get_data().decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return 'OK', 200
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return 'Error', 500

# ============ SET WEBHOOK ============

def set_webhook():
    """Set webhook URL"""
    webhook_url = f"{config.WEBHOOK_URL}{config.WEBHOOK_PATH}"
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    logger.info(f"🌐 Webhook set to: {webhook_url}")

if __name__ == "__main__":
    set_webhook()
    app.run(host='0.0.0.0', port=5000)