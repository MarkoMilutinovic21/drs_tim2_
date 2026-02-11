"""
Models module initialization.
"""
from .flight import Flight
from .booking import Booking
from .rating import Rating
from .airline import Airline

__all__ = ['Flight', 'Booking', 'Rating', 'Airline']
