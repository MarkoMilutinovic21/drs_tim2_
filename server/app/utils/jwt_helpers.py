"""
Helper functions for JWT token handling.
"""
from flask_jwt_extended import get_jwt_identity


def get_current_user_id():
    """
    Get current user ID as integer from JWT token.

    Returns:
        int: User ID or None if not authenticated
    """
    user_id_str = get_jwt_identity()
    return int(user_id_str) if user_id_str else None
