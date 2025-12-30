"""
Validation utility functions.
"""
import re
from datetime import datetime, date


def validate_email(email):
    """
    Validate email format.
    
    Args:
        email: Email string to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password_strength(password):
    """
    Validate password strength.
    
    Args:
        password: Password string to validate
    
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    # Optional: Add more complexity requirements
    # if not re.search(r'[A-Z]', password):
    #     return False, "Password must contain at least one uppercase letter"
    
    # if not re.search(r'[0-9]', password):
    #     return False, "Password must contain at least one digit"
    
    return True, ""


def validate_date_of_birth(dob):
    """
    Validate date of birth (must be at least 18 years old).
    
    Args:
        dob: Date object or string in ISO format
    
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if isinstance(dob, str):
        try:
            dob = date.fromisoformat(dob)
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD"
    
    if not isinstance(dob, date):
        return False, "Date of birth must be a valid date"
    
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    
    if age < 18:
        return False, "User must be at least 18 years old"
    
    if age > 120:
        return False, "Invalid date of birth"
    
    return True, ""


def validate_gender(gender):
    """
    Validate gender value.
    
    Args:
        gender: Gender string
    
    Returns:
        bool: True if valid, False otherwise
    """
    return gender in ['M', 'F', 'Other']


def validate_role(role):
    """
    Validate user role.
    
    Args:
        role: Role string
    
    Returns:
        bool: True if valid, False otherwise
    """
    return role in ['KORISNIK', 'MENADŽER', 'ADMINISTRATOR']


def validate_amount(amount):
    """
    Validate monetary amount.
    
    Args:
        amount: Amount to validate
    
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    try:
        amount = float(amount)
        if amount <= 0:
            return False, "Amount must be greater than 0"
        if amount > 1000000:
            return False, "Amount is too large"
        return True, ""
    except (ValueError, TypeError):
        return False, "Invalid amount format"


def sanitize_string(text, max_length=None):
    """
    Sanitize string input (remove extra whitespace, trim).
    
    Args:
        text: Text to sanitize
        max_length: Optional maximum length
    
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Trim to max length if specified
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text.strip()