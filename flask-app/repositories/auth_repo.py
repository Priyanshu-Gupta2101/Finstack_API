from database import db
from models import User, RoleEnum
from mappers import AuthMapper

class AuthRepository:
    @staticmethod
    def create(auth_helper, role):
        user = AuthMapper.helper_to_model(auth_helper, role)
        db.session.add(user)
        db.session.commit()
        return AuthMapper.model_to_helper(user)
    
    @staticmethod
    def get_by_id(user_id):
        user = User.query.get(user_id)
        if user is not None:
            return AuthMapper.model_to_helper(user)
        return None
    
    @staticmethod
    def get_by_email(email: str):
        user = User.query.filter_by(email=email).first()
        if user is not None:
            return AuthMapper.model_to_helper(user)
        return None
    
    @staticmethod
    def get_all(skip: int = 0, limit: int = 100):
        users = User.query.offset(skip).limit(limit).all()
        if users is not None:
            return [AuthMapper.model_to_helper(user) for user in users if user is not None]
        return []
    
    @staticmethod
    def update(user_id: int, auth_helper):
        user = User.query.get(user_id)
        if user is not None:
            user.email = auth_helper.email
            user.role = auth_helper.role
            db.session.commit()
            return AuthMapper.model_to_helper(user)
        return None
    
    @staticmethod
    def delete(user_id):
        user = User.query.get(user_id)
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def check_password(id, password):
        user = User.query.get(id)
        return user is not None and user.check_password(password)
    
    @staticmethod
    def is_valid_role(role_name: str) -> bool:
        return role_name in {"super_user", "admin", "user"}