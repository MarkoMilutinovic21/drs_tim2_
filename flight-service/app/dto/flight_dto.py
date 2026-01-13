"""
Data Transfer Objects (DTOs) for Flight operations.
"""
from datetime import datetime


class FlightCreateDTO:
    """DTO for creating a new flight."""
    
    def __init__(self, name, airline_id, distance_km, duration_minutes,
                 departure_time, departure_airport, arrival_airport, ticket_price):
        self.name = name
        self.airline_id = airline_id
        self.distance_km = distance_km
        self.duration_minutes = duration_minutes
        self.departure_time = departure_time
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.ticket_price = ticket_price
    
    @staticmethod
    def from_dict(data):
        """Create DTO from dictionary."""
        # Parse departure_time if it's a string
        departure_time = data.get('departure_time')
        if isinstance(departure_time, str):
            departure_time = datetime.fromisoformat(departure_time.replace('Z', '+00:00'))
        
        return FlightCreateDTO(
            name=data.get('name'),
            airline_id=data.get('airline_id'),
            distance_km=data.get('distance_km'),
            duration_minutes=data.get('duration_minutes'),
            departure_time=departure_time,
            departure_airport=data.get('departure_airport'),
            arrival_airport=data.get('arrival_airport'),
            ticket_price=data.get('ticket_price')
        )
    
    def validate(self):
        """Validate DTO data."""
        errors = []
        
        if not self.name or len(self.name.strip()) == 0:
            errors.append("Flight name is required")
        
        if not self.airline_id:
            errors.append("Airline ID is required")
        
        if not self.distance_km or self.distance_km <= 0:
            errors.append("Distance must be greater than 0")
        
        if not self.duration_minutes or self.duration_minutes <= 0:
            errors.append("Duration must be greater than 0")
        
        if not self.departure_time:
            errors.append("Departure time is required")
        elif self.departure_time < datetime.utcnow():
            errors.append("Departure time cannot be in the past")
        
        if not self.departure_airport or len(self.departure_airport.strip()) == 0:
            errors.append("Departure airport is required")
        
        if not self.arrival_airport or len(self.arrival_airport.strip()) == 0:
            errors.append("Arrival airport is required")
        
        if not self.ticket_price or self.ticket_price <= 0:
            errors.append("Ticket price must be greater than 0")
        
        return errors


class FlightUpdateDTO:
    """DTO for updating flight information."""
    
    def __init__(self, name=None, distance_km=None, duration_minutes=None,
                 departure_time=None, departure_airport=None, 
                 arrival_airport=None, ticket_price=None):
        self.name = name
        self.distance_km = distance_km
        self.duration_minutes = duration_minutes
        self.departure_time = departure_time
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.ticket_price = ticket_price
    
    @staticmethod
    def from_dict(data):
        """Create DTO from dictionary."""
        departure_time = data.get('departure_time')
        if departure_time and isinstance(departure_time, str):
            departure_time = datetime.fromisoformat(departure_time.replace('Z', '+00:00'))
        
        return FlightUpdateDTO(
            name=data.get('name'),
            distance_km=data.get('distance_km'),
            duration_minutes=data.get('duration_minutes'),
            departure_time=departure_time,
            departure_airport=data.get('departure_airport'),
            arrival_airport=data.get('arrival_airport'),
            ticket_price=data.get('ticket_price')
        )
    
    def validate(self):
        """Validate DTO data."""
        errors = []
        
        if self.distance_km and self.distance_km <= 0:
            errors.append("Distance must be greater than 0")
        
        if self.duration_minutes and self.duration_minutes <= 0:
            errors.append("Duration must be greater than 0")
        
        if self.departure_time and self.departure_time < datetime.utcnow():
            errors.append("Departure time cannot be in the past")
        
        if self.ticket_price and self.ticket_price <= 0:
            errors.append("Ticket price must be greater than 0")
        
        return errors


class FlightApprovalDTO:
    """DTO for approving/rejecting flight."""
    
    def __init__(self, action, rejection_reason=None):
        self.action = action  # 'approve' or 'reject'
        self.rejection_reason = rejection_reason
    
    @staticmethod
    def from_dict(data):
        """Create DTO from dictionary."""
        return FlightApprovalDTO(
            action=data.get('action'),
            rejection_reason=data.get('rejection_reason')
        )
    
    def validate(self):
        """Validate DTO data."""
        errors = []
        
        if self.action not in ['approve', 'reject']:
            errors.append("Action must be 'approve' or 'reject'")
        
        if self.action == 'reject' and not self.rejection_reason:
            errors.append("Rejection reason is required when rejecting")
        
        return errors


class FlightSearchDTO:
    """DTO for searching flights."""
    
    def __init__(self, name=None, airline_id=None, status=None):
        self.name = name
        self.airline_id = airline_id
        self.status = status
    
    @staticmethod
    def from_dict(data):
        """Create DTO from dictionary."""
        return FlightSearchDTO(
            name=data.get('name'),
            airline_id=data.get('airline_id'),
            status=data.get('status')
        )