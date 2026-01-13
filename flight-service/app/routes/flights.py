"""
Flight management routes.
"""
from flask import Blueprint, request, jsonify
from flask_socketio import emit
from app.services import FlightService
from app.dto import FlightCreateDTO, FlightUpdateDTO, FlightApprovalDTO, FlightSearchDTO
from app import socketio
import requests

flights_bp = Blueprint('flights', __name__)


@flights_bp.route('', methods=['POST'])
def create_flight():
    """
    Create a new flight (manager only).
    
    POST /api/flights
    Headers: Authorization: Bearer <token> (validated on Server side)
    Body: {
        "name": "BEG-NYC-001",
        "airline_id": 1,
        "distance_km": 7500,
        "duration_minutes": 1,
        "departure_time": "2025-01-15T10:00:00Z",
        "departure_airport": "Belgrade Nikola Tesla",
        "arrival_airport": "JFK New York",
        "ticket_price": 500.00,
        "created_by": 2
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        created_by = data.get('created_by')
        if not created_by:
            return jsonify({'error': 'created_by is required'}), 400
        
        # Create DTO
        flight_dto = FlightCreateDTO.from_dict(data)
        
        # Create flight
        response, status_code = FlightService.create_flight(flight_dto, created_by)
        
        # If successful, send WebSocket notification to admin
        if status_code == 201:
            flight_data = response.get('flight')
            socketio.emit('new_flight', flight_data, namespace='/', broadcast=True)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to create flight: {str(e)}'}), 500


@flights_bp.route('', methods=['GET'])
def get_all_flights():
    """
    Get all flights with optional filters.
    
    GET /api/flights?name=BEG&airline_id=1&status=APPROVED
    """
    try:
        # Get query parameters
        search_dto = FlightSearchDTO.from_dict({
            'name': request.args.get('name'),
            'airline_id': request.args.get('airline_id', type=int),
            'status': request.args.get('status')
        })
        
        response, status_code = FlightService.get_all_flights(search_dto)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch flights: {str(e)}'}), 500


@flights_bp.route('/tabs', methods=['GET'])
def get_flights_by_tab():
    """
    Get flights organized by tabs (upcoming, ongoing, completed/cancelled).
    
    GET /api/flights/tabs
    """
    try:
        response, status_code = FlightService.get_flights_by_tab()
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch flights by tab: {str(e)}'}), 500


@flights_bp.route('/pending', methods=['GET'])
def get_pending_flights():
    """
    Get all pending flights (for admin approval).
    
    GET /api/flights/pending
    """
    try:
        response, status_code = FlightService.get_pending_flights()
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch pending flights: {str(e)}'}), 500


@flights_bp.route('/<int:flight_id>', methods=['GET'])
def get_flight(flight_id):
    """
    Get flight by ID.
    
    GET /api/flights/{flight_id}
    """
    try:
        response, status_code = FlightService.get_flight_by_id(flight_id)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch flight: {str(e)}'}), 500


@flights_bp.route('/<int:flight_id>/approve', methods=['POST'])
def approve_reject_flight(flight_id):
    """
    Approve or reject a flight (admin only).
    
    POST /api/flights/{flight_id}/approve
    Body: {
        "action": "approve"  // or "reject"
        "rejection_reason": "Reason for rejection"  // required if action is "reject"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Create DTO
        approval_dto = FlightApprovalDTO.from_dict(data)
        
        # Approve/reject flight
        response, status_code = FlightService.approve_reject_flight(flight_id, approval_dto)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to process flight approval: {str(e)}'}), 500


@flights_bp.route('/<int:flight_id>', methods=['PUT'])
def update_flight(flight_id):
    """
    Update flight information (manager only, for rejected flights).
    
    PUT /api/flights/{flight_id}
    Body: {
        "name": "Updated name",
        "distance_km": 8000,
        "duration_minutes": 2,
        "departure_time": "2025-01-20T12:00:00Z",
        "departure_airport": "Updated airport",
        "arrival_airport": "Updated airport",
        "ticket_price": 600.00
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Create DTO
        update_dto = FlightUpdateDTO.from_dict(data)
        
        # Update flight
        response, status_code = FlightService.update_flight(flight_id, update_dto)
        
        # If successful, send WebSocket notification to admin (resubmitted)
        if status_code == 200:
            flight_data = response.get('flight')
            socketio.emit('new_flight', flight_data, namespace='/', broadcast=True)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to update flight: {str(e)}'}), 500


@flights_bp.route('/<int:flight_id>/cancel', methods=['POST'])
def cancel_flight(flight_id):
    """
    Cancel flight (admin only).
    
    POST /api/flights/{flight_id}/cancel
    """
    try:
        response, status_code = FlightService.cancel_flight(flight_id)
        
        # If successful, send email notifications to all affected users
        if status_code == 200:
            affected_users = response.get('affected_users', [])
            flight_data = response.get('flight')
            
            # Send email notifications via Server
            try:
                from flask import current_app
                server_url = current_app.config['SERVER_URL']
                
                for user_id in affected_users:
                    # Notify user about cancellation
                    requests.post(
                        f"{server_url}/api/notifications/flight-cancelled",
                        json={
                            'user_id': user_id,
                            'flight': flight_data
                        },
                        timeout=5
                    )
            except Exception as e:
                current_app.logger.error(f"Failed to send cancellation emails: {str(e)}")
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to cancel flight: {str(e)}'}), 500


@flights_bp.route('/<int:flight_id>', methods=['DELETE'])
def delete_flight(flight_id):
    """
    Delete flight (admin only).
    
    DELETE /api/flights/{flight_id}
    """
    try:
        response, status_code = FlightService.delete_flight(flight_id)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to delete flight: {str(e)}'}), 500


# WebSocket event handlers
@socketio.on('connect', namespace='/')
def handle_connect():
    """Handle client connection."""
    print('Client connected to Flight Service WebSocket')


@socketio.on('disconnect', namespace='/')
def handle_disconnect():
    """Handle client disconnection."""
    print('Client disconnected from Flight Service WebSocket')