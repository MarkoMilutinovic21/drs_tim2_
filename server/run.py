"""
Application entry point.
"""
import os
from app import create_app, socketio

# Get configuration from environment
config_name = os.getenv('FLASK_ENV', 'development')

# Create Flask app
app = create_app(config_name)

if __name__ == '__main__':
    # Run with SocketIO support
    socketio.run(
        app,
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
