class TextBase:
    """Base text templates with borders and footers"""
    
    # Borders
    BORDER_TOP = "࿇═════════════════════════࿇"
    BORDER_BOTTOM = "࿇═════════════════════════࿇"
    
    # Footers
    FOOTERS = {
        'welcome': 'Soo Dhawoow',
        'menu': 'Soo Dhawoow',
        'place': 'Xulo Goobta',
        'class': 'Xulo Fasalka',
        'subject': 'Xulo Maadada',
        'question': 'Soo Dir Su\'aasha',
        'preview': 'Hubi Su\'aasha',
        'post': 'Ku Darso Jaawaabtaada',
        'success': 'Waa Lagu Guulaystay',
        'error': 'Isku Day Mar Kale',
        'cancel': 'La Joojiyey',
        'help': 'Caawimaad',
        'restore': 'Soo Celinta',
        'invalid': 'Isku Day Mar Kale'
    }
    
    @classmethod
    def footer(cls, key):
        """Get footer text by key"""
        return f"└────{cls.FOOTERS.get(key, '')}──────"