"""
Booking model for managing flight bookings.
"""
from datetime import datetime, timezone
from app import db


class Booking(db.Model):
    """Booking model representing purchased flight tickets."""
    
    __tablename__ = 'bookings'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Flight Reference
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False, index=True)
    
    # User Reference (from Server DB)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    
    # Booking Information
    ticket_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Status: PENDING, PROCESSING, COMPLETED, CANCELLED, REFUNDED
    status = db.Column(db.String(20), default='PENDING', nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __init__(self, flight_id, user_id, ticket_price):
        """Initialize a new booking."""
        self.flight_id = flight_id
        self.user_id = user_id
        self.ticket_price = ticket_price
        self.status = 'PENDING'
    
    def mark_processing(self):
        """Mark booking as processing."""
        self.status = 'PROCESSING'
    
    def mark_completed(self):
        """Mark booking as completed."""
        self.status = 'COMPLETED'
    
    def mark_cancelled(self):
        """Mark booking as cancelled."""
        self.status = 'CANCELLED'
    
    def mark_refunded(self):
        """Mark booking as refunded."""
        self.status = 'REFUNDED'
    
    def to_dict(self):
        """Convert booking object to dictionary."""
        def _format_utc(value):
            if not value:
                return None
            return value.replace(tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z')

        return {
            'id': self.id,
            'flight_id': self.flight_id,
            'user_id': self.user_id,
            'ticket_price': float(self.ticket_price),
            'status': self.status,
            'created_at': _format_utc(self.created_at),
            'updated_at': _format_utc(self.updated_at)
        }
    
    def __repr__(self):
        """String representation of Booking."""
        return f'<Booking User:{self.user_id} Flight:{self.flight_id} - {self.status}>'
