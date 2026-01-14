"""
Notification routes for internal service events.
"""
from flask import Blueprint, request, jsonify
from app.models import User
from app.services.email_service import EmailService
from app import db

notifications_bp = Blueprint('notifications', __name__)


@notifications_bp.route('/flight-cancelled', methods=['POST'])
def notify_flight_cancelled():
    """
    Send flight cancellation email to a user (internal use).
    
    POST /api/notifications/flight-cancelled
    Body: {
        "user_id": 1,
        "flight": { ... }
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user_id = data.get('user_id')
        flight = data.get('flight')
        
        if not user_id or not flight:
            return jsonify({'error': 'user_id and flight are required'}), 400
        
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        EmailService.send_flight_cancelled_email(user, flight)
        
        return jsonify({'message': 'Notification sent'}), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to send notification: {str(e)}'}), 500
