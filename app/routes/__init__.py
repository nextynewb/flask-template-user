from app.routes.user_routes import register_user_routes
from app.routes.auth_routes import register_auth_routes

def register_routes(app):
    register_user_routes(app)
    register_auth_routes(app)
