from text.messages import Messages
from keyboard import Keyboard

class HelHandler:
    """Handle Hel Waydiin (launch Mini App)"""
    
    def __init__(self, bot, db, status, config):
        self.bot = bot
        self.db = db
        self.status = status
        self.config = config
    
    def handle_hel_waydiin(self, message):
        """Send Hel Waydiin message with Mini App button"""
        user_id = message.from_user.id
        
        # Create Web App button
        from telebot import types
        keyboard = types.InlineKeyboardMarkup()
        webapp_button = types.WebAppInfo(url=self.config.WEBHOOK_URL)  # Or your mini app URL
        button = types.InlineKeyboardButton(
            "🎯 Open Nuun Quiz",
            web_app=webapp_button
        )
        keyboard.add(button)
        
        # Send message
        self.bot.send_message(
            user_id,
            Messages.hel_message(),
            parse_mode='HTML',
            reply_markup=keyboard
        )