from telebot import types
from text.messages import Messages
from keyboard import Keyboard
from handlers.commands import CommandHandler
from handlers.waydiin import WaydiinHandler
from handlers.hel import HelHandler
from utils.logger import logger

class Router:
    """
    SINGLE DOOR FOR THE ENTIRE BOT
    All messages, commands, and callbacks go through this router
    """
    
    def __init__(self, bot, db, status, config):
        self.bot = bot
        self.db = db
        self.status = status
        self.config = config
        
        # Initialize all handlers
        self.commands = CommandHandler(bot, db, status, config)
        self.waydiin = WaydiinHandler(bot, db, status, config)
        self.hel = HelHandler(bot, db, status, config)
        
        # Register all handlers
        self._register_handlers()
        
        logger.info("🔀 Router initialized - All routes registered")
    
    def _register_handlers(self):
        """Register all message and callback handlers"""
        
        # ============ COMMAND HANDLERS ============
        
        @self.bot.message_handler(commands=['start'])
        def start(message):
            logger.info(f"📩 /start from {message.from_user.id}")
            self.commands.handle_start(message)
        
        @self.bot.message_handler(commands=['help'])
        def help(message):
            logger.info(f"📩 /help from {message.from_user.id}")
            self.commands.handle_help(message)
        
        @self.bot.message_handler(commands=['cancel'])
        def cancel(message):
            logger.info(f"📩 /cancel from {message.from_user.id}")
            self.commands.handle_cancel(message)
        
        @self.bot.message_handler(commands=['restore'])
        def restore(message):
            logger.info(f"📩 /restore from {message.from_user.id}")
            self.commands.handle_restore(message)
        
        # ============ MAIN MENU HANDLERS ============
        
        @self.bot.message_handler(func=lambda m: m.text == "📚 Dir Waydiin")
        def dir_waydiin(message):
            logger.info(f"📩 Dir Waydiin from {message.from_user.id}")
            self.waydiin.handle_dir_waydiin(message)
        
        @self.bot.message_handler(func=lambda m: m.text == "🌐 Hel Waydiin")
        def hel_waydiin(message):
            logger.info(f"📩 Hel Waydiin from {message.from_user.id}")
            self.hel.handle_hel_waydiin(message)
        
        @self.bot.message_handler(func=lambda m: m.text == "❓ Help")
        def help_button(message):
            logger.info(f"📩 Help button from {message.from_user.id}")
            self.commands.handle_help(message)
        
        # ============ RESTORE RESPONSE ============
        
        @self.bot.message_handler(func=lambda m: m.text in ["✅ Yes, Restore", "❌ No, Continue"])
        def restore_response(message):
            logger.info(f"📩 Restore response from {message.from_user.id}: {message.text}")
            self.commands.handle_restore_response(message)
        
        # ============ CATCH-ALL: Route by State ============
        
        @self.bot.message_handler(func=lambda m: True)
        def route_by_state(message):
            self._route_message(message)
    
    def _route_message(self, message):
        """Route message based on user's current state"""
        user_id = message.from_user.id
        text = message.text or ""
        
        logger.info(f"🔄 Routing message from {user_id}: '{text[:30]}...'")
        
        # Check if banned
        if self.status.is_banned(user_id):
            self.bot.send_message(user_id, Messages.banned())
            return
        
        # Get current state
        state = self.status.get_state(user_id)
        current_status = state['status']
        
        logger.info(f"📍 User {user_id} state: {current_status}")
        
        # Route based on state
        if current_status == 'idle':
            self.bot.send_message(
                user_id,
                Messages.idle_message(),
                reply_markup=Keyboard.main_menu()
            )
        
        elif current_status == 'awaiting_place':
            self.waydiin.handle_place(message)
        
        elif current_status == 'awaiting_class':
            self.waydiin.handle_class(message)
        
        elif current_status == 'awaiting_subject':
            self.waydiin.handle_subject(message)
        
        elif current_status == 'awaiting_question':
            self.waydiin.handle_question(message)
        
        elif current_status == 'awaiting_confirmation':
            self.waydiin.handle_confirmation(message)
        
        else:
            # Unknown state - reset
            logger.warning(f"⚠️ Unknown state {current_status} for user {user_id}")
            self.status.clear_state(user_id)
            self.bot.send_message(
                user_id,
                "⚠️ Something went wrong. Please start over.",
                reply_markup=Keyboard.main_menu()
            )
    
    def get_handlers(self):
        """Return all handlers (for testing/debugging)"""
        return {
            'commands': self.commands,
            'waydiin': self.waydiin,
            'hel': self.hel
        }