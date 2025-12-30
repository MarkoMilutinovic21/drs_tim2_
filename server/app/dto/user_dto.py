"""
Data Transfer Objects (DTOs) for User-related operations.
"""
from datetime import date


class UserRegistrationDTO:
    """DTO for user registration."""
    
    def __init__(self, first_name, last_name, email, password, date_of_birth,
                 gender, country, street, street_number, account_balance=0.00):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.country = country
        self.street = street
        self.street_number = street_number
        self.account_balance = account_balance
    
    @staticmethod
    def from_dict(data):
        """Create DTO from dictionary."""
        # Parse date_of_birth if it's a string
        dob = data.get('date_of_birth')
        if isinstance(dob, str):
            dob = date.fromisoformat(dob)
        
        return UserRegistrationDTO(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            password=data.get('password'),
            date_of_birth=dob,
            gender=data.get('gender'),
            country=data.get('country'),
            street=data.get('street'),
            street_number=data.get('street_number'),
            account_balance=data.get('account_balance', 0.00)
        )
    
    def validate(self):
        """Validate DTO data."""
        errors = []
        
        if not self.first_name or len(self.first_name.strip()) == 0:
            errors.append("First name is required")
        
        if not self.last_name or len(self.last_name.strip()) == 0:
            errors.append("Last name is required")
        
        if not self.email or '@' not in self.email:
            errors.append("Valid email is required")
        
        if not self.password or len(self.password) < 6:
            errors.append("Password must be at least 6 characters long")
        
        if not self.date_of_birth:
            errors.append("Date of birth is required")
        
        if self.gender not in ['M', 'F', 'Other']:
            errors.append("Gender must be M, F, or Other")
        
        if not self.country or len(self.country.strip()) == 0:
            errors.append("Country is required")
        
        if not self.street or len(self.street.strip()) == 0:
            errors.append("Street is required")
        
        if not self.street_number or len(self.street_number.strip()) == 0:
            errors.append("Street number is required")
        
        return errors


class UserUpdateDTO:
    """DTO for updating user information."""
    
    def __init__(self, first_name=None, last_name=None, date_of_birth=None,
                 gender=None, country=None, street=None, street_number=None):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.country = country
        self.street = street
        self.street_number = street_number
    
    @staticmethod
    def from_dict(data):
        """Create DTO from dictionary."""
        dob = data.get('date_of_birth')
        if dob and isinstance(dob, str):
            dob = date.fromisoformat(dob)
        
        return UserUpdateDTO(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            date_of_birth=dob,
            gender=data.get('gender'),
            country=data.get('country'),
            street=data.get('street'),
            street_number=data.get('street_number')
        )
    
    def validate(self):
        """Validate DTO data."""
        errors = []
        
        if self.gender and self.gender not in ['M', 'F', 'Other']:
            errors.append("Gender must be M, F, or Other")
        
        return errors


class PasswordChangeDTO:
    """DTO for changing user password."""
    
    def __init__(self, old_password, new_password):
        self.old_password = old_password
        self.new_password = new_password
    
    @staticmethod
    def from_dict(data):
        """Create DTO from dictionary."""
        return PasswordChangeDTO(
            old_password=data.get('old_password'),
            new_password=data.get('new_password')
        )
    
    def validate(self):
        """Validate DTO data."""
        errors = []
        
        if not self.old_password:
            errors.append("Old password is required")
        
        if not self.new_password or len(self.new_password) < 6:
            errors.append("New password must be at least 6 characters long")
        
        return errors


class BalanceUpdateDTO:
    """DTO for updating user account balance."""
    
    def __init__(self, amount):
        self.amount = amount
    
    @staticmethod
    def from_dict(data):
        """Create DTO from dictionary."""
        return BalanceUpdateDTO(amount=float(data.get('amount', 0)))
    
    def validate(self):
        """Validate DTO data."""
        errors = []
        
        if self.amount <= 0:
            errors.append("Amount must be greater than 0")
        
        return errors