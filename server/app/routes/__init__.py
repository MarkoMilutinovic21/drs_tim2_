"""
Routes module initialization.
"""
from .auth import auth_bp
from .users import users_bp
from .airlines import airlines_bp

__all__ = ['auth_bp', 'users_bp', 'airlines_bp']