from utils.validators import Validators
from utils.formatters import Formatters
from keyboard import Keyboard
from utils.logger import logger

class HandlerFunctions:
    """Shared helper functions for handlers"""
    
    def __init__(self, bot, db, status, config):
        self.bot = bot
        self.db = db
        self.status = status
        self.config = config
    
    def get_user_state(self, user_id):
        return self.status.get_state(user_id)
    
    def clear_user_state(self, user_id):
        self.status.clear_state(user_id)
    
    def save_question(self, user_id, place, class_name, subject, question_text):
        return self.db.save_question(user_id, place, class_name, subject, question_text)
    
    def post_to_channel(self, channel_id, place_flag, place_name, class_name, subject, question_text):
        time = Formatters.format_time()
        from text.messages import Messages
        post_text = Messages.channel_post(
            place_flag, place_name, class_name, subject, question_text, time
        )
        return self.bot.send_message(channel_id, post_text, parse_mode='HTML')
    
    def validate_question(self, text):
        return Validators.validate_question(text)
    
    def is_rate_limited(self, user_id):
        last_time = self.db.get_last_question_time(user_id)
        return Validators.is_rate_limited(last_time, self.config.RATE_LIMIT_SECONDS)
    
    def get_place_info(self, button_text):
        return Keyboard.get_place_info(button_text)
    
    def get_place_flag(self, place):
        return Keyboard.get_place_flag(place)
    
    def get_place_name(self, place):
        return Keyboard.get_place_name(place)
    
    def get_subjects(self, class_name):
        return Keyboard.get_subjects(class_name)
    
    def is_valid_place(self, place):
        return Validators.is_valid_place(place)
    
    def is_valid_class(self, class_name):
        return Validators.is_valid_class(class_name)
    
    def is_valid_subject(self, class_name, subject):
        """Check if subject is valid for class - with logging"""
        class_name = class_name.strip() if class_name else ''
        subject = subject.strip() if subject else ''
        
        # Get class_subjects from Keyboard
        class_subjects = Keyboard.CLASS_SUBJECTS
        
        # Debug logging
        logger.info(f"🔍 is_valid_subject: class='{class_name}', subject='{subject}'")
        logger.info(f"📋 Available for {class_name}: {class_subjects.get(class_name, [])}")
        
        result = Validators.is_valid_subject(class_name, subject, class_subjects)
        logger.info(f"✅ Result: {result}")
        
        return result
    
    def get_user_display_name(self, user):
        return Formatters.get_user_display_name(user)
    
    def format_time(self, timestamp=None):
        return Formatters.format_time(timestamp)
    
    def truncate_text(self, text, max_length=50):
        return Formatters.truncate_text(text, max_length)
    
    def is_banned(self, user_id):
        return self.status.is_banned(user_id)
    
    def is_active(self, user_id):
        return self.status.is_active(user_id)