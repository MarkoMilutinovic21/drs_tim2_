
"""
Booking management routes.
"""
from flask import Blueprint, request, jsonify
from app.services import BookingService
from app.dto import BookingCreateDTO

bookings_bp = Blueprint('bookings', __name__)


@bookings_bp.route('', methods=['POST'])
def create_booking():
    """
    Create a new booking (buy ticket).
    
    POST /api/bookings
    Body: {
        "flight_id": 1,
        "user_id": 3
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Create DTO
        booking_dto = BookingCreateDTO.from_dict(data)
        
        # Create booking (async processing)
        response, status_code = BookingService.create_booking(booking_dto)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to create booking: {str(e)}'}), 500


@bookings_bp.route('/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    """
    Get booking by ID.
    
    GET /api/bookings/{booking_id}
    """
    try:
        response, status_code = BookingService.get_booking_by_id(booking_id)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch booking: {str(e)}'}), 500


@bookings_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_bookings(user_id):
    """
    Get all bookings for a user.
    
    GET /api/bookings/user/{user_id}
    """
    try:
        response, status_code = BookingService.get_user_bookings(user_id)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch user bookings: {str(e)}'}), 500


@bookings_bp.route('/flight/<int:flight_id>', methods=['GET'])
def get_flight_bookings(flight_id):
    """
    Get all bookings for a flight.
    
    GET /api/bookings/flight/{flight_id}
    """
    try:
        response, status_code = BookingService.get_flight_bookings(flight_id)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch flight bookings: {str(e)}'}), 500