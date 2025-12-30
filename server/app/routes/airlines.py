"""
Airline management routes.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import AirlineService
from app.dto import AirlineCreateDTO, AirlineUpdateDTO
from app.utils import manager_required, admin_required, account_active_required

airlines_bp = Blueprint('airlines', __name__)


@airlines_bp.route('', methods=['POST'])
@jwt_required()
@manager_required()
@account_active_required()
def create_airline():
    """
    Create a new airline (manager only).
    
    POST /api/airlines
    Headers: Authorization: Bearer <token>
    Body: {
        "name": "Air Serbia",
        "code": "JU",
        "country": "Serbia",
        "description": "National airline of Serbia",
        "logo_url": "https://example.com/logo.png"
    }
    """
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Create DTO
        airline_dto = AirlineCreateDTO.from_dict(data)
        
        # Create airline
        response, status_code = AirlineService.create_airline(airline_dto, current_user_id)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to create airline: {str(e)}'}), 500


@airlines_bp.route('', methods=['GET'])
def get_all_airlines():
    """
    Get all airlines (public endpoint).
    
    GET /api/airlines?active_only=true
    """
    try:
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        
        response, status_code = AirlineService.get_all_airlines(active_only)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch airlines: {str(e)}'}), 500


@airlines_bp.route('/<int:airline_id>', methods=['GET'])
def get_airline(airline_id):
    """
    Get airline by ID (public endpoint).
    
    GET /api/airlines/{airline_id}
    """
    try:
        response, status_code = AirlineService.get_airline_by_id(airline_id)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch airline: {str(e)}'}), 500


@airlines_bp.route('/<int:airline_id>', methods=['PUT'])
@jwt_required()
@manager_required()
@account_active_required()
def update_airline(airline_id):
    """
    Update airline information (manager only).
    
    PUT /api/airlines/{airline_id}
    Headers: Authorization: Bearer <token>
    Body: {
        "name": "Air Serbia",
        "country": "Serbia",
        "description": "Updated description",
        "logo_url": "https://example.com/new-logo.png"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Create DTO
        update_dto = AirlineUpdateDTO.from_dict(data)
        
        # Update airline
        response, status_code = AirlineService.update_airline(airline_id, update_dto)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to update airline: {str(e)}'}), 500


@airlines_bp.route('/<int:airline_id>', methods=['DELETE'])
@jwt_required()
@admin_required()
def delete_airline(airline_id):
    """
    Delete airline (admin only - soft delete).
    
    DELETE /api/airlines/{airline_id}
    Headers: Authorization: Bearer <token>
    """
    try:
        response, status_code = AirlineService.delete_airline(airline_id)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to delete airline: {str(e)}'}), 500