from datetime import datetime
from typing import Optional

class CountryHelper:
    
    def __init__(self, name: Optional[str], code: Optional[str], id: Optional[int], created_at: Optional[datetime]):
        self.id = id
        self.name = name
        self.code = code
        self.created_at = created_at
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data['name'].strip() if data.get('name') else None,
            code=data['code'].strip().upper() if data.get('code') else None,
            id=data['id'].strip() if data.get('id') else None,
            created_at=data['created_at'] if data.get('created_at') else None
        )
