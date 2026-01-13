"""
Airline model for managing airline companies.
"""
from datetime import datetime
from app import db


class Airline(db.Model):
    """Airline model representing airline companies."""
    
    __tablename__ = 'airlines'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Airline Information
    name = db.Column(db.String(200), unique=True, nullable=False, index=True)
    code = db.Column(db.String(10), unique=True, nullable=False)  # e.g., "AA", "BA", "LH"
    country = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    logo_url = db.Column(db.String(255), nullable=True)
    
    # Status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Created By (Manager who created this airline)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    creator = db.relationship('User', backref='created_airlines', foreign_keys=[created_by])
    
    def __init__(self, name, code, country, created_by, description=None, logo_url=None):
        """Initialize a new airline."""
        self.name = name
        self.code = code.upper()  # Always uppercase
        self.country = country
        self.created_by = created_by
        self.description = description
        self.logo_url = logo_url
    
    def to_dict(self):
        """Convert airline object to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'country': self.country,
            'description': self.description,
            'logo_url': self.logo_url,
            'is_active': self.is_active,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        """String representation of Airline."""
        return f'<Airline {self.code} - {self.name}>'