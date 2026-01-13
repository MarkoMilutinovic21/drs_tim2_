"""
Booking service for managing flight bookings.
"""
from flask import current_app
import requests
from app import db
from app.models import Flight, Booking
from app.dto import BookingCreateDTO
from app.utils import start_booking_process


class BookingService:
    """Service for handling booking operations."""
    
    @staticmethod
    def create_booking(booking_dto: BookingCreateDTO):
        """
        Create a new booking (async processing).
        
        Args:
            booking_dto: BookingCreateDTO with booking data
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        # Validate DTO
        errors = booking_dto.validate()
        if errors:
            return {'errors': errors}, 400
        
        # Get flight
        flight = db.session.get(Flight, booking_dto.flight_id)
        
        if not flight:
            return {'error': 'Flight not found'}, 404
        
        # Check if flight is available for booking
        if not flight.is_upcoming():
            return {'error': 'Flight is not available for booking'}, 400
        
        # Check if user has already booked this flight
        existing_booking = Booking.query.filter_by(
            flight_id=booking_dto.flight_id,
            user_id=booking_dto.user_id
        ).filter(Booking.status.in_(['PENDING', 'PROCESSING', 'COMPLETED'])).first()
        
        if existing_booking:
            return {'error': 'You have already booked this flight'}, 409
        
        try:
            # Check user balance (call Server API)
            server_url = current_app.config['SERVER_URL']
            
            try:
                user_response = requests.get(
                    f"{server_url}/api/users/{booking_dto.user_id}",
                    timeout=5
                )
                
                if user_response.status_code != 200:
                    return {'error': 'Failed to verify user'}, 400
                
                user_data = user_response.json().get('user', {})
                account_balance = float(user_data.get('account_balance', 0))
                
                # Check if user has sufficient balance
                if account_balance < float(flight.ticket_price):
                    return {'error': 'Insufficient balance'}, 400
                
            except requests.RequestException as e:
                current_app.logger.error(f"Failed to verify user balance: {str(e)}")
                return {'error': 'Failed to verify user balance'}, 500
            
            # Deduct balance from user (call Server API)
            try:
                deduct_response = requests.post(
                    f"{server_url}/api/users/{booking_dto.user_id}/deduct",
                    json={'amount': float(flight.ticket_price)},
                    timeout=5
                )
                
                if deduct_response.status_code != 200:
                    return {'error': 'Failed to deduct balance'}, 500
            
            except requests.RequestException as e:
                current_app.logger.error(f"Failed to deduct balance: {str(e)}")
                return {'error': 'Failed to process payment'}, 500
            
            # Create booking with PROCESSING status
            new_booking = Booking(
                flight_id=booking_dto.flight_id,
                user_id=booking_dto.user_id,
                ticket_price=flight.ticket_price
            )
            new_booking.mark_processing()
            
            db.session.add(new_booking)
            db.session.commit()
            
            # Start async processing (multiprocessing)
            start_booking_process(
                flight_id=booking_dto.flight_id,
                user_id=booking_dto.user_id,
                ticket_price=float(flight.ticket_price),
                app_config=current_app.config
            )
            
            return {
                'message': 'Booking is being processed asynchronously',
                'booking': new_booking.to_dict()
            }, 202  # 202 Accepted
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating booking: {str(e)}")
            return {'error': 'Failed to create booking'}, 500
    
    @staticmethod
    def get_booking_by_id(booking_id):
        """
        Get booking by ID.
        
        Args:
            booking_id: Booking ID
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        booking = db.session.get(Booking, booking_id)
        
        if not booking:
            return {'error': 'Booking not found'}, 404
        
        return {
            'booking': booking.to_dict()
        }, 200
    
    @staticmethod
    def get_user_bookings(user_id):
        """
        Get all bookings for a user.
        
        Args:
            user_id: User ID
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        try:
            bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.created_at.desc()).all()
            
            # Include flight details
            bookings_data = []
            for booking in bookings:
                booking_dict = booking.to_dict()
                
                # Get flight details
                flight = db.session.get(Flight, booking.flight_id)
                if flight:
                    booking_dict['flight'] = flight.to_dict()
                
                bookings_data.append(booking_dict)
            
            return {
                'bookings': bookings_data,
                'total': len(bookings_data)
            }, 200
        
        except Exception as e:
            current_app.logger.error(f"Error fetching user bookings: {str(e)}")
            return {'error': 'Failed to fetch bookings'}, 500
    
    @staticmethod
    def get_flight_bookings(flight_id):
        """
        Get all bookings for a flight.
        
        Args:
            flight_id: Flight ID
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        try:
            bookings = Booking.query.filter_by(flight_id=flight_id).all()
            bookings_data = [booking.to_dict() for booking in bookings]
            
            return {
                'bookings': bookings_data,
                'total': len(bookings_data)
            }, 200
        
        except Exception as e:
            current_app.logger.error(f"Error fetching flight bookings: {str(e)}")
            return {'error': 'Failed to fetch bookings'}, 500