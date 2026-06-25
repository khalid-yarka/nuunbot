from datetime import datetime

class Formatters:
    """Data formatters"""
    
    @classmethod
    def format_time(cls, timestamp=None):
        """Format time for display"""
        if timestamp:
            if isinstance(timestamp, str):
                try:
                    dt = datetime.fromisoformat(timestamp)
                except:
                    dt = datetime.now()
            else:
                dt = timestamp
        else:
            dt = datetime.now()
        
        return dt.strftime("%d/%m/%Y at %I:%M %p")
    
    @classmethod
    def truncate_text(cls, text, max_length=50):
        """Truncate text with ellipsis"""
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."
    
    @classmethod
    def format_place_display(cls, flag, name):
        """Format place for display"""
        return f"{flag} {name}"
    
    @classmethod
    def get_user_display_name(cls, user):
        """Get user's display name"""
        if user.username:
            return f"@{user.username}"
        if user.first_name and user.last_name:
            return f"{user.first_name} {user.last_name}"
        return user.first_name or "User"