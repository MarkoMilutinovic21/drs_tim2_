"""
Data Transfer Objects (DTOs) for Authentication operations.
"""


class LoginDTO:
    """DTO for user login."""
    
    def __init__(self, email, password):
        self.email = email
        self.password = password
    
    @staticmethod
    def from_dict(data):
        """Create DTO from dictionary."""
        return LoginDTO(
            email=data.get('email'),
            password=data.get('password')
        )
    
    def validate(self):
        """Validate DTO data."""
        errors = []
        
        if not self.email or '@' not in self.email:
            errors.append("Valid email is required")
        
        if not self.password:
            errors.append("Password is required")
        
        return errors


class RoleUpdateDTO:
    """DTO for updating user role (admin only)."""
    
    def __init__(self, user_id, new_role):
        self.user_id = user_id
        self.new_role = new_role
    
    @staticmethod
    def from_dict(data):
        """Create DTO from dictionary."""
        return RoleUpdateDTO(
            user_id=data.get('user_id'),
            new_role=data.get('new_role')
        )
    
    def validate(self):
        """Validate DTO data."""
        errors = []
        
        if not self.user_id:
            errors.append("User ID is required")
        
        if self.new_role not in ['KORISNIK', 'MENADŽER', 'ADMINISTRATOR']:
            errors.append("Role must be KORISNIK, MENADŽER, or ADMINISTRATOR")
        
        return errors