"""
Async tasks using multiprocessing for booking operations.
"""
import time
from multiprocessing import Process
from flask import current_app


def process_booking_async(flight_id, user_id, ticket_price, app_config):
    """
    Process booking asynchronously (simulates long-running operation).
    
    This function runs in a separate process.
    
    Args:
        flight_id: Flight ID
        user_id: User ID
        ticket_price: Ticket price
        app_config: Flask app configuration dict
    """
    # Import here to avoid circular imports in subprocess
    from app import create_app, db
    from app.models import Booking, Flight
    import requests
    
    # Create app context in subprocess
    app = create_app()
    
    with app.app_context():
        try:
            # Simulate long-running processing (sleep for testing)
            time.sleep(5)  # Simulate 5 seconds of processing
            
            # Find the booking
            booking = Booking.query.filter_by(
                flight_id=flight_id,
                user_id=user_id,
                status='PROCESSING'
            ).first()
            
            if not booking:
                print(f"Booking not found for user {user_id} and flight {flight_id}")
                return
            
            # Get flight details
            flight = db.session.get(Flight, flight_id)
            
            if not flight:
                booking.mark_cancelled()
                db.session.commit()
                print(f"Flight {flight_id} not found")
                return
            
            # Check if flight is still available (approved and upcoming)
            if not flight.is_upcoming():
                booking.mark_cancelled()
                db.session.commit()
                
                # Refund user (call Server API)
                try:
                    server_url = app.config['SERVER_URL']
                    requests.post(
                        f"{server_url}/api/users/{user_id}/refund",
                        json={'amount': float(ticket_price)},
                        timeout=5
                    )
                except Exception as e:
                    print(f"Failed to refund user: {str(e)}")
                
                print(f"Flight {flight_id} is not available for booking")
                return
            
            # Mark booking as completed
            booking.mark_completed()
            db.session.commit()
            
            print(f"Booking completed: User {user_id}, Flight {flight_id}")
        
        except Exception as e:
            print(f"Error processing booking: {str(e)}")
            
            # Try to cancel booking on error
            try:
                booking = Booking.query.filter_by(
                    flight_id=flight_id,
                    user_id=user_id,
                    status='PROCESSING'
                ).first()
                
                if booking:
                    booking.mark_cancelled()
                    db.session.commit()
            except:
                pass


def start_booking_process(flight_id, user_id, ticket_price, app_config):
    """
    Start async booking process.
    
    Args:
        flight_id: Flight ID
        user_id: User ID
        ticket_price: Ticket price
        app_config: Flask app configuration dict
    
    Returns:
        Process: Started process
    """
    process = Process(
        target=process_booking_async,
        args=(flight_id, user_id, ticket_price, app_config)
    )
    process.start()
    return process