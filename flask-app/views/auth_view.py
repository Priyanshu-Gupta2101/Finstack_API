from helpers.response_helper import ResponseHelper
from flask import jsonify
from services import AuthServices

class AuthViews:
    """Views for authentication endpoints"""
    
    @staticmethod
    def login(data):
        """POST /auth/login - Login the user"""
        try:
            auth_response = AuthServices.login(data)
            
            response = ResponseHelper.success_response(
                data=auth_response,
                message="User logged in successfully"
            )
            return jsonify(response), 200
            
        except ValueError as e:
            return jsonify(ResponseHelper.error_response(str(e))), 400
        except Exception as e:
            return jsonify(ResponseHelper.error_response("Internal server error: " + str(e))), 500
        
    
    @staticmethod
    def register(data):
        """POST /auth/register - Create new user"""
        try:
            user = AuthServices.create_user(data)
            
            response = ResponseHelper.success_response(
                user.to_dict(),
                "New user created successfully"
            )
            return jsonify(response), 201
            
        except ValueError as e:
            return jsonify(ResponseHelper.error_response(str(e))), 400
        except Exception as e:
            return jsonify(ResponseHelper.error_response("Internal server error: " + str(e))), 500
    
    
    @staticmethod
    def get_current_user(user_id):
        """GET /auth/me - Get current user profile"""
        try:
            user = AuthServices.get_current_user(user_id)
            
            response = ResponseHelper.success_response(
                user.to_dict(),
                "User profile retrieved successfully"
            )
            return jsonify(response), 200
        
        except ValueError as e:
            return jsonify(ResponseHelper.error_response(str(e))), 400
        except Exception as e:
            return jsonify(ResponseHelper.error_response("Internal server error: " + str(e))), 500
        

    @staticmethod
    def get_user_by_id(user_id):
        """GET /auth/users/{user_id} - Get user by ID"""
        try:
            user = AuthServices.get_user_by_id(user_id)
            
            if not user:
                return jsonify(ResponseHelper.error_response("User not found")), 404
            
            response = ResponseHelper.success_response(
                user.to_dict(),
                "User retrieved successfully"
            )
            return jsonify(response), 200
        
        except ValueError as e:
            return jsonify(ResponseHelper.error_response(str(e))), 400
        except Exception as e:
            return jsonify(ResponseHelper.error_response("Internal server error: " + str(e))), 500


    @staticmethod
    def get_all_users(skip=0, limit=100):
        """GET /auth/users - Get all users with pagination"""
        try:
            users = AuthServices.get_all_users(skip, limit)
            
            users_dict = [user.to_dict() for user in users]
            
            response = ResponseHelper.success_response(
                users_dict,
                "Users retrieved successfully"
            )
            return jsonify(response), 200
        
        except ValueError as e:
            return jsonify(ResponseHelper.error_response(str(e))), 400
        except Exception as e:
            return jsonify(ResponseHelper.error_response("Internal server error: " + str(e))), 500


    @staticmethod
    def update_user(user_id, data):
        """PUT /auth/users/{user_id} - Update user"""
        try:
            updated_user = AuthServices.update_user(user_id, data)
            
            response = ResponseHelper.success_response(
                updated_user.to_dict(),
                "User updated successfully"
            )
            return jsonify(response), 200
        
        except ValueError as e:
            return jsonify(ResponseHelper.error_response(str(e))), 400
        except Exception as e:
            return jsonify(ResponseHelper.error_response("Internal server error: " + str(e))), 500


    @staticmethod
    def delete_user(user_id):
        """DELETE /auth/users/{user_id} - Delete user"""
        try:
            result = AuthServices.delete_user(user_id)
            
            response = ResponseHelper.success_response(
                None,
                "User deleted successfully"
            )
            return jsonify(response), 200
        
        except ValueError as e:
            return jsonify(ResponseHelper.error_response(str(e))), 400
        except Exception as e:
            return jsonify(ResponseHelper.error_response("Internal server error: " + str(e))), 500