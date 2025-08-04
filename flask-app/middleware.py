from functools import wraps
from flask_jwt_extended import get_jwt_identity
from services import AuthServices
from flask import jsonify

def require_role(required_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            current_user = AuthServices.get_current_user(current_user_id)
            
            if not current_user:
                return jsonify({'error': 'User not found'}), 404
                        
            if current_user.to_dict()['role'] not in required_roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
