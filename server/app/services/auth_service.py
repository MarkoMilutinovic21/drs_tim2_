"""
Authentication service for user login, logout, and token management.
"""
from datetime import datetime, timedelta
from flask import current_app, request
from flask_jwt_extended import create_access_token
from app import db, get_redis
from app.models import User, LoginAttempt
from app.dto import LoginDTO


class AuthService:
    """Service for handling authentication operations."""
    
    @staticmethod
    def login(login_dto: LoginDTO):
        """
        Authenticate user and generate JWT token.
        
        Args:
            login_dto: LoginDTO with email and password
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        # Find user by email
        user = User.query.filter_by(email=login_dto.email).first()
        
        if not user:
            # Log failed attempt (wrong email)
            return {
                'error': 'Invalid email or password'
            }, 401
        
        # Check if account is locked
        if user.is_account_locked():
            locked_until = user.locked_until.isoformat() if user.locked_until else 'unknown'
            return {
                'error': 'Account is locked due to multiple failed login attempts',
                'locked_until': locked_until
            }, 403
        
        # Check if account is active
        if not user.is_active:
            return {
                'error': 'Account is deactivated'
            }, 403
        
        # Verify password
        if not user.check_password(login_dto.password):
            # Log failed attempt
            AuthService._log_failed_attempt(user.id, 'wrong_password')
            
            # Check failed attempts count
            failed_attempts = LoginAttempt.get_recent_failed_attempts(
                user.id,
                minutes=current_app.config['LOCKOUT_DURATION'] // 60
            )
            
            if failed_attempts >= current_app.config['MAX_LOGIN_ATTEMPTS']:
                # Lock account
                user.lock_account(current_app.config['LOCKOUT_DURATION'])
                db.session.commit()
                
                return {
                    'error': f'Account locked due to {current_app.config["MAX_LOGIN_ATTEMPTS"]} failed login attempts',
                    'locked_until': user.locked_until.isoformat()
                }, 403
            
            remaining_attempts = current_app.config['MAX_LOGIN_ATTEMPTS'] - failed_attempts
            return {
                'error': 'Invalid email or password',
                'remaining_attempts': remaining_attempts
            }, 401
        
        # Successful login
        AuthService._log_successful_attempt(user.id)
        
        # Clear previous failed attempts
        LoginAttempt.clear_failed_attempts(user.id)
        
        # Generate JWT token
        access_token = create_access_token(identity=user.id)
        
        return {
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }, 200
    
    @staticmethod
    def logout(jti):
        """
        Logout user by blacklisting JWT token.
        
        Args:
            jti: JWT token ID
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        redis_client = get_redis()
        
        if redis_client:
            # Add token to blacklist with expiration
            expiration = current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()
            redis_client.setex(
                f"blacklist:{jti}",
                int(expiration),
                "true"
            )
        
        return {
            'message': 'Logout successful'
        }, 200
    
    @staticmethod
    def _log_failed_attempt(user_id, reason):
        """Log a failed login attempt."""
        ip_address = request.remote_addr if request else None
        user_agent = request.headers.get('User-Agent') if request else None
        
        attempt = LoginAttempt(
            user_id=user_id,
            success=False,
            ip_address=ip_address,
            user_agent=user_agent,
            failure_reason=reason
        )
        db.session.add(attempt)
        db.session.commit()
    
    @staticmethod
    def _log_successful_attempt(user_id):
        """Log a successful login attempt."""
        ip_address = request.remote_addr if request else None
        user_agent = request.headers.get('User-Agent') if request else None
        
        attempt = LoginAttempt(
            user_id=user_id,
            success=True,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.session.add(attempt)
        db.session.commit()
    
    @staticmethod
    def get_current_user(user_id):
        """
        Get current authenticated user.
        
        Args:
            user_id: User ID from JWT
        
        Returns:
            User object or None
        """
        return db.session.get(User, user_id)