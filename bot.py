import telebot
from config import Config
from database.queries import Database
from status.manager import StatusManager
from router import Router
from utils.logger import logger

def main():
    """Main bot entry point for polling mode"""
    
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
    
    # ============ START POLLING ============
    
    logger.info("🚀 Nuun Bot started in polling mode")
    logger.info("📡 All messages routed through Router")
    bot.remove_webhook()
    bot.infinity_polling()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped")