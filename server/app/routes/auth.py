"""
Authentication routes for login, logout, and user registration.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import AuthService, UserService
from app.dto import LoginDTO, UserRegistrationDTO

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    
    POST /api/auth/register
    Body: {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "password": "password123",
        "date_of_birth": "1990-01-15",
        "gender": "M",
        "country": "Serbia",
        "street": "Main Street",
        "street_number": "123",
        "account_balance": 0.00
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Create DTO
        registration_dto = UserRegistrationDTO.from_dict(data)
        
        # Register user
        response, status_code = UserService.register_user(registration_dto)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user and get JWT token.
    
    POST /api/auth/login
    Body: {
        "email": "john@example.com",
        "password": "password123"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Create DTO
        login_dto = LoginDTO.from_dict(data)
        
        # Validate DTO
        errors = login_dto.validate()
        if errors:
            return jsonify({'errors': errors}), 400
        
        # Login
        response, status_code = AuthService.login(login_dto)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Login failed: {str(e)}'}), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout user (blacklist JWT token).
    
    POST /api/auth/logout
    Headers: Authorization: Bearer <token>
    """
    try:
        # Get JWT token ID
        jti = get_jwt()['jti']
        
        # Logout (blacklist token)
        response, status_code = AuthService.logout(jti)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Logout failed: {str(e)}'}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current authenticated user information.
    
    GET /api/auth/me
    Headers: Authorization: Bearer <token>
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Get user
        user = AuthService.get_current_user(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get user: {str(e)}'}), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required()
def refresh_token():
    """
    Refresh JWT token (optional - for extending session).
    
    POST /api/auth/refresh
    Headers: Authorization: Bearer <token>
    """
    try:
        from flask_jwt_extended import create_access_token
        
        current_user_id = get_jwt_identity()
        
        # Create new access token
        new_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            'message': 'Token refreshed successfully',
            'access_token': new_token
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Token refresh failed: {str(e)}'}), 500