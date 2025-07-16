from datetime import datetime
from typing import Optional

class AuthHelper:
    def __init__(self, email: str, role: Optional[str], id: Optional[int] = None, 
                 created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None, 
                 password: Optional[str] = None):
        self.id = id
        self.email = email
        self.role = role
        self.created_at = created_at
        self.updated_at = updated_at
        self.password = password
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            email=data.get('email').strip() if data.get('email') else None,
            password=data.get('password').strip() if data.get('password') else None,
            role=data.get('role').strip() if data.get('role') else None,
            id=None,
            created_at=None,
            updated_at=None
        )