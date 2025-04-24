from flask import request, jsonify, current_app
from app.models.user import User
import jwt
import datetime

class AuthController:
    @staticmethod
    def login():
        data = request.get_json()
        
        if not data or not all(k in data for k in ('username', 'password')):
            return jsonify({"error": "Missing username or password"}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({"error": "Invalid username or password"}), 401
        
        # Generate JWT token
        expiration = datetime.datetime.utcnow() + datetime.timedelta(
            hours=current_app.config.get('JWT_EXPIRATION_HOURS', 24)
        )
        
        token = jwt.encode({
            'user_id': user.id,
            'username': user.username,
            'exp': expiration
        }, current_app.config['SECRET_KEY'])
        
        return jsonify({
            'token': token,
            'user': user.to_dict(),
            'expires_at': expiration.isoformat()
        }), 200
