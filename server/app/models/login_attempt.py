"""
LoginAttempt model for tracking failed login attempts.
"""
from datetime import datetime
from app import db


class LoginAttempt(db.Model):
    """LoginAttempt model for tracking login attempts."""
    
    __tablename__ = 'login_attempts'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # User Reference
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Attempt Information
    ip_address = db.Column(db.String(45), nullable=True)  # IPv6 can be up to 45 chars
    user_agent = db.Column(db.String(255), nullable=True)
    success = db.Column(db.Boolean, nullable=False)
    failure_reason = db.Column(db.String(100), nullable=True)  # 'wrong_password', 'wrong_email', 'account_locked'
    
    # Timestamp
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __init__(self, user_id, success, ip_address=None, user_agent=None, failure_reason=None):
        """Initialize a new login attempt record."""
        self.user_id = user_id
        self.success = success
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.failure_reason = failure_reason
    
    def to_dict(self):
        """Convert login attempt object to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'success': self.success,
            'failure_reason': self.failure_reason,
            'attempted_at': self.attempted_at.isoformat() if self.attempted_at else None
        }
    
    @staticmethod
    def get_recent_failed_attempts(user_id, minutes=1):
        """Get count of recent failed login attempts for a user."""
        from datetime import timedelta
        time_threshold = datetime.utcnow() - timedelta(minutes=minutes)
        
        return LoginAttempt.query.filter(
            LoginAttempt.user_id == user_id,
            LoginAttempt.success == False,
            LoginAttempt.attempted_at >= time_threshold
        ).count()
    
    @staticmethod
    def clear_failed_attempts(user_id):
        """Clear all failed login attempts for a user."""
        LoginAttempt.query.filter(
            LoginAttempt.user_id == user_id,
            LoginAttempt.success == False
        ).delete()
        db.session.commit()
    
    def __repr__(self):
        """String representation of LoginAttempt."""
        status = 'SUCCESS' if self.success else 'FAILED'
        return f'<LoginAttempt {self.user_id} - {status} at {self.attempted_at}>'