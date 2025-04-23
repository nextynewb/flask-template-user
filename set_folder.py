import os
import sys

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    else:
        print(f"Directory already exists: {path}")

def create_file(path, content=""):
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    
    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write(content)
        print(f"Created file: {path}")
    else:
        print(f"File already exists: {path}")

def setup_flask_mvc_structure():
    # Create main directories
    create_directory("app")
    create_directory("app/controllers")
    create_directory("app/models")
    create_directory("app/routes")
    create_directory("app/utils")
    create_directory("app/middlewares")
    create_directory("app/config")
    create_directory("migrations")
    create_directory("tests")
    create_directory("tests/unit")
    create_directory("tests/integration")
    
    # Create basic files
    create_file("app/__init__.py", """from flask import Flask
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
""")
    
    # Config files
    create_file("app/config/__init__.py")
    create_file("app/config/config.py", """import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
""")
    
    # Models
    create_file("app/models/__init__.py", """from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.user import User
""")
    
    create_file("app/models/user.py", """from datetime import datetime
from app.models import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
""")
    
    # Controllers
    create_file("app/controllers/__init__.py")
    create_file("app/controllers/user_controller.py", """from flask import request, jsonify
from app.models import db
from app.models.user import User
from werkzeug.security import generate_password_hash

class UserController:
    @staticmethod
    def get_all_users():
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200
    
    @staticmethod
    def get_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user.to_dict()), 200
    
    @staticmethod
    def create_user():
        data = request.get_json()
        
        if not data or not all(k in data for k in ('username', 'email', 'password')):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Check if username or email already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "Username already exists"}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email already exists"}), 400
        
        try:
            user = User(
                username=data['username'],
                email=data['email'],
                password_hash=generate_password_hash(data['password'])
            )
            
            db.session.add(user)
            db.session.commit()
            return jsonify(user.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
    
    @staticmethod
    def update_user(user_id):
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        try:
            if 'username' in data and data['username'] != user.username:
                if User.query.filter_by(username=data['username']).first():
                    return jsonify({"error": "Username already exists"}), 400
                user.username = data['username']
            
            if 'email' in data and data['email'] != user.email:
                if User.query.filter_by(email=data['email']).first():
                    return jsonify({"error": "Email already exists"}), 400
                user.email = data['email']
            
            if 'password' in data:
                user.password_hash = generate_password_hash(data['password'])
            
            db.session.commit()
            return jsonify(user.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
    
    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "User deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
""")
    
    # Routes
    create_file("app/routes/__init__.py", """from app.routes.user_routes import register_user_routes

def register_routes(app):
    register_user_routes(app)
""")
    
    create_file("app/routes/user_routes.py", """from app.controllers.user_controller import UserController

def register_user_routes(app):
    # Get all users
    app.add_url_rule('/api/users', 'get_users', UserController.get_all_users, methods=['GET'])
    
    # Get a specific user
    app.add_url_rule('/api/users/<int:user_id>', 'get_user', UserController.get_user, methods=['GET'])
    
    # Create a new user
    app.add_url_rule('/api/users', 'create_user', UserController.create_user, methods=['POST'])
    
    # Update a user
    app.add_url_rule('/api/users/<int:user_id>', 'update_user', UserController.update_user, methods=['PUT'])
    
    # Delete a user
    app.add_url_rule('/api/users/<int:user_id>', 'delete_user', UserController.delete_user, methods=['DELETE'])
""")
    
    # Middlewares
    create_file("app/middlewares/__init__.py")
    
    # Utils
    create_file("app/utils/__init__.py")
    
    # Main application files
    create_file("run.py", """from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
""")
    
    create_file(".env", """SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db
FLASK_APP=run.py
FLASK_ENV=development
""")
    
    print("\nFlask MVC structure has been set up successfully!")

# Add this to your setup_flask_mvc_structure function
    create_file("init_db.py", """from app import create_app
from app.models import db

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
""")


if __name__ == "__main__":
    setup_flask_mvc_structure()
