"""
Flight service for managing flight operations.
"""
from flask import current_app
from datetime import datetime
from app import db
from app.models import Flight, Booking
from app.dto import FlightCreateDTO, FlightUpdateDTO, FlightApprovalDTO, FlightSearchDTO


class FlightService:
    """Service for handling flight operations."""
    
    @staticmethod
    def create_flight(flight_dto: FlightCreateDTO, created_by):
        """
        Create a new flight (manager only).
        
        Args:
            flight_dto: FlightCreateDTO with flight data
            created_by: User ID of the creator (manager)
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        # Validate DTO
        errors = flight_dto.validate()
        if errors:
            return {'errors': errors}, 400
        
        try:
            new_flight = Flight(
                name=flight_dto.name,
                airline_id=flight_dto.airline_id,
                distance_km=flight_dto.distance_km,
                duration_minutes=flight_dto.duration_minutes,
                departure_time=flight_dto.departure_time,
                departure_airport=flight_dto.departure_airport,
                arrival_airport=flight_dto.arrival_airport,
                ticket_price=flight_dto.ticket_price,
                created_by=created_by
            )
            
            db.session.add(new_flight)
            db.session.commit()
            
            # TODO: Send WebSocket notification to admin
            # This will be implemented in routes
            
            return {
                'message': 'Flight created successfully and pending approval',
                'flight': new_flight.to_dict()
            }, 201
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating flight: {str(e)}")
            return {'error': 'Failed to create flight'}, 500
    
    @staticmethod
    def get_flight_by_id(flight_id):
        """
        Get flight by ID.
        
        Args:
            flight_id: Flight ID
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        flight = db.session.get(Flight, flight_id)
        
        if not flight:
            return {'error': 'Flight not found'}, 404
        
        return {
            'flight': flight.to_dict()
        }, 200
    
    @staticmethod
    def get_all_flights(search_dto: FlightSearchDTO = None):
        """
        Get all flights with optional filters.
        
        Args:
            search_dto: FlightSearchDTO with search parameters
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        try:
            query = Flight.query
            
            # Apply filters if search_dto is provided
            if search_dto:
                if search_dto.name:
                    query = query.filter(Flight.name.ilike(f"%{search_dto.name}%"))
                
                if search_dto.airline_id:
                    query = query.filter_by(airline_id=search_dto.airline_id)
                
                if search_dto.status:
                    query = query.filter_by(status=search_dto.status)
            
            flights = query.order_by(Flight.departure_time.asc()).all()
            flights_data = [flight.to_dict() for flight in flights]
            
            return {
                'flights': flights_data,
                'total': len(flights_data)
            }, 200
        
        except Exception as e:
            current_app.logger.error(f"Error fetching flights: {str(e)}")
            return {'error': 'Failed to fetch flights'}, 500
    
    @staticmethod
    def get_flights_by_tab():
        """
        Get flights organized by tabs (upcoming, ongoing, completed/cancelled).
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        try:
            now = datetime.utcnow()
            
            # Get all approved flights
            all_flights = Flight.query.filter_by(status='APPROVED').all()
            
            upcoming = []
            ongoing = []
            completed_cancelled = []
            completed_ids = set()
            
            for flight in all_flights:
                if flight.is_upcoming():
                    upcoming.append(flight.to_dict())
                elif flight.is_ongoing():
                    ongoing.append(flight.to_dict())
                elif flight.is_completed():
                    # Mark as completed if not already
                    if flight.status == 'APPROVED':
                        flight.complete()
                    completed_cancelled.append(flight.to_dict())
                    completed_ids.add(flight.id)
            
            # Get cancelled flights
            cancelled_flights = Flight.query.filter_by(status='CANCELLED').all()
            completed_cancelled.extend([f.to_dict() for f in cancelled_flights])
            
            # Get completed flights
            completed_flights = Flight.query.filter_by(status='COMPLETED').all()
            for flight in completed_flights:
                if flight.id in completed_ids:
                    continue
                completed_cancelled.append(flight.to_dict())
            
            db.session.commit()
            
            return {
                'upcoming': upcoming,
                'ongoing': ongoing,
                'completed_cancelled': completed_cancelled
            }, 200
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error fetching flights by tab: {str(e)}")
            return {'error': 'Failed to fetch flights'}, 500
    
    @staticmethod
    def get_pending_flights():
        """
        Get all pending flights (for admin approval).
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        try:
            pending_flights = Flight.query.filter_by(status='PENDING').order_by(Flight.created_at.desc()).all()
            flights_data = [flight.to_dict() for flight in pending_flights]
            
            return {
                'flights': flights_data,
                'total': len(flights_data)
            }, 200
        
        except Exception as e:
            current_app.logger.error(f"Error fetching pending flights: {str(e)}")
            return {'error': 'Failed to fetch pending flights'}, 500
    
    @staticmethod
    def approve_reject_flight(flight_id, approval_dto: FlightApprovalDTO):
        """
        Approve or reject a flight (admin only).
        
        Args:
            flight_id: Flight ID
            approval_dto: FlightApprovalDTO with action and reason
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        flight = db.session.get(Flight, flight_id)
        
        if not flight:
            return {'error': 'Flight not found'}, 404
        
        if flight.status != 'PENDING' and flight.status != 'REJECTED':
            return {'error': 'Flight is not pending approval'}, 400
        
        # Validate DTO
        errors = approval_dto.validate()
        if errors:
            return {'errors': errors}, 400
        
        try:
            if approval_dto.action == 'approve':
                flight.approve()
                message = 'Flight approved successfully'
            else:  # reject
                flight.reject(approval_dto.rejection_reason)
                message = 'Flight rejected'
            
            db.session.commit()
            
            return {
                'message': message,
                'flight': flight.to_dict()
            }, 200
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error approving/rejecting flight: {str(e)}")
            return {'error': 'Failed to process flight approval'}, 500
    
    @staticmethod
    def update_flight(flight_id, update_dto: FlightUpdateDTO):
        """
        Update flight information (manager only, for rejected flights).
        
        Args:
            flight_id: Flight ID
            update_dto: FlightUpdateDTO with updated data
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        flight = db.session.get(Flight, flight_id)
        
        if not flight:
            return {'error': 'Flight not found'}, 404
        
        # Only rejected flights can be updated
        if flight.status != 'REJECTED':
            return {'error': 'Only rejected flights can be updated'}, 400
        
        # Validate DTO
        errors = update_dto.validate()
        if errors:
            return {'errors': errors}, 400
        
        try:
            if update_dto.name:
                flight.name = update_dto.name
            
            if update_dto.distance_km:
                flight.distance_km = update_dto.distance_km
            
            if update_dto.duration_minutes:
                flight.duration_minutes = update_dto.duration_minutes
            
            if update_dto.departure_time:
                flight.departure_time = update_dto.departure_time
            
            if update_dto.departure_airport:
                flight.departure_airport = update_dto.departure_airport
            
            if update_dto.arrival_airport:
                flight.arrival_airport = update_dto.arrival_airport
            
            if update_dto.ticket_price:
                flight.ticket_price = update_dto.ticket_price
            
            # Reset to pending after update
            flight.status = 'PENDING'
            flight.rejection_reason = None
            
            db.session.commit()
            
            return {
                'message': 'Flight updated and resubmitted for approval',
                'flight': flight.to_dict()
            }, 200
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating flight: {str(e)}")
            return {'error': 'Failed to update flight'}, 500
    
    @staticmethod
    def cancel_flight(flight_id):
        """
        Cancel flight (admin only).
        
        Args:
            flight_id: Flight ID
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        flight = db.session.get(Flight, flight_id)
        
        if not flight:
            return {'error': 'Flight not found'}, 404
        
        # Can only cancel approved flights that haven't started
        if flight.status != 'APPROVED':
            return {'error': 'Only approved flights can be cancelled'}, 400
        
        if not flight.is_upcoming():
            return {'error': 'Cannot cancel flight that has already started or completed'}, 400
        
        try:
            # Get all bookings for this flight
            bookings = Booking.query.filter_by(flight_id=flight_id, status='COMPLETED').all()
            
            # Cancel flight
            flight.cancel()
            db.session.commit()
            
            # Refund all users (this will be done via Server API in routes)
            user_ids = [booking.user_id for booking in bookings]
            
            return {
                'message': 'Flight cancelled successfully',
                'flight': flight.to_dict(),
                'affected_users': user_ids
            }, 200
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error cancelling flight: {str(e)}")
            return {'error': 'Failed to cancel flight'}, 500
    
    @staticmethod
    def delete_flight(flight_id):
        """
        Delete flight (admin only).
        
        Args:
            flight_id: Flight ID
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        flight = db.session.get(Flight, flight_id)
        
        if not flight:
            return {'error': 'Flight not found'}, 404
        
        try:
            db.session.delete(flight)
            db.session.commit()
            
            return {
                'message': 'Flight deleted successfully'
            }, 200
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error deleting flight: {str(e)}")
            return {'error': 'Failed to delete flight'}, 500
