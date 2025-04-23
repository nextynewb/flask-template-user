from flask import Flask
from app.config.config import Config
from app.routes import register_routes
from app.models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register routes
    register_routes(app)
    
    return app
