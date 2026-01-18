"""
Notification routes for internal service events.
"""
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.models import User
from app.services.email_service import EmailService
from app import db
import os
import uuid

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


@notifications_bp.route('/flight-report', methods=['POST'])
def notify_flight_report():
    """
    Send flight report PDF to admin (internal use).
    
    POST /api/notifications/flight-report
    Body: multipart/form-data with fields:
        - user_id
        - report_type
        - file (PDF)
    """
    try:
        user_id = request.form.get('user_id', type=int)
        report_type = request.form.get('report_type')
        
        if not user_id or not report_type:
            return jsonify({'error': 'user_id and report_type are required'}), 400
        
        if 'file' not in request.files:
            return jsonify({'error': 'PDF file is required'}), 400
        
        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({'error': 'Invalid PDF file'}), 400
        
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        filename = secure_filename(file.filename) or 'flight_report.pdf'
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        pdf_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
        
        file.save(pdf_path)
        
        try:
            EmailService.send_pdf_report_email(user, report_type, pdf_path)
        finally:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        
        return jsonify({'message': 'Report email sent'}), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to send report: {str(e)}'}), 500
