from models import RoleEnum
from models import User
from helpers import AuthHelper

class AuthMapper:
    @staticmethod
    def model_to_helper(user: User) -> AuthHelper:
        return AuthHelper(
            id=user.id,
            email=user.email,
            role=user.role.value if hasattr(user.role, 'value') else user.role,
            created_at=user.created_at.isoformat() if user.created_at else None,
            updated_at=user.updated_at.isoformat() if user.updated_at else None
        )
    
    @staticmethod
    def helper_to_model(helper: AuthHelper, role:str) -> User:
        if isinstance(role, str):
            role = RoleEnum(role)
    
        user = User(
            email=helper.email,
            role=role
        )
        user.set_password(helper.password)
        return user