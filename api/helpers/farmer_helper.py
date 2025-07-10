from datetime import datetime
from typing import Optional
from .country_helper import CountryHelper

class FarmerHelper:
    
    def __init__(self, id: Optional[int], phone_number: str, name: str, language: str, 
                 country_id: int, created_at: Optional[datetime], country: Optional[CountryHelper] = None):
        self.id = id
        self.phone_number = phone_number
        self.name = name
        self.language = language
        self.country_id = country_id
        self.created_at = created_at
        self.country = country

    def to_dict(self, include_country: bool = False) -> dict:
        result = {
            'id': self.id,
            'phone_number': self.phone_number,
            'name': self.name,
            'language': self.language,
            'country_id': self.country_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_country and self.country:
            result['country'] = self.country.to_dict()
            
        return result
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=None,
            phone_number=data.get('phone_number'),
            name=data.get('name'),
            language=data.get('language'),
            country_id=data.get('country_id'),
            created_at=None,
            country=None
        )