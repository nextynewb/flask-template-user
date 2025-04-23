from app.controllers.user_controller import UserController

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
