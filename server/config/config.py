"""
Configuration module for Flask application.
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value == '':
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


class Config:
    """Base configuration class."""
    
    # Flask
    SECRET_KEY = _require_env('SECRET_KEY')
    DEBUG = _require_env('DEBUG') == 'True'
    
    # Database
    SQLALCHEMY_DATABASE_URI = _require_env('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG
    
    # Redis
    REDIS_URL = _require_env('REDIS_URL')
    
    # JWT
    JWT_SECRET_KEY = _require_env('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(_require_env('JWT_ACCESS_TOKEN_EXPIRES'))
    )
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']
    
    # Email Configuration
    MAIL_SERVER = _require_env('MAIL_SERVER')
    MAIL_PORT = int(_require_env('MAIL_PORT'))
    MAIL_USE_TLS = _require_env('MAIL_USE_TLS') == 'True'
    MAIL_USE_SSL = _require_env('MAIL_USE_SSL') == 'True'
    MAIL_USERNAME = _require_env('MAIL_USERNAME')
    MAIL_PASSWORD = _require_env('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = _require_env('MAIL_DEFAULT_SENDER')
    
    # CORS
    CORS_ORIGINS = _require_env('CORS_ORIGINS').split(',')
    
    # Flight Service
    FLIGHT_SERVICE_URL = _require_env('FLIGHT_SERVICE_URL')
    
    # Login Security
    MAX_LOGIN_ATTEMPTS = int(_require_env('MAX_LOGIN_ATTEMPTS'))
    LOCKOUT_DURATION = int(_require_env('LOCKOUT_DURATION'))
    
    # Server
    HOST = _require_env('HOST')
    PORT = int(_require_env('PORT'))
    
    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


class DevelopmentConfig(Config):    # kada je ukljucen prikazuje sql upite
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):     # kada je iskljucen bez sql upita
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):    # koristi privremenu bazu u memoriji
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
