from app.controllers.auth_controller import AuthController

def register_auth_routes(app):
    # Login route
    app.add_url_rule('/api/auth/login', 'login', AuthController.login, methods=['POST'])
