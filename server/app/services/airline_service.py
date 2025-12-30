"""
Airline service for managing airline companies.
"""
from flask import current_app
from app import db
from app.models import Airline
from app.dto import AirlineCreateDTO, AirlineUpdateDTO


class AirlineService:
    """Service for handling airline operations."""
    
    @staticmethod
    def create_airline(airline_dto: AirlineCreateDTO, created_by):
        """
        Create a new airline.
        
        Args:
            airline_dto: AirlineCreateDTO with airline data
            created_by: User ID of the creator (manager)
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        # Validate DTO
        errors = airline_dto.validate()
        if errors:
            return {'errors': errors}, 400
        
        # Check if airline with same name or code exists
        existing_airline = Airline.query.filter(
            (Airline.name == airline_dto.name) | (Airline.code == airline_dto.code.upper())
        ).first()
        
        if existing_airline:
            return {'error': 'Airline with this name or code already exists'}, 409
        
        try:
            new_airline = Airline(
                name=airline_dto.name,
                code=airline_dto.code,
                country=airline_dto.country,
                created_by=created_by,
                description=airline_dto.description,
                logo_url=airline_dto.logo_url
            )
            
            db.session.add(new_airline)
            db.session.commit()
            
            return {
                'message': 'Airline created successfully',
                'airline': new_airline.to_dict()
            }, 201
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating airline: {str(e)}")
            return {'error': 'Failed to create airline'}, 500
    
    @staticmethod
    def get_airline_by_id(airline_id):
        """
        Get airline by ID.
        
        Args:
            airline_id: Airline ID
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        airline = db.session.get(Airline, airline_id)
        
        if not airline:
            return {'error': 'Airline not found'}, 404
        
        return {
            'airline': airline.to_dict()
        }, 200
    
    @staticmethod
    def get_all_airlines(active_only=True):
        """
        Get all airlines.
        
        Args:
            active_only: If True, return only active airlines
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        try:
            query = Airline.query
            
            if active_only:
                query = query.filter_by(is_active=True)
            
            airlines = query.order_by(Airline.name).all()
            airlines_data = [airline.to_dict() for airline in airlines]
            
            return {
                'airlines': airlines_data,
                'total': len(airlines_data)
            }, 200
        
        except Exception as e:
            current_app.logger.error(f"Error fetching airlines: {str(e)}")
            return {'error': 'Failed to fetch airlines'}, 500
    
    @staticmethod
    def update_airline(airline_id, update_dto: AirlineUpdateDTO):
        """
        Update airline information.
        
        Args:
            airline_id: Airline ID
            update_dto: AirlineUpdateDTO with updated data
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        airline = db.session.get(Airline, airline_id)
        
        if not airline:
            return {'error': 'Airline not found'}, 404
        
        # Validate DTO
        errors = update_dto.validate()
        if errors:
            return {'errors': errors}, 400
        
        try:
            if update_dto.name:
                # Check if name is taken by another airline
                existing = Airline.query.filter(
                    Airline.name == update_dto.name,
                    Airline.id != airline_id
                ).first()
                if existing:
                    return {'error': 'Airline name already exists'}, 409
                airline.name = update_dto.name
            
            if update_dto.country:
                airline.country = update_dto.country
            
            if update_dto.description is not None:
                airline.description = update_dto.description
            
            if update_dto.logo_url is not None:
                airline.logo_url = update_dto.logo_url
            
            db.session.commit()
            
            return {
                'message': 'Airline updated successfully',
                'airline': airline.to_dict()
            }, 200
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating airline: {str(e)}")
            return {'error': 'Failed to update airline'}, 500
    
    @staticmethod
    def delete_airline(airline_id):
        """
        Delete airline (soft delete - set is_active to False).
        
        Args:
            airline_id: Airline ID
        
        Returns:
            tuple: (dict, int) - (response_data, status_code)
        """
        airline = db.session.get(Airline, airline_id)
        
        if not airline:
            return {'error': 'Airline not found'}, 404
        
        try:
            # Soft delete
            airline.is_active = False
            db.session.commit()
            
            return {
                'message': 'Airline deleted successfully'
            }, 200
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error deleting airline: {str(e)}")
            return {'error': 'Failed to delete airline'}, 500