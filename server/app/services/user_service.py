"""
User service for managing user operations.
"""
from flask import current_app
from werkzeug.utils import secure_filename
import os
from app import db
from app.models import User
from app.dto import UserRegistrationDTO, UserUpdateDTO, PasswordChangeDTO, BalanceUpdateDTO
from app.utils import validate_email, validate_password_strength, validate_date_of_birth


class UserService:
    """Service for handling user operations."""
    
    @staticmethod
    def register_user(registration_dto: UserRegistrationDTO):
        """
        Register a new user.
        
        Args:
            registration_dto: UserRegistrationDTO with user data
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        # Validate DTO
        errors = registration_dto.validate()
        if errors:
            return {'errors': errors}, 400
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=registration_dto.email).first()
        if existing_user:
            return {'error': 'Email already registered'}, 409
        
        # Additional validations
        if not validate_email(registration_dto.email):
            return {'error': 'Invalid email format'}, 400
        
        is_valid, error_msg = validate_password_strength(registration_dto.password)
        if not is_valid:
            return {'error': error_msg}, 400
        
        is_valid, error_msg = validate_date_of_birth(registration_dto.date_of_birth)
        if not is_valid:
            return {'error': error_msg}, 400
        
        # Create new user
        try:
            new_user = User(
                first_name=registration_dto.first_name,
                last_name=registration_dto.last_name,
                email=registration_dto.email,
                password=registration_dto.password,
                date_of_birth=registration_dto.date_of_birth,
                gender=registration_dto.gender,
                country=registration_dto.country,
                street=registration_dto.street,
                street_number=registration_dto.street_number,
                account_balance=registration_dto.account_balance,
                role='KORISNIK'  # Default role
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            return {
                'message': 'User registered successfully',
                'user': new_user.to_dict()
            }, 201
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error registering user: {str(e)}")
            return {'error': 'Failed to register user'}, 500
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user by ID.
        
        Args:
            user_id: User ID
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        user = db.session.get(User, user_id)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        return {
            'user': user.to_dict()
        }, 200
    
    @staticmethod
    def get_all_users(page=1, per_page=20):
        """
        Get all users with pagination.
        
        Args:
            page: Page number
            per_page: Items per page
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        try:
            pagination = User.query.order_by(User.created_at.desc()).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            users = [user.to_dict() for user in pagination.items]
            
            return {
                'users': users,
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': pagination.page
            }, 200
        
        except Exception as e:
            current_app.logger.error(f"Error fetching users: {str(e)}")
            return {'error': 'Failed to fetch users'}, 500
    
    @staticmethod
    def update_user(user_id, update_dto: UserUpdateDTO):
        """
        Update user information.
        
        Args:
            user_id: User ID
            update_dto: UserUpdateDTO with updated data
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        user = db.session.get(User, user_id)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        # Validate DTO
        errors = update_dto.validate()
        if errors:
            return {'errors': errors}, 400
        
        # Update fields if provided
        try:
            if update_dto.first_name:
                user.first_name = update_dto.first_name
            
            if update_dto.last_name:
                user.last_name = update_dto.last_name
            
            if update_dto.date_of_birth:
                is_valid, error_msg = validate_date_of_birth(update_dto.date_of_birth)
                if not is_valid:
                    return {'error': error_msg}, 400
                user.date_of_birth = update_dto.date_of_birth
            
            if update_dto.gender:
                user.gender = update_dto.gender
            
            if update_dto.country:
                user.country = update_dto.country
            
            if update_dto.street:
                user.street = update_dto.street
            
            if update_dto.street_number:
                user.street_number = update_dto.street_number
            
            db.session.commit()
            
            return {
                'message': 'User updated successfully',
                'user': user.to_dict()
            }, 200
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating user: {str(e)}")
            return {'error': 'Failed to update user'}, 500
    
    @staticmethod
    def delete_user(user_id):
        """
        Delete user (admin only).
        
        Args:
            user_id: User ID
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        user = db.session.get(User, user_id)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        try:
            db.session.delete(user)
            db.session.commit()
            
            return {
                'message': 'User deleted successfully'
            }, 200
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error deleting user: {str(e)}")
            return {'error': 'Failed to delete user'}, 500
    
    @staticmethod
    def change_password(user_id, password_dto: PasswordChangeDTO):
        """
        Change user password.
        
        Args:
            user_id: User ID
            password_dto: PasswordChangeDTO with old and new password
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        user = db.session.get(User, user_id)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        # Validate DTO
        errors = password_dto.validate()
        if errors:
            return {'errors': errors}, 400
        
        # Check old password
        if not user.check_password(password_dto.old_password):
            return {'error': 'Old password is incorrect'}, 400
        
        # Validate new password
        is_valid, error_msg = validate_password_strength(password_dto.new_password)
        if not is_valid:
            return {'error': error_msg}, 400
        
        try:
            user.set_password(password_dto.new_password)
            db.session.commit()
            
            return {
                'message': 'Password changed successfully'
            }, 200
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error changing password: {str(e)}")
            return {'error': 'Failed to change password'}, 500
    
    @staticmethod
    def update_role(user_id, new_role):
        """
        Update user role (admin only).
        
        Args:
            user_id: User ID
            new_role: New role (KORISNIK, MANAGER, ADMINISTRATOR)
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        user = db.session.get(User, user_id)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        if new_role not in ['KORISNIK', 'MANAGER', 'ADMINISTRATOR']:
            return {'error': 'Invalid role'}, 400
        
        old_role = user.role
        
        try:
            user.role = new_role
            db.session.commit()
            
            # Send email notification about role change
            from app.services.email_service import EmailService
            EmailService.send_role_change_email(user, old_role, new_role)
            
            return {
                'message': 'User role updated successfully',
                'user': user.to_dict()
            }, 200
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating role: {str(e)}")
            return {'error': 'Failed to update role'}, 500
    
    @staticmethod
    def add_balance(user_id, balance_dto: BalanceUpdateDTO):
        """
        Add money to user's account balance.
        
        Args:
            user_id: User ID
            balance_dto: BalanceUpdateDTO with amount
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        user = db.session.get(User, user_id)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        # Validate DTO
        errors = balance_dto.validate()
        if errors:
            return {'errors': errors}, 400
        
        try:
            if user.add_balance(balance_dto.amount):
                db.session.commit()
                
                return {
                    'message': 'Balance added successfully',
                    'new_balance': float(user.account_balance)
                }, 200
            else:
                return {'error': 'Invalid amount'}, 400
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error adding balance: {str(e)}")
            return {'error': 'Failed to add balance'}, 500

    @staticmethod
    def deduct_balance(user_id, balance_dto: BalanceUpdateDTO):
        """
        Deduct money from user's account balance (internal use).
        
        Args:
            user_id: User ID
            balance_dto: BalanceUpdateDTO with amount
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        user = db.session.get(User, user_id)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        errors = balance_dto.validate()
        if errors:
            return {'errors': errors}, 400
        
        try:
            if user.deduct_balance(balance_dto.amount):
                db.session.commit()
                return {
                    'message': 'Balance deducted successfully',
                    'new_balance': float(user.account_balance)
                }, 200
            return {'error': 'Insufficient balance'}, 400
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error deducting balance: {str(e)}")
            return {'error': 'Failed to deduct balance'}, 500

    @staticmethod
    def refund_balance(user_id, balance_dto: BalanceUpdateDTO):
        """
        Refund money to user's account balance (internal use).
        
        Args:
            user_id: User ID
            balance_dto: BalanceUpdateDTO with amount
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        user = db.session.get(User, user_id)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        errors = balance_dto.validate()
        if errors:
            return {'errors': errors}, 400
        
        try:
            if user.add_balance(balance_dto.amount):
                db.session.commit()
                return {
                    'message': 'Balance refunded successfully',
                    'new_balance': float(user.account_balance)
                }, 200
            return {'error': 'Invalid amount'}, 400
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error refunding balance: {str(e)}")
            return {'error': 'Failed to refund balance'}, 500
    
    @staticmethod
    def upload_profile_picture(user_id, file):
        """
        Upload user profile picture.
        
        Args:
            user_id: User ID
            file: File object from request
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        user = db.session.get(User, user_id)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        if not file:
            return {'error': 'No file provided'}, 400
        
        # Check file extension
        filename = secure_filename(file.filename)
        if '.' not in filename:
            return {'error': 'Invalid file format'}, 400
        
        extension = filename.rsplit('.', 1)[1].lower()
        if extension not in current_app.config['ALLOWED_EXTENSIONS']:
            return {'error': 'File type not allowed'}, 400
        
        try:
            # Create unique filename
            import uuid
            unique_filename = f"{user_id}_{uuid.uuid4().hex}.{extension}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            
            # Save file
            file.save(filepath)
            
            # Update user profile picture path
            user.profile_picture = unique_filename
            db.session.commit()
            
            return {
                'message': 'Profile picture uploaded successfully',
                'profile_picture': unique_filename
            }, 200
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error uploading profile picture: {str(e)}")
            return {'error': 'Failed to upload profile picture'}, 500
