"""
User model for authentication and user management.
"""
from datetime import datetime
from decimal import Decimal
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(db.Model):
    """User model representing registered users in the system."""
    
    __tablename__ = 'users'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Personal Information
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Additional Information
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)  # 'M', 'F', 'Other'
    country = db.Column(db.String(100), nullable=False)
    street = db.Column(db.String(200), nullable=False)
    street_number = db.Column(db.String(20), nullable=False)
    
    # Account Balance
    account_balance = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    
    # Profile Picture
    profile_picture = db.Column(db.String(255), nullable=True)
    
    # Role: KORISNIK, MANAGER, ADMINISTRATOR
    role = db.Column(db.String(20), default='KORISNIK', nullable=False)
    
    # Account Status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_locked = db.Column(db.Boolean, default=False, nullable=False)
    locked_until = db.Column(db.DateTime, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    login_attempts = db.relationship('LoginAttempt', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, first_name, last_name, email, password, date_of_birth, 
                 gender, country, street, street_number, account_balance=0.00, role='KORISNIK'):
        """Initialize a new user."""
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.country = country
        self.street = street
        self.street_number = street_number
        self.account_balance = account_balance
        self.role = role
    
    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash."""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if user is an administrator."""
        return self.role == 'ADMINISTRATOR'
    
    def is_manager(self):
        """Check if user is a manager."""
        return self.role == 'MANAGER'
    
    def is_regular_user(self):
        """Check if user is a regular user."""
        return self.role == 'KORISNIK'
    
    def can_create_flights(self):
        """Check if user can create flights (managers only)."""
        return self.role == 'MANAGER'
    
    def lock_account(self, duration_seconds):
        """Lock the user account for specified duration."""
        from datetime import timedelta
        self.is_locked = True
        self.locked_until = datetime.utcnow() + timedelta(seconds=duration_seconds)
    
    def unlock_account(self):
        """Unlock the user account."""
        self.is_locked = False
        self.locked_until = None
    
    def is_account_locked(self):
        """Check if account is currently locked."""
        if not self.is_locked:
            return False
        
        if self.locked_until and datetime.utcnow() > self.locked_until:
            # Lock period expired, unlock automatically
            self.unlock_account()
            db.session.commit()
            return False
        
        return True
    
    def add_balance(self, amount):
        """Add money to user's account balance."""
        if amount > 0:
            self.account_balance += Decimal(str(amount))
            return True
        return False
    
    def deduct_balance(self, amount):
        """Deduct money from user's account balance."""
        if amount > 0 and self.account_balance >= Decimal(str(amount)):
            self.account_balance -= Decimal(str(amount))
            return True
        return False
    
    def to_dict(self, include_sensitive=False):
        """Convert user object to dictionary."""
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'country': self.country,
            'street': self.street,
            'street_number': self.street_number,
            'account_balance': float(self.account_balance),
            'profile_picture': self.profile_picture,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_sensitive:
            data['is_locked'] = self.is_locked
            data['locked_until'] = self.locked_until.isoformat() if self.locked_until else None
        
        return data
    
    def __repr__(self):
        """String representation of User."""
        return f'<User {self.email} - {self.role}>'