from text.messages import Messages
from keyboard import Keyboard
from handlers.functions import HandlerFunctions
from utils.logger import logger

class WaydiinHandler:
    """Handle Dir Waydiin flow"""
    
    def __init__(self, bot, db, status, config):
        self.bot = bot
        self.db = db
        self.status = status
        self.config = config
        self.functions = HandlerFunctions(bot, db, status, config)
    
    def handle_dir_waydiin(self, message):
        """Start Dir Waydiin flow"""
        user_id = message.from_user.id
        
        if self.functions.is_banned(user_id):
            self.bot.send_message(user_id, Messages.banned())
            return
        
        self.status.clear_state(user_id)
        self.status.set_state(user_id, 'awaiting_place')
        
        self.bot.send_message(
            user_id,
            Messages.place_selection(),
            parse_mode='HTML',
            reply_markup=Keyboard.place_selection()
        )
    
    def handle_place(self, message):
        """Handle place selection"""
        user_id = message.from_user.id
        text = message.text.strip()
        
        if text == "❌ Cancel":
            self.status.clear_state(user_id)
            self.bot.send_message(user_id, Messages.cancel(), parse_mode='HTML', reply_markup=Keyboard.main_menu())
            return
        
        place = self.functions.get_place_info(text)
        
        if not place or not self.functions.is_valid_place(place):
            self.bot.send_message(user_id, Messages.invalid_selection(), reply_markup=Keyboard.place_selection())
            return
        
        # ✅ Save place
        current_data = self.status.get_data(user_id)
        current_data['place'] = place
        self.status.set_state(user_id, 'awaiting_class', current_data)
        
        # 🔍 DEBUG
        logger.info(f"✅ Place saved: {current_data}")
        
        self.bot.send_message(
            user_id,
            Messages.class_selection(),
            parse_mode='HTML',
            reply_markup=Keyboard.class_selection()
        )
    
    def handle_class(self, message):
        """Handle class selection"""
        user_id = message.from_user.id
        text = message.text.strip()
        
        if text == "❌ Cancel":
            self.status.clear_state(user_id)
            self.bot.send_message(user_id, Messages.cancel(), parse_mode='HTML', reply_markup=Keyboard.main_menu())
            return
        
        class_name = text
        
        if not self.functions.is_valid_class(class_name):
            self.bot.send_message(user_id, Messages.invalid_selection(), reply_markup=Keyboard.class_selection())
            return
        
        # ✅ FIX: Get existing data first, then update
        current_data = self.status.get_data(user_id)
        current_data['class'] = class_name
        
        # ✅ Use set_state to ensure data is saved properly
        self.status.set_state(user_id, 'awaiting_subject', current_data)
        
        # 🔍 DEBUG: Verify it's saved
        debug_data = self.status.get_data(user_id)
        logger.info(f"✅ Class saved: {debug_data}")
        
        self.bot.send_message(
            user_id,
            Messages.subject_selection(class_name),
            parse_mode='HTML',
            reply_markup=Keyboard.subject_selection(class_name)
        )
    
    def handle_subject(self, message):
        """Handle subject selection"""
        user_id = message.from_user.id
        text = message.text.strip()
        
        if text == "❌ Cancel":
            self.status.clear_state(user_id)
            self.bot.send_message(user_id, Messages.cancel(), parse_mode='HTML', reply_markup=Keyboard.main_menu())
            return
        
        subject = text
        data = self.status.get_data(user_id)
        class_name = data.get('class', '').strip()
        place = data.get('place', '')
        
        # 🔍 DEBUG LOGGING
        logger.info(f"📝 Subject selected: '{subject}'")
        logger.info(f"📚 Class from data: '{class_name}'")
        logger.info(f"📋 Full data: {data}")
        
        # Validate subject
        is_valid = self.functions.is_valid_subject(class_name, subject)
        logger.info(f"✅ Is valid? {is_valid}")
        
        if not is_valid:
            logger.warning(f"❌ Invalid subject '{subject}' for class '{class_name}'")
            self.bot.send_message(
                user_id,
                Messages.invalid_selection(),
                reply_markup=Keyboard.subject_selection(class_name)
            )
            return
        
        # ✅ Save subject
        current_data = self.status.get_data(user_id)
        current_data['subject'] = subject
        self.status.set_state(user_id, 'awaiting_question', current_data)
        
        self.bot.send_message(
            user_id,
            Messages.question_prompt(place, class_name, subject),
            parse_mode='HTML'
        )
    
    def handle_question(self, message):
        """Handle question text"""
        user_id = message.from_user.id
        question_text = message.text.strip()
        
        if question_text == "❌ Cancel":
            self.status.clear_state(user_id)
            self.bot.send_message(user_id, Messages.cancel(), parse_mode='HTML', reply_markup=Keyboard.main_menu())
            return
        
        errors = self.functions.validate_question(question_text)
        if errors:
            self.bot.send_message(user_id, Messages.validation_errors(errors), parse_mode='HTML')
            return
        
        if self.functions.is_rate_limited(user_id):
            self.bot.send_message(user_id, "⏳ Please wait 1 minute before sending another question.")
            return
        
        data = self.status.get_data(user_id)
        place = data.get('place')
        class_name = data.get('class')
        subject = data.get('subject')
        
        question_id = self.functions.save_question(user_id, place, class_name, subject, question_text)
        
        # ✅ Save question data
        current_data = self.status.get_data(user_id)
        current_data['question'] = question_text
        current_data['question_id'] = question_id
        self.status.set_state(user_id, 'awaiting_confirmation', current_data)
        
        place_flag = self.functions.get_place_flag(place)
        place_name = self.functions.get_place_name(place)
        
        preview_text = Messages.preview(place_flag, place_name, class_name, subject, question_text)
        
        self.bot.send_message(
            user_id,
            preview_text,
            parse_mode='HTML',
            reply_markup=Keyboard.confirmation()
        )
    
    def handle_confirmation(self, message):
        """Handle confirmation (Dir / Cancel)"""
        user_id = message.from_user.id
        text = message.text.strip()
        
        if text == "✅ Dir":
            data = self.status.get_data(user_id)
            place = data.get('place')
            class_name = data.get('class')
            subject = data.get('subject')
            question_text = data.get('question')
            question_id = data.get('question_id')
            
            try:
                place_flag = self.functions.get_place_flag(place)
                place_name = self.functions.get_place_name(place)
                
                sent_message = self.functions.post_to_channel(
                    self.config.CHANNEL_ID,
                    place_flag, place_name, class_name, subject, question_text
                )
                
                self.db.update_question_status(question_id, 'posted', sent_message.message_id)
                self.status.clear_state(user_id)
                
                self.bot.send_message(
                    user_id,
                    Messages.success(class_name, subject),
                    parse_mode='HTML',
                    reply_markup=Keyboard.main_menu()
                )
                
            except Exception as e:
                self.bot.send_message(
                    user_id,
                    f"❌ Error posting to channel: {str(e)}",
                    reply_markup=Keyboard.main_menu()
                )
        
        elif text == "❌ Cancel":
            data = self.status.get_data(user_id)
            question_id = data.get('question_id')
            if question_id:
                self.db.update_question_status(question_id, 'cancelled')
            
            self.status.clear_state(user_id)
            self.bot.send_message(user_id, Messages.cancel(), parse_mode='HTML', reply_markup=Keyboard.main_menu())
        
        else:
            self.bot.send_message(user_id, Messages.invalid_selection(), reply_markup=Keyboard.confirmation())