from telebot import types

class Keyboard:
    """All reply keyboards"""
    
    # Place mapping
    PLACE_FLAGS = {
        'SL': '🇮🇷',
        'SOM': '🇸🇴',
        'PL': '🇸🇱',
        'ALL': '🌍'
    }
    
    PLACE_NAMES = {
        'SL': 'Somaliland',
        'SOM': 'Somalia',
        'PL': 'Puntland',
        'ALL': 'All Places'
    }
    
    # Class-subject mapping
    CLASS_SUBJECTS = {
        '7aad': ['Baro', 'Xisaab', 'Physics', 'Chemistry', 'Biology', 'History', 'Geography'],
        '8aad': ['Baro', 'Xisaab', 'Physics', 'Chemistry', 'Biology', 'History', 'Geography'],
        'Sare 3aad': ['Baro', 'Xisaab', 'Physics', 'Chemistry', 'Biology', 'History', 'Geography', 'Logic'],
        'Sare 4aad': ['Baro', 'Xisaab', 'Physics', 'Chemistry', 'Biology', 'History', 'Geography', 'Logic']
    }
    
    @classmethod
    def main_menu(cls):
        """Main menu keyboard"""
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        keyboard.add(
            types.KeyboardButton("📚 Dir Waydiin"),
            types.KeyboardButton("🌐 Hel Waydiin")
        )
        keyboard.add(types.KeyboardButton("❓ Help"))
        return keyboard
    
    @classmethod
    def place_selection(cls):
        """Place selection keyboard"""
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(
            types.KeyboardButton("🇮🇷 SL"),
            types.KeyboardButton("🇸🇴 SOM")
        )
        keyboard.add(
            types.KeyboardButton("🇸🇱 PL"),
            types.KeyboardButton("🌍 ALL")
        )
        keyboard.add(types.KeyboardButton("❌ Cancel"))
        return keyboard
    
    @classmethod
    def class_selection(cls):
        """Class selection keyboard"""
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(
            types.KeyboardButton("7aad"),
            types.KeyboardButton("8aad")
        )
        keyboard.add(
            types.KeyboardButton("Sare 3aad"),
            types.KeyboardButton("Sare 4aad")
        )
        keyboard.add(types.KeyboardButton("❌ Cancel"))
        return keyboard
    
    @classmethod
    def subject_selection(cls, class_name):
        """Dynamic subject selection based on class"""
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        
        subjects = cls.CLASS_SUBJECTS.get(class_name, [])
        row = []
        for subject in subjects:
            row.append(types.KeyboardButton(subject))
            if len(row) == 2:
                keyboard.add(*row)
                row = []
        if row:
            keyboard.add(*row)
        
        keyboard.add(types.KeyboardButton("❌ Cancel"))
        return keyboard
    
    @classmethod
    def confirmation(cls):
        """Confirmation keyboard"""
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(
            types.KeyboardButton("✅ Dir"),
            types.KeyboardButton("❌ Cancel")
        )
        return keyboard
    
    @classmethod
    def restore_confirmation(cls):
        """Restore confirmation keyboard"""
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(
            types.KeyboardButton("✅ Yes, Restore"),
            types.KeyboardButton("❌ No, Continue")
        )
        return keyboard
    
    @classmethod
    def get_place_info(cls, button_text):
        """Extract place tag from button text"""
        # Button text: "🇮🇷 SL" -> "SL"
        parts = button_text.strip().split()
        return parts[-1] if parts else None
    
    @classmethod
    def get_place_flag(cls, place):
        """Get flag for place"""
        return cls.PLACE_FLAGS.get(place, '')
    
    @classmethod
    def get_place_name(cls, place):
        """Get name for place"""
        return cls.PLACE_NAMES.get(place, place)
    
    @classmethod
    def get_subjects(cls, class_name):
        """Get subjects for a class"""
        return cls.CLASS_SUBJECTS.get(class_name, [])