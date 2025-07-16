from datetime import timedelta
from flask_jwt_extended import create_access_token
from services import ValidationService
from repositories import AuthRepository
from helpers import AuthHelper

class AuthServices:
    @staticmethod
    def login(data: dict):
        if not data['email']:
            raise ValueError("Email is required")
        
        data['email'] = ValidationService.validate_email(data["email"])
        
        if not data['password']:
            raise ValueError("Password is required")
        
        user = AuthRepository.get_by_email(data['email'])
        
        if not user:
            raise ValueError("Invalid credentials / User not found for this credentials")
        
        
        if not AuthRepository.check_password(user.id, data['password']):
            raise ValueError("Invalid credentials / Incorrect password")
        

        additional_claims = {
            "role": user.role,
            "email": user.email,
        }

        
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims=additional_claims,
            expires_delta=timedelta(hours=24)
        )


        return {
            "access_token":access_token,
            "user":user.to_dict()
        }
    
    @staticmethod
    def get_current_user(user_id):
        return AuthRepository.get_by_id(user_id)

    @staticmethod
    def create_user(user_data: dict):

        if not user_data['email']:
            raise ValueError("Email is required")
        
        user_data['email'] = ValidationService.validate_email(user_data["email"])
        
        if not user_data['password']:
            raise ValueError("Password is required")
        
        existing_user = AuthRepository.get_by_email(user_data['email'])
        if existing_user:
            raise ValueError("User with this email already exists")
        
        
        if not AuthRepository.is_valid_role(user_data['role']):
            raise ValueError("Invalid role specified")
       
        return AuthRepository.create(AuthHelper.from_dict(user_data), user_data['role'])

    @staticmethod        
    def get_user_by_id(user_id: int):
        return AuthRepository.get_by_id(user_id)
    
    @staticmethod
    def get_all_users(skip: int = 0, limit: int = 100):
        return AuthRepository.get_all(skip, limit)
    
    @staticmethod
    def update_user(user_id: int, update_data: dict):
        user = AuthRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        if update_data['role'] and not AuthRepository.is_valid_role(update_data.role):
            raise ValueError("Invalid role specified")
        
        updated_user = AuthHelper.from_dict(update_data)
        return AuthRepository.update(user_id, updated_user)
        
    @staticmethod
    def delete_user(user_id: int):
        user = AuthRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        return AuthRepository.delete(user)