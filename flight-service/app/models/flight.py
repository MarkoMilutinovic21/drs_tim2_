"""
Flight model for managing flights.
"""
from datetime import datetime, timezone
from app import db


class Flight(db.Model):
    """Flight model representing flights."""
    
    __tablename__ = 'flights'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Flight Information
    name = db.Column(db.String(200), nullable=False, index=True)
    airline_id = db.Column(db.Integer, nullable=False)  # Reference to Airline in Server DB
    distance_km = db.Column(db.Integer, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)  # For testing: 1 minute
    
    # Departure & Arrival
    departure_time = db.Column(db.DateTime, nullable=False, index=True)
    departure_airport = db.Column(db.String(200), nullable=False)
    arrival_airport = db.Column(db.String(200), nullable=False)
    
    # Pricing
    ticket_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Creator
    created_by = db.Column(db.Integer, nullable=False)  # Manager user ID from Server DB
    
    # Status: PENDING, APPROVED, REJECTED, CANCELLED, ONGOING, COMPLETED
    status = db.Column(db.String(20), default='PENDING', nullable=False, index=True)
    
    # Rejection reason (if status is REJECTED)
    rejection_reason = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    bookings = db.relationship('Booking', backref='flight', lazy='dynamic', cascade='all, delete-orphan')
    ratings = db.relationship('Rating', backref='flight', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, name, airline_id, distance_km, duration_minutes, 
                 departure_time, departure_airport, arrival_airport, 
                 ticket_price, created_by):
        """Initialize a new flight."""
        self.name = name
        self.airline_id = airline_id
        self.distance_km = distance_km
        self.duration_minutes = duration_minutes
        self.departure_time = departure_time
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.ticket_price = ticket_price
        self.created_by = created_by
        self.status = 'PENDING'
    
    def approve(self):
        """Approve the flight."""
        self.status = 'APPROVED'
    
    def reject(self, reason):
        """Reject the flight with a reason."""
        self.status = 'REJECTED'
        self.rejection_reason = reason
    
    def cancel(self):
        """Cancel the flight."""
        self.status = 'CANCELLED'
    
    def start(self):
        """Mark flight as ongoing."""
        self.status = 'ONGOING'
    
    def complete(self):
        """Mark flight as completed."""
        self.status = 'COMPLETED'
    
    def is_upcoming(self):
        """Check if flight is upcoming (approved and not started)."""
        return self.status == 'APPROVED' and datetime.utcnow() < self.departure_time
    
    def is_ongoing(self):
        """Check if flight is currently ongoing."""
        if self.status != 'APPROVED' and self.status != 'ONGOING':
            return False
        
        now = datetime.utcnow()
        from datetime import timedelta
        end_time = self.departure_time + timedelta(minutes=self.duration_minutes)
        
        return self.departure_time <= now < end_time
    
    def is_completed(self):
        """Check if flight is completed."""
        if self.status == 'COMPLETED':
            return True
        
        now = datetime.utcnow()
        from datetime import timedelta
        end_time = self.departure_time + timedelta(minutes=self.duration_minutes)
        
        return now >= end_time
    
    def get_remaining_time(self):
        """Get remaining time in minutes for ongoing flight."""
        if not self.is_ongoing():
            return 0
        
        from datetime import timedelta
        now = datetime.utcnow()
        end_time = self.departure_time + timedelta(minutes=self.duration_minutes)
        remaining = end_time - now
        
        return max(0, int(remaining.total_seconds() / 60))
    
    def to_dict(self):
        """Convert flight object to dictionary."""
        def _format_utc(value):
            if not value:
                return None
            return value.replace(tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z')

        return {
            'id': self.id,
            'name': self.name,
            'airline_id': self.airline_id,
            'distance_km': self.distance_km,
            'duration_minutes': self.duration_minutes,
            'departure_time': _format_utc(self.departure_time),
            'departure_airport': self.departure_airport,
            'arrival_airport': self.arrival_airport,
            'ticket_price': float(self.ticket_price),
            'created_by': self.created_by,
            'status': self.status,
            'rejection_reason': self.rejection_reason,
            'is_upcoming': self.is_upcoming(),
            'is_ongoing': self.is_ongoing(),
            'is_completed': self.is_completed(),
            'remaining_time': self.get_remaining_time() if self.is_ongoing() else None,
            'created_at': _format_utc(self.created_at),
            'updated_at': _format_utc(self.updated_at)
        }
    
    def __repr__(self):
        """String representation of Flight."""
        return f'<Flight {self.name} - {self.status}>'
