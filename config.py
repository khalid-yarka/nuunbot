import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration manager for Nuun Bot"""
    
    # Bot
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    CHANNEL_ID = os.getenv('CHANNEL_ID')
    
    # Webhook
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
    WEBHOOK_PATH = os.getenv('WEBHOOK_PATH', '/webhook')
    
    # Database
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'database.db')
    
    # Features
    RATE_LIMIT_SECONDS = int(os.getenv('RATE_LIMIT_SECONDS', 60))
    MIN_QUESTION_LENGTH = int(os.getenv('MIN_QUESTION_LENGTH', 10))
    MAX_QUESTION_LENGTH = int(os.getenv('MAX_QUESTION_LENGTH', 1000))
    
    # Admin
    ADMIN_IDS = [int(id.strip()) for id in os.getenv('ADMIN_IDS', '').split(',') if id.strip()]
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required")
        if not cls.CHANNEL_ID:
            raise ValueError("CHANNEL_ID is required")
        return True