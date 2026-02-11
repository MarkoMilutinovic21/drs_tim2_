"""
Routes module initialization.
"""
from .flights import flights_bp
from .bookings import bookings_bp
from .ratings import ratings_bp
from .airlines import airlines_bp

__all__ = ['flights_bp', 'bookings_bp', 'ratings_bp', 'airlines_bp']
