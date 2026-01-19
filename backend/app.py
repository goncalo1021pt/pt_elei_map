import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config import get_config
from src.models import db
from src.routes import register_routes
from flask import Flask
from flask_cors import CORS


def create_app(config=None):
    """Application factory"""
    app = Flask(__name__)

    # Load configuration
    if config is None:
        config = get_config()
    app.config.from_object(config)

    # Initialize database
    db.init_app(app)

    # Enable CORS
    CORS(app)

    # Register routes
    register_routes(app)

    # Create tables on startup
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
