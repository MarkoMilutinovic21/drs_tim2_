"""
Flask application factory for Flight Service.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_socketio import SocketIO
import os

# Initialize extensions
db = SQLAlchemy()
socketio = SocketIO()


def create_app(config_name='default'):
    """
    Application factory pattern.
    
    Args:
        config_name: Configuration to use (development, production, testing)
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    
    # CORS configuration
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # SocketIO initialization
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Create PDF folder if it doesn't exist
    if not os.path.exists(app.config['PDF_FOLDER']):
        os.makedirs(app.config['PDF_FOLDER'])
    
    # Register blueprints
    from app.routes import flights_bp, bookings_bp, ratings_bp
    
    app.register_blueprint(flights_bp, url_prefix='/api/flights')
    app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
    app.register_blueprint(ratings_bp, url_prefix='/api/ratings')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Health check endpoint."""
        return {
            'status': 'healthy',
            'service': 'flight-service',
            'database': 'connected' if db.engine else 'disconnected'
        }, 200
    
    # Create database tables
    with app.app_context():
        db.create_all()
        app.logger.info("Database tables created successfully")
    
    return app