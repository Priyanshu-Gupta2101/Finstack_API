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
            email=data['email'].strip(),
            password=data['password'].strip() if data.get('password') else None,
            role=data['role'].strip() if data.get('role') else None,
            id=data['id'].strip() if data.get('id') else None,
            created_at=data['created_at'].strip() if data.get('created_at') else None,
            updated_at=data['updated_at'].strip() if data.get('updated_at') else None
        )