import json

class StatusManager:
    """Database-based status manager"""
    
    def __init__(self, db):
        self.db = db
    
    def get_state(self, user_id):
        """Get user's status and data from database"""
        result = self.db.get_user_flow(user_id)
        
        if result:
            return {
                'status': result['flow_status'] or 'idle',
                'data': json.loads(result['flow_data']) if result['flow_data'] else {}
            }
        
        self.db.create_user(user_id)
        return {'status': 'idle', 'data': {}}
    
    def set_state(self, user_id, status, data=None):
        """Set user's status and data"""
        data_json = json.dumps(data) if data else None
        self.db.set_user_flow(user_id, status, data_json)
    
    def update_data(self, user_id, data):
        """Update only the data field"""
        current = self.get_state(user_id)
        current_data = current.get('data', {})
        current_data.update(data)
        
        # ✅ FIX: Use set_state to save properly
        self.set_state(user_id, current['status'], current_data)
    
    def clear_state(self, user_id):
        """Clear user's flow (reset to idle)"""
        self.db.clear_user_flow(user_id)
    
    def get_data(self, user_id):
        """Get only the data"""
        state = self.get_state(user_id)
        return state.get('data', {})
    
    def is_banned(self, user_id):
        """Check if user is banned"""
        return self.db.is_user_banned(user_id)
    
    def is_active(self, user_id):
        """Check if user has active operation"""
        state = self.get_state(user_id)
        return state['status'] != 'idle'