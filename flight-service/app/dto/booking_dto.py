"""
Data Transfer Objects (DTOs) for Booking operations.
"""


class BookingCreateDTO:
    """DTO for creating a new booking."""
    
    def __init__(self, flight_id, user_id):
        self.flight_id = flight_id
        self.user_id = user_id
    
    @staticmethod
    def from_dict(data):
        """Create DTO from dictionary."""
        return BookingCreateDTO(
            flight_id=data.get('flight_id'),
            user_id=data.get('user_id')
        )
    
    def validate(self):
        """Validate DTO data."""
        errors = []
        
        if not self.flight_id:
            errors.append("Flight ID is required")
        
        if not self.user_id:
            errors.append("User ID is required")
        
        return errors