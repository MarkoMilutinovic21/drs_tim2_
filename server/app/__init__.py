"""
Flask application factory.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from flask_socketio import SocketIO
from redis import Redis
import os

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
socketio = SocketIO()
redis_client = None


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
    jwt.init_app(app)
    mail.init_app(app)
    
    # CORS configuration
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # SocketIO initialization
    socketio.init_app(app, cors_allowed_origins=app.config['CORS_ORIGINS'])
    
    # Redis initialization
    global redis_client
    try:
        redis_client = Redis.from_url(
            app.config['REDIS_URL'],
            decode_responses=True
        )
        redis_client.ping()
        app.logger.info("Redis connection established successfully")
    except Exception as e:
        app.logger.error(f"Redis connection failed: {str(e)}")
        redis_client = None
    
    # Create upload folder if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Serve uploaded files
    from flask import send_from_directory
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        """Serve uploaded files."""
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # JWT token blacklist check
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        """Check if JWT token is in blacklist (revoked)."""
        if redis_client:
            jti = jwt_payload['jti']
            token_in_redis = redis_client.get(f"blacklist:{jti}")
            return token_in_redis is not None
        return False

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """Handle expired token."""
        from flask import jsonify
        return jsonify({'error': 'Token has expired'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """Handle invalid token."""
        from flask import jsonify
        app.logger.error(f"Invalid token: {error}")
        return jsonify({'error': f'Invalid token: {error}'}), 422

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """Handle missing token."""
        from flask import jsonify
        app.logger.error(f"Missing token: {error}")
        return jsonify({'error': f'Authorization header is missing: {error}'}), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """Handle revoked token."""
        from flask import jsonify
        return jsonify({'error': 'Token has been revoked'}), 401
    
    # Register blueprints
    from app.routes import auth_bp, users_bp, airlines_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(airlines_bp, url_prefix='/api/airlines')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Health check endpoint."""
        return {
            'status': 'healthy',
            'service': 'flight-booking-server',
            'database': 'connected' if db.engine else 'disconnected',
            'redis': 'connected' if redis_client else 'disconnected'
        }, 200
    
    # Create database tables
    with app.app_context():
        db.create_all()
        app.logger.info("Database tables created successfully")
    
    return app


def get_redis():
    """Get Redis client instance."""
    return redis_client