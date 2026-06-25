from text.messages import Messages
from keyboard import Keyboard
from handlers.functions import HandlerFunctions

class CommandHandler:
    """Handle /start, /help, /cancel, /restore commands"""
    
    def __init__(self, bot, db, status, config):
        self.bot = bot
        self.db = db
        self.status = status
        self.config = config
        self.functions = HandlerFunctions(bot, db, status, config)
    
    def handle_start(self, message):
        """Handle /start command"""
        user_id = message.from_user.id
        first_name = message.from_user.first_name or "User"
        
        # Clear any existing state
        self.status.clear_state(user_id)
        
        # Send welcome message
        self.bot.send_message(
            user_id,
            Messages.main_menu(first_name),
            parse_mode='HTML',
            reply_markup=Keyboard.main_menu()
        )
    
    def handle_help(self, message):
        """Handle /help command"""
        self.bot.send_message(
            message.chat.id,
            Messages.help_menu(),
            parse_mode='HTML',
            reply_markup=Keyboard.main_menu()
        )
    
    def handle_cancel(self, message):
        """Handle /cancel command"""
        user_id = message.from_user.id
        
        # Clear state
        self.status.clear_state(user_id)
        
        # Send cancel message
        self.bot.send_message(
            user_id,
            Messages.cancel(),
            parse_mode='HTML',
            reply_markup=Keyboard.main_menu()
        )
    
    def handle_restore(self, message):
        """Handle /restore command"""
        user_id = message.from_user.id
        
        # Check if user has active operation
        if not self.status.is_active(user_id):
            self.bot.send_message(
                user_id,
                Messages.restore_no_active(),
                reply_markup=Keyboard.main_menu()
            )
            return
        
        # Get current data
        state = self.status.get_state(user_id)
        data = state.get('data', {})
        
        # Show confirmation
        confirm_text = Messages.restore_confirmation(
            data.get('place'),
            data.get('class'),
            data.get('subject'),
            data.get('question')
        )
        
        self.bot.send_message(
            user_id,
            confirm_text,
            parse_mode='HTML',
            reply_markup=Keyboard.restore_confirmation()
        )
    
    def handle_restore_response(self, message):
        """Handle restore confirmation response"""
        user_id = message.from_user.id
        
        if message.text == "✅ Yes, Restore":
            self.status.clear_state(user_id)
            self.bot.send_message(
                user_id,
                Messages.restore_success(),
                reply_markup=Keyboard.main_menu()
            )
        elif message.text == "❌ No, Continue":
            self.bot.send_message(
                user_id,
                Messages.restore_continue(),
                reply_markup=Keyboard.main_menu()
            )
        else:
            self.bot.send_message(
                user_id,
                Messages.invalid_selection(),
                reply_markup=Keyboard.main_menu()
            )