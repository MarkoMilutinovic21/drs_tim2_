"""
Data Transfer Objects (DTOs) for Rating operations.
"""


class RatingCreateDTO:
    """DTO for creating a new rating."""
    
    def __init__(self, flight_id, user_id, rating, comment=None):
        self.flight_id = flight_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment
    
    @staticmethod
    def from_dict(data):
        """Create DTO from dictionary."""
        return RatingCreateDTO(
            flight_id=data.get('flight_id'),
            user_id=data.get('user_id'),
            rating=data.get('rating'),
            comment=data.get('comment')
        )
    
    def validate(self):
        """Validate DTO data."""
        errors = []
        
        if not self.flight_id:
            errors.append("Flight ID is required")
        
        if not self.user_id:
            errors.append("User ID is required")
        
        if not self.rating or self.rating not in [1, 2, 3, 4, 5]:
            errors.append("Rating must be between 1 and 5")
        
        return errors