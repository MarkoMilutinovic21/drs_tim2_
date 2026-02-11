"""
Routes module initialization.
"""
from .auth import auth_bp
from .users import users_bp
from .notifications import notifications_bp
from .proxy import proxy_bp

__all__ = [
    'auth_bp',
    'users_bp',
    'notifications_bp',
    'proxy_bp'
]
