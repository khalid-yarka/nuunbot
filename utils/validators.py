import re
import time
from datetime import datetime

class Validators:
    """Input validators"""
    
    @classmethod
    def validate_question(cls, text):
        """Validate question text"""
        errors = []
        
        if not text or not text.strip():
            errors.append("Question cannot be empty")
            return errors
        
        if len(text.strip()) < 10:
            errors.append("Question too short (minimum 10 characters)")
        
        if len(text.strip()) > 1000:
            errors.append("Question too long (maximum 1000 characters)")
        
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+])+'
        if re.search(url_pattern, text):
            errors.append("Links are not allowed")
        
        if 't.me' in text.lower() or 'telegram.me' in text.lower():
            errors.append("Telegram links are not allowed")
        
        if len(text) > 0:
            caps = sum(1 for c in text if c.isupper())
            if caps / len(text) > 0.5:
                errors.append("Please don't use excessive CAPS")
        
        return errors
    
    @classmethod
    def is_rate_limited(cls, last_question_time, limit_seconds=60):
        """Check if user is rate limited"""
        if not last_question_time:
            return False
        
        if isinstance(last_question_time, str):
            try:
                last_time = datetime.fromisoformat(last_question_time).timestamp()
            except:
                return False
        else:
            last_time = last_question_time
        
        elapsed = time.time() - last_time
        return elapsed < limit_seconds
    
    @classmethod
    def is_valid_place(cls, place):
        """Check if place is valid"""
        valid_places = ['SL', 'SOM', 'PL', 'ALL']
        place = place.strip() if place else ''
        return place in valid_places
    
    @classmethod
    def is_valid_class(cls, class_name):
        """Check if class is valid"""
        valid_classes = ['7aad', '8aad', 'Sare 3aad', 'Sare 4aad']
        class_name = class_name.strip() if class_name else ''
        return class_name in valid_classes
    
    @classmethod
    def is_valid_subject(cls, class_name, subject, class_subjects):
        """Check if subject is valid for the class"""
        subjects = class_subjects.get(class_name, [])
        
        # Clean both values
        subject = subject.strip() if subject else ''
        class_name = class_name.strip() if class_name else ''
        
        # Debug: Log what we're comparing
        print(f"🔍 Validating: class='{class_name}', subject='{subject}'")
        print(f"📋 Available subjects: {subjects}")
        
        # Check if subject exists (with strip)
        return any(s.strip() == subject for s in subjects)