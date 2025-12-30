"""
Rating model for flight reviews.
"""
from datetime import datetime
from app import db


class Rating(db.Model):
    """Rating model for flight ratings (1-5 stars)."""
    
    __tablename__ = 'ratings'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Flight Reference
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False, index=True)
    
    # User Reference (from Server DB)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    
    # Rating (1-5)
    rating = db.Column(db.Integer, nullable=False)
    
    # Optional Comment
    comment = db.Column(db.Text, nullable=True)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Unique constraint: one rating per user per flight
    __table_args__ = (
        db.UniqueConstraint('flight_id', 'user_id', name='unique_flight_user_rating'),
    )
    
    def __init__(self, flight_id, user_id, rating, comment=None):
        """Initialize a new rating."""
        self.flight_id = flight_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment
    
    def to_dict(self):
        """Convert rating object to dictionary."""
        return {
            'id': self.id,
            'flight_id': self.flight_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def get_average_rating(flight_id):
        """Get average rating for a flight."""
        from sqlalchemy import func
        result = db.session.query(func.avg(Rating.rating)).filter_by(flight_id=flight_id).scalar()
        return float(result) if result else 0.0
    
    def __repr__(self):
        """String representation of Rating."""
        return f'<Rating Flight:{self.flight_id} User:{self.user_id} - {self.rating}/5>'