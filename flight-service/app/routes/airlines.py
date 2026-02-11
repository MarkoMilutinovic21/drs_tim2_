"""
Airline management routes.
"""
from flask import Blueprint, request, jsonify
from app.services import AirlineService
from app.dto import AirlineCreateDTO, AirlineUpdateDTO

airlines_bp = Blueprint('airlines', __name__)


@airlines_bp.route('', methods=['POST'])
def create_airline():
    """
    Create a new airline.
    POST /api/airlines
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        created_by = data.get('created_by')
        if not created_by:
            return jsonify({'error': 'created_by is required'}), 400

        airline_dto = AirlineCreateDTO.from_dict(data)
        response, status_code = AirlineService.create_airline(airline_dto, created_by)
        return jsonify(response), status_code

    except Exception as e:
        return jsonify({'error': f'Failed to create airline: {str(e)}'}), 500


@airlines_bp.route('', methods=['GET'])
def get_all_airlines():
    """
    Get all airlines.
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
    Get airline by ID.
    GET /api/airlines/{airline_id}
    """
    try:
        response, status_code = AirlineService.get_airline_by_id(airline_id)
        return jsonify(response), status_code

    except Exception as e:
        return jsonify({'error': f'Failed to fetch airline: {str(e)}'}), 500


@airlines_bp.route('/<int:airline_id>', methods=['PUT'])
def update_airline(airline_id):
    """
    Update airline information.
    PUT /api/airlines/{airline_id}
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        update_dto = AirlineUpdateDTO.from_dict(data)
        response, status_code = AirlineService.update_airline(airline_id, update_dto)
        return jsonify(response), status_code

    except Exception as e:
        return jsonify({'error': f'Failed to update airline: {str(e)}'}), 500


@airlines_bp.route('/<int:airline_id>', methods=['DELETE'])
def delete_airline(airline_id):
    """
    Delete airline (soft delete).
    DELETE /api/airlines/{airline_id}
    """
    try:
        response, status_code = AirlineService.delete_airline(airline_id)
        return jsonify(response), status_code

    except Exception as e:
        return jsonify({'error': f'Failed to delete airline: {str(e)}'}), 500
