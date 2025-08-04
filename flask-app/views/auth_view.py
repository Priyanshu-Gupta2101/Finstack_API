from helpers.response_helper import ResponseHelper
from flask import jsonify, request
from services import AuthServices
from database import app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError


@app.route('/auth/login', methods=["POST"])
def login():
    """POST /auth/login - Login the user"""
    try:
        if not request.json:
            return jsonify(ResponseHelper.error_response("JSON data required")), 400
        
        data = {
            'email': request.json.get('email'),
            'password': request.json.get('password'),
        }
        
        auth_response = AuthServices.login(data)
        
        if auth_response is None:
            return jsonify(ResponseHelper.error_response("Login failed")), 401
        
        response = ResponseHelper.success_response(
            data=auth_response,
            message="User logged in successfully"
        )
        return jsonify(response), 200
        
    except ValueError as e:
        return jsonify(ResponseHelper.error_response(str(e))), 400
    except IntegrityError:
        return jsonify(ResponseHelper.error_response("Authentication error")), 409
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error")), 500


@app.route('/auth/register', methods=["POST"])
@jwt_required()
def register():
    """POST /auth/register - Create new user"""
    try:
        if not request.json:
            return jsonify(ResponseHelper.error_response("JSON data required")), 400
        
        current_user_id = get_jwt_identity()
        current_user = AuthServices.get_current_user(current_user_id)
        
        if current_user is None:
            return jsonify(ResponseHelper.error_response("User not found")), 404
        
        requested_role = request.json.get('role', 'user')
        
        if current_user.role == 'admin':
            if requested_role not in ['user', 'admin']:
                return jsonify(ResponseHelper.error_response("Insufficient permissions to create this role")), 403
        elif current_user.role == 'super_user':
            if requested_role not in ['user', 'admin', 'super_user']:
                return jsonify(ResponseHelper.error_response("Invalid role specified")), 400
        else:
            return jsonify(ResponseHelper.error_response("Insufficient permissions")), 403
        
        data = {
            'email': request.json.get('email'),
            'password': request.json.get('password'),
            'role': requested_role
        }
        
        user = AuthServices.create_user(data)
        
        if user is None:
            return jsonify(ResponseHelper.error_response("Failed to create user")), 500
        
        response = ResponseHelper.success_response(
            user.to_dict(),
            "New user created successfully"
        )
        return jsonify(response), 201
        
    except ValueError as e:
        return jsonify(ResponseHelper.error_response(str(e))), 400
    except IntegrityError:
        return jsonify(ResponseHelper.error_response("User already exists")), 409
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error: " + str(e))), 500


@app.route('/auth/me', methods=["GET"])
@jwt_required()
def get_current_user():
    """GET /auth/me - Get current user profile"""
    try:
        user_id = get_jwt_identity()
                    
        if not user_id:
            return jsonify(ResponseHelper.error_response("User ID required")), 400
        
        if isinstance(user_id, str):
            user_id = int(user_id)
        
        user = AuthServices.get_current_user(user_id)
        
        if user is None:
            return jsonify(ResponseHelper.error_response("User not found")), 404
        
        response = ResponseHelper.success_response(
            user.to_dict(),
            "User profile retrieved successfully"
        )
        return jsonify(response), 200
    
    except ValueError as e:
        return jsonify(ResponseHelper.error_response(str(e))), 400
    except IntegrityError:
        return jsonify(ResponseHelper.error_response("Authentication error")), 409
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error")), 500