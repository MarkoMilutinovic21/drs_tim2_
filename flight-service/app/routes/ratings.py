"""
Rating management routes.
"""
from flask import Blueprint, request, jsonify
from app.services import RatingService
from app.dto import RatingCreateDTO

ratings_bp = Blueprint('ratings', __name__)


@ratings_bp.route('', methods=['POST'])
def create_rating():
    """
    Create a new rating for a completed flight.
    
    POST /api/ratings
    Body: {
        "flight_id": 1,
        "user_id": 3,
        "rating": 5,
        "comment": "Excellent flight!"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Create DTO
        rating_dto = RatingCreateDTO.from_dict(data)
        
        # Create rating
        response, status_code = RatingService.create_rating(rating_dto)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to create rating: {str(e)}'}), 500


@ratings_bp.route('/<int:rating_id>', methods=['GET'])
def get_rating(rating_id):
    """
    Get rating by ID.
    
    GET /api/ratings/{rating_id}
    """
    try:
        response, status_code = RatingService.get_rating_by_id(rating_id)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch rating: {str(e)}'}), 500


@ratings_bp.route('/flight/<int:flight_id>', methods=['GET'])
def get_flight_ratings(flight_id):
    """
    Get all ratings for a flight.
    
    GET /api/ratings/flight/{flight_id}
    """
    try:
        response, status_code = RatingService.get_flight_ratings(flight_id)
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch flight ratings: {str(e)}'}), 500


@ratings_bp.route('', methods=['GET'])
def get_all_ratings():
    """
    Get all ratings (admin only).
    
    GET /api/ratings
    """
    try:
        response, status_code = RatingService.get_all_ratings()
        
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'error': f'Failed to fetch ratings: {str(e)}'}), 500