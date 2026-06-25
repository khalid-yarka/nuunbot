import sqlite3
import json
from contextlib import contextmanager

class DatabaseConnection:
    """SQLite3 connection manager"""
    
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database with required tables"""
        with self.get_connection() as conn:
            # Users table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    status TEXT DEFAULT 'active',
                    flow_status TEXT DEFAULT 'idle',
                    flow_data TEXT
                )
            ''')
            
            # Questions table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    place TEXT NOT NULL,
                    class TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    question_text TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    posted_at TIMESTAMP,
                    channel_message_id INTEGER
                )
            ''')
            
            # Indexes
            conn.execute('CREATE INDEX IF NOT EXISTS idx_user_flow_status ON users(user_id, flow_status)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_question_status ON questions(status)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_place_class_subject ON questions(place, class, subject)')
            
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()