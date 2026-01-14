"""
User management routes.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils.jwt_helpers import get_current_user_id
from app.services import UserService
from app.dto import UserUpdateDTO, PasswordChangeDTO, BalanceUpdateDTO, RoleUpdateDTO
from app.utils import admin_required, account_active_required
from app import db
from app.models import User

users_bp = Blueprint('users', __name__)


@users_bp.route('', methods=['GET'])
@jwt_required()
@admin_required()
def get_all_users():
    """
    Get all users (admin only).
    
    GET /api/users?page=1&per_page=20
    Headers: Authorization: Bearer <token>
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        response, status_code = UserService.get_all_users(page, per_page)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch users: {str(e)}'}), 500


@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """
    Get user by ID.
    
    GET /api/users/{user_id}
    Headers: Authorization: Bearer <token>
    """
    try:
        current_user_id = get_current_user_id()
        current_user = db.session.get(User, current_user_id)
        
        # Users can only view their own profile unless admin
        if user_id != current_user_id and not current_user.is_admin():
            return jsonify({'error': 'Unauthorized'}), 403
        
        response, status_code = UserService.get_user_by_id(user_id)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch user: {str(e)}'}), 500


@users_bp.route('/<int:user_id>/internal', methods=['GET'])
def get_user_internal(user_id):
    """
    Get basic user info for internal services (no auth).
    
    GET /api/users/{user_id}/internal
    """
    try:
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'id': user.id,
                'email': user.email,
                'account_balance': float(user.account_balance),
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch user: {str(e)}'}), 500


@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
@account_active_required()
def update_user(user_id):
    """
    Update user information.
    
    PUT /api/users/{user_id}
    Headers: Authorization: Bearer <token>
    Body: {
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1990-01-15",
        "gender": "M",
        "country": "Serbia",
        "street": "Main Street",
        "street_number": "123"
    }
    """
    try:
        current_user_id = get_current_user_id()
        
        # Users can only update their own profile
        if user_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Create DTO
        update_dto = UserUpdateDTO.from_dict(data)
        
        # Update user
        response, status_code = UserService.update_user(user_id, update_dto)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to update user: {str(e)}'}), 500


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required()
def delete_user(user_id):
    """
    Delete user (admin only).
    
    DELETE /api/users/{user_id}
    Headers: Authorization: Bearer <token>
    """
    try:
        current_user_id = get_current_user_id()
        
        # Admin cannot delete themselves
        if user_id == current_user_id:
            return jsonify({'error': 'Cannot delete your own account'}), 400
        
        response, status_code = UserService.delete_user(user_id)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to delete user: {str(e)}'}), 500


@users_bp.route('/<int:user_id>/password', methods=['PUT'])
@jwt_required()
@account_active_required()
def change_password(user_id):
    """
    Change user password.
    
    PUT /api/users/{user_id}/password
    Headers: Authorization: Bearer <token>
    Body: {
        "old_password": "oldpass123",
        "new_password": "newpass123"
    }
    """
    try:
        current_user_id = get_current_user_id()
        
        # Users can only change their own password
        if user_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Create DTO
        password_dto = PasswordChangeDTO.from_dict(data)
        
        # Change password
        response, status_code = UserService.change_password(user_id, password_dto)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to change password: {str(e)}'}), 500


@users_bp.route('/<int:user_id>/role', methods=['PUT'])
@jwt_required()
@admin_required()
def update_user_role(user_id):
    """
    Update user role (admin only).

    PUT /api/users/{user_id}/role
    Headers: Authorization: Bearer <token>
    Body: {
        "new_role": "MANAGER"
    }
    """
    try:
        current_user_id = get_current_user_id()
        
        # Admin cannot change their own role
        if user_id == current_user_id:
            return jsonify({'error': 'Cannot change your own role'}), 400
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        new_role = data.get('new_role')
        
        if not new_role:
            return jsonify({'error': 'new_role is required'}), 400
        
        # Update role
        response, status_code = UserService.update_role(user_id, new_role)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to update role: {str(e)}'}), 500


@users_bp.route('/<int:user_id>/balance', methods=['POST'])
@jwt_required()
@account_active_required()
def add_balance(user_id):
    """
    Add money to user account balance.
    
    POST /api/users/{user_id}/balance
    Headers: Authorization: Bearer <token>
    Body: {
        "amount": 100.00
    }
    """
    try:
        current_user_id = get_current_user_id()
        
        # Users can only add to their own balance
        if user_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Create DTO
        balance_dto = BalanceUpdateDTO.from_dict(data)
        
        # Add balance
        response, status_code = UserService.add_balance(user_id, balance_dto)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to add balance: {str(e)}'}), 500


@users_bp.route('/<int:user_id>/deduct', methods=['POST'])
def deduct_balance(user_id):
    """
    Deduct money from user account balance (internal use).
    
    POST /api/users/{user_id}/deduct
    Body: {
        "amount": 100.00
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        balance_dto = BalanceUpdateDTO.from_dict(data)
        response, status_code = UserService.deduct_balance(user_id, balance_dto)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to deduct balance: {str(e)}'}), 500


@users_bp.route('/<int:user_id>/refund', methods=['POST'])
def refund_balance(user_id):
    """
    Refund money to user account balance (internal use).
    
    POST /api/users/{user_id}/refund
    Body: {
        "amount": 100.00
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        balance_dto = BalanceUpdateDTO.from_dict(data)
        response, status_code = UserService.refund_balance(user_id, balance_dto)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to refund balance: {str(e)}'}), 500


@users_bp.route('/<int:user_id>/profile-picture', methods=['POST'])
@jwt_required()
@account_active_required()
def upload_profile_picture(user_id):
    """
    Upload user profile picture.
    
    POST /api/users/{user_id}/profile-picture
    Headers: Authorization: Bearer <token>
    Body: multipart/form-data with 'file' field
    """
    try:
        current_user_id = get_current_user_id()
        
        # Users can only upload their own profile picture
        if user_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Upload picture
        response, status_code = UserService.upload_profile_picture(user_id, file)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to upload profile picture: {str(e)}'}), 500
