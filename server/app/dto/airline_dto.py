"""
Data Transfer Objects (DTOs) for Airline operations.
"""


class AirlineCreateDTO:
    """DTO for creating a new airline."""
    
    def __init__(self, name, code, country, description=None, logo_url=None):
        self.name = name
        self.code = code
        self.country = country
        self.description = description
        self.logo_url = logo_url
    
    @staticmethod
    def from_dict(data):
        """Create DTO from dictionary."""
        return AirlineCreateDTO(
            name=data.get('name'),
            code=data.get('code'),
            country=data.get('country'),
            description=data.get('description'),
            logo_url=data.get('logo_url')
        )
    
    def validate(self):
        """Validate DTO data."""
        errors = []
        
        if not self.name or len(self.name.strip()) == 0:
            errors.append("Airline name is required")
        
        if not self.code or len(self.code.strip()) == 0:
            errors.append("Airline code is required")
        elif len(self.code) > 10:
            errors.append("Airline code must be 10 characters or less")
        
        if not self.country or len(self.country.strip()) == 0:
            errors.append("Country is required")
        
        return errors


class AirlineUpdateDTO:
    """DTO for updating airline information."""
    
    def __init__(self, name=None, country=None, description=None, logo_url=None):
        self.name = name
        self.country = country
        self.description = description
        self.logo_url = logo_url
    
    @staticmethod
    def from_dict(data):
        """Create DTO from dictionary."""
        return AirlineUpdateDTO(
            name=data.get('name'),
            country=data.get('country'),
            description=data.get('description'),
            logo_url=data.get('logo_url')
        )
    
    def validate(self):
        """Validate DTO data."""
        errors = []
        
        # No specific validation needed for optional updates
        
        return errors