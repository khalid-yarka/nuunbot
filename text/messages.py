from text.base import TextBase

class Messages(TextBase):
    """All bot messages"""
    
    @classmethod
    def main_menu(cls, first_name):
        return f"""
{cls.BORDER_TOP}
┃┌─〔 🏫 NUUN BOT 〕
┃
┃  ✦ Welcome, {first_name}!
┃  
┃  ➩ 📚 Dir Waydiin
┃    • Ask questions for your class
┃    • Posted to channel
┃  
┃  ➩ 🌐 Hel Waydiin
┃    • Open Nuun Quiz
┃  
┃  ✧ Choose an option below
┃
┃{cls.footer('menu')}
{cls.BORDER_BOTTOM}
"""
    
    @classmethod
    def place_selection(cls):
        return f"""
{cls.BORDER_TOP}
┃┌─〔 📍 SELECT PLACE 〕
┃
┃  ✦ Choose your place:
┃  
┃  ✧ Tap a button below
┃
┃{cls.footer('place')}
{cls.BORDER_BOTTOM}
"""
    
    @classmethod
    def class_selection(cls):
        return f"""
{cls.BORDER_TOP}
┃┌─〔 📚 SELECT CLASS 〕
┃
┃  ✦ Choose your class:
┃  
┃  ✧ Tap a button below
┃
┃{cls.footer('class')}
{cls.BORDER_BOTTOM}
"""
    
    @classmethod
    def subject_selection(cls, class_name):
        return f"""
{cls.BORDER_TOP}
┃┌─〔 📖 SELECT SUBJECT 〕
┃
┃  ✦ Class: {class_name}
┃  
┃  ✧ Tap a subject below
┃
┃{cls.footer('subject')}
{cls.BORDER_BOTTOM}
"""
    
    @classmethod
    def question_prompt(cls, place, class_name, subject):
        return f"""
{cls.BORDER_TOP}
┃┌─〔 ✍️ SEND QUESTION 〕
┃
┃  ✦ Place: {place}
┃  ✦ Class: {class_name}
┃  ✦ Subject: {subject}
┃  
┃  ──────────────────────
┃  ✧ Type your question below
┃  ✧ Min 10 characters
┃  ✧ Max 1000 characters
┃  ──────────────────────
┃  
┃  ✧ Send your question now
┃
┃{cls.footer('question')}
{cls.BORDER_BOTTOM}
"""
    
    @classmethod
    def preview(cls, place_flag, place_name, class_name, subject, question_text):
        return f"""
{cls.BORDER_TOP}
┃┌─〔 📝 PREVIEW 〕
┃
┃  ┌────────────────────┐
┃  │ 📍 Place    : {place_flag} {place_name}
┃  │ 📖 Class    : {class_name}
┃  │ 📚 Subject  : {subject}
┃  └────────────────────┘
┃  
┃  ──────────────────────
┃  💬 "{question_text}"
┃  ──────────────────────
┃  
┃  ✧ This is how it will look
┃  ✧ Click "Dir" to post
┃  ✧ Click "Cancel" to discard
┃
┃{cls.footer('preview')}
{cls.BORDER_BOTTOM}
"""
    
    @classmethod
    def channel_post(cls, place_flag, place_name, class_name, subject, question_text, time):
        return f"""
{cls.BORDER_TOP}
┃┌─〔 📚 NEW QUESTION 〕
┃
┃  ┌────────────────────┐
┃  │ 📍 Place    : {place_flag} {place_name}
┃  │ 📖 Class    : {class_name}
┃  │ 📚 Subject  : {subject}
┃  └────────────────────┘
┃  
┃  ──────────────────────
┃  💬 "{question_text}"
┃  ──────────────────────
┃  
┃  ✧ Posted: {time}
┃
┃{cls.footer('post')}
{cls.BORDER_BOTTOM}
"""
    
    @classmethod
    def success(cls, class_name, subject):
        return f"""
{cls.BORDER_TOP}
┃┌─〔 ✅ POSTED! 〕
┃
┃  ✦ Your question was posted!
┃  
┃  ┌────────────────────┐
┃  │ 📖 Class    : {class_name}
┃  │ 📚 Subject  : {subject}
┃  └────────────────────┘
┃  
┃  ✧ Click "Dir Waydiin" for more
┃
┃{cls.footer('success')}
{cls.BORDER_BOTTOM}
"""
    
    @classmethod
    def validation_errors(cls, errors):
        error_list = "\n  ".join(f"• {e}" for e in errors)
        return f"""
{cls.BORDER_TOP}
┃┌─〔 ❌ ERROR 〕
┃
┃  ✦ Please fix the following:
┃  
┃  ──────────────────────
┃  {error_list}
┃  ──────────────────────
┃  
┃  ✧ Try again with corrections
┃  ✧ Use /cancel to stop
┃
┃{cls.footer('error')}
{cls.BORDER_BOTTOM}
"""
    
    @classmethod
    def cancel(cls):
        return f"""
{cls.BORDER_TOP}
┃┌─〔 ❌ CANCELLED 〕
┃
┃  ✦ Operation cancelled
┃  
┃  ✧ Start over with "Dir Waydiin"
┃  ✧ /help for commands
┃
┃{cls.footer('cancel')}
{cls.BORDER_BOTTOM}
"""
    
    @classmethod
    def help_menu(cls):
        return f"""
{cls.BORDER_TOP}
┃┌─〔 📚 HELP 〕
┃
┃  ➩ /start
┃    • Show main menu
┃  
┃  ➩ /help
┃    • Show this menu
┃  
┃  ➩ /cancel
┃    • Cancel operation
┃  
┃  ➩ /restore
┃    • Clear active session
┃  
┃  ──────────────────────
┃  ✧ Click "Dir Waydiin" to ask
┃  ✧ Click "Hel Waydiin" for quiz
┃
┃{cls.footer('help')}
{cls.BORDER_BOTTOM}
"""
    
    @classmethod
    def hel_message(cls):
        return f"""
{cls.BORDER_TOP}
┃┌─〔 🌐 NUUN QUIZ 〕
┃
┃  ✦ Welcome to Nuun Quiz!
┃  
┃  ✧ Test your knowledge with
┃    interactive quizzes
┃  ✧ Place-based questions
┃  ✧ Multiple quiz modes
┃  
┃  ──────────────────────
┃  Click the button below
┃  to open the quiz app
┃  ──────────────────────
┃
┃{cls.footer('welcome')}
{cls.BORDER_BOTTOM}
"""
    
    @classmethod
    def idle_message(cls):
        return """
Please use the buttons below or /help for commands.
"""
    
    @classmethod
    def invalid_selection(cls):
        return f"""
{cls.BORDER_TOP}
┃┌─〔 ❌ INVALID 〕
┃
┃  ✦ Invalid selection
┃  
┃  ✧ Please use the buttons below
┃  ✧ /cancel to stop
┃
┃{cls.footer('invalid')}
{cls.BORDER_BOTTOM}
"""
    
    @classmethod
    def restore_no_active(cls):
        return "ℹ️ You have no active operation to restore."
    
    @classmethod
    def restore_confirmation(cls, place, class_name, subject, question):
        question_preview = question[:50] + "..." if question and len(question) > 50 else question or "Not sent yet"
        return f"""
⚠️ **You have an active operation:**

📍 Place: {place or 'Not selected'}
📖 Class: {class_name or 'Not selected'}
📚 Subject: {subject or 'Not selected'}
💬 Question: "{question_preview}"

Are you sure you want to cancel and start over?
"""
    
    @classmethod
    def restore_success(cls):
        return "✅ Your session has been restored. You can start a new operation."
    
    @classmethod
    def restore_continue(cls):
        return "✅ Continuing your current operation."
    
    @classmethod
    def banned(cls):
        return "🚫 You are banned from using this bot."