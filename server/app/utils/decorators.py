"""
Custom decorators for route protection and validation.
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request
from app.utils.jwt_helpers import get_current_user_id
from app.models import User
from app import db


def admin_required():
    """Decorator to require admin role."""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_current_user_id()
            user = db.session.get(User, current_user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            if not user.is_admin():
                return jsonify({'error': 'Admin privileges required'}), 403
            
            return fn(*args, **kwargs)
        return decorator
    return wrapper


def manager_required():
    """Decorator to require manager role."""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_current_user_id()
            user = db.session.get(User, current_user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            if not user.is_manager() and not user.is_admin():
                return jsonify({'error': 'Manager privileges required'}), 403
            
            return fn(*args, **kwargs)
        return decorator
    return wrapper


def role_required(allowed_roles):
    """
    Decorator to require specific role(s).
    
    Args:
        allowed_roles: List of allowed roles or single role string
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_current_user_id()
            user = db.session.get(User, current_user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Convert single role to list
            roles = allowed_roles if isinstance(allowed_roles, list) else [allowed_roles]
            
            if user.role not in roles:
                return jsonify({'error': f'Required role: {", ".join(roles)}'}), 403
            
            return fn(*args, **kwargs)
        return decorator
    return wrapper


def account_active_required():
    """Decorator to check if account is active and not locked."""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_current_user_id()
            user = db.session.get(User, current_user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            if not user.is_active:
                return jsonify({'error': 'Account is deactivated'}), 403
            
            if user.is_account_locked():
                locked_until = user.locked_until.isoformat() if user.locked_until else 'unknown'
                return jsonify({
                    'error': 'Account is locked',
                    'locked_until': locked_until
                }), 403
            
            return fn(*args, **kwargs)
        return decorator
    return wrapper