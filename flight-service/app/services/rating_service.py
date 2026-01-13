"""
Rating service for managing flight ratings.
"""
from flask import current_app
from app import db
from app.models import Flight, Booking, Rating
from app.dto import RatingCreateDTO


class RatingService:
    """Service for handling rating operations."""
    
    @staticmethod
    def create_rating(rating_dto: RatingCreateDTO):
        """
        Create a new rating for a completed flight.
        
        Args:
            rating_dto: RatingCreateDTO with rating data
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        # Validate DTO
        errors = rating_dto.validate()
        if errors:
            return {'errors': errors}, 400
        
        # Get flight
        flight = db.session.get(Flight, rating_dto.flight_id)
        
        if not flight:
            return {'error': 'Flight not found'}, 404
        
        # Check if flight is completed
        if not flight.is_completed():
            return {'error': 'Can only rate completed flights'}, 400
        
        # Check if user has booked this flight
        booking = Booking.query.filter_by(
            flight_id=rating_dto.flight_id,
            user_id=rating_dto.user_id,
            status='COMPLETED'
        ).first()
        
        if not booking:
            return {'error': 'You must book and complete this flight to rate it'}, 403
        
        # Check if user has already rated this flight
        existing_rating = Rating.query.filter_by(
            flight_id=rating_dto.flight_id,
            user_id=rating_dto.user_id
        ).first()
        
        if existing_rating:
            return {'error': 'You have already rated this flight'}, 409
        
        try:
            new_rating = Rating(
                flight_id=rating_dto.flight_id,
                user_id=rating_dto.user_id,
                rating=rating_dto.rating,
                comment=rating_dto.comment
            )
            
            db.session.add(new_rating)
            db.session.commit()
            
            return {
                'message': 'Rating created successfully',
                'rating': new_rating.to_dict()
            }, 201
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating rating: {str(e)}")
            return {'error': 'Failed to create rating'}, 500
    
    @staticmethod
    def get_rating_by_id(rating_id):
        """
        Get rating by ID.
        
        Args:
            rating_id: Rating ID
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        rating = db.session.get(Rating, rating_id)
        
        if not rating:
            return {'error': 'Rating not found'}, 404
        
        return {
            'rating': rating.to_dict()
        }, 200
    
    @staticmethod
    def get_flight_ratings(flight_id):
        """
        Get all ratings for a flight.
        
        Args:
            flight_id: Flight ID
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        try:
            ratings = Rating.query.filter_by(flight_id=flight_id).order_by(Rating.created_at.desc()).all()
            ratings_data = [rating.to_dict() for rating in ratings]
            
            # Calculate average rating
            average_rating = Rating.get_average_rating(flight_id)
            
            return {
                'ratings': ratings_data,
                'total': len(ratings_data),
                'average_rating': average_rating
            }, 200
        
        except Exception as e:
            current_app.logger.error(f"Error fetching flight ratings: {str(e)}")
            return {'error': 'Failed to fetch ratings'}, 500
    
    @staticmethod
    def get_all_ratings():
        """
        Get all ratings (admin only).
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        try:
            ratings = Rating.query.order_by(Rating.created_at.desc()).all()
            
            # Include flight details
            ratings_data = []
            for rating in ratings:
                rating_dict = rating.to_dict()
                
                # Get flight details
                flight = db.session.get(Flight, rating.flight_id)
                if flight:
                    rating_dict['flight'] = {
                        'id': flight.id,
                        'name': flight.name,
                        'departure_airport': flight.departure_airport,
                        'arrival_airport': flight.arrival_airport
                    }
                
                ratings_data.append(rating_dict)
            
            return {
                'ratings': ratings_data,
                'total': len(ratings_data)
            }, 200
        
        except Exception as e:
            current_app.logger.error(f"Error fetching all ratings: {str(e)}")
            return {'error': 'Failed to fetch ratings'}, 500