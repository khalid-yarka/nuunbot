import json
from database.connection import DatabaseConnection

class Database:
    """All database operations"""
    
    def __init__(self, db_path='database.db'):
        self.db = DatabaseConnection(db_path)
    
    # ============ USER OPERATIONS ============
    
    def create_user(self, user_id):
        """Create user if not exists"""
        with self.db.get_connection() as conn:
            conn.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
            conn.commit()
    
    def get_user_flow(self, user_id):
        """Get user's flow status and data"""
        with self.db.get_connection() as conn:
            result = conn.execute(
                'SELECT flow_status, flow_data FROM users WHERE user_id = ?',
                (user_id,)
            ).fetchone()
            return dict(result) if result else None
    
    def set_user_flow(self, user_id, status, data=None):
        """Set user's flow status and data"""
        with self.db.get_connection() as conn:
            conn.execute(
                'UPDATE users SET flow_status = ?, flow_data = ? WHERE user_id = ?',
                (status, data, user_id)
            )
            conn.commit()
    
    def clear_user_flow(self, user_id):
        """Clear user's flow (reset to idle)"""
        with self.db.get_connection() as conn:
            conn.execute(
                'UPDATE users SET flow_status = "idle", flow_data = NULL WHERE user_id = ?',
                (user_id,)
            )
            conn.commit()
    
    def is_user_banned(self, user_id):
        """Check if user is banned"""
        with self.db.get_connection() as conn:
            result = conn.execute(
                'SELECT status FROM users WHERE user_id = ?',
                (user_id,)
            ).fetchone()
            return result and result['status'] == 'banned'
    
    # ============ QUESTION OPERATIONS ============
    
    def save_question(self, user_id, place, class_name, subject, question_text):
        """Save question to database"""
        with self.db.get_connection() as conn:
            cursor = conn.execute('''
                INSERT INTO questions (user_id, place, class, subject, question_text)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, place, class_name, subject, question_text))
            conn.commit()
            return cursor.lastrowid
    
    def get_question(self, question_id):
        """Get question by ID"""
        with self.db.get_connection() as conn:
            result = conn.execute(
                'SELECT * FROM questions WHERE id = ?',
                (question_id,)
            ).fetchone()
            return dict(result) if result else None
    
    def update_question_status(self, question_id, status, channel_message_id=None):
        """Update question status"""
        with self.db.get_connection() as conn:
            if channel_message_id:
                conn.execute('''
                    UPDATE questions 
                    SET status = ?, posted_at = CURRENT_TIMESTAMP, channel_message_id = ?
                    WHERE id = ?
                ''', (status, channel_message_id, question_id))
            else:
                conn.execute('''
                    UPDATE questions SET status = ? WHERE id = ?
                ''', (status, question_id))
            conn.commit()
    
    def get_last_question_time(self, user_id):
        """Get last question time for rate limiting"""
        with self.db.get_connection() as conn:
            result = conn.execute('''
                SELECT created_at FROM questions 
                WHERE user_id = ? 
                ORDER BY created_at DESC LIMIT 1
            ''', (user_id,)).fetchone()
            return result['created_at'] if result else None