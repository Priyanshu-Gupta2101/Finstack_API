from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from .country_helper import CountryHelper

if TYPE_CHECKING:
    from .farm_helper import FarmHelper

class FarmerHelper:
    
    def __init__(self, id: Optional[int], phone_number: str, name: str, language: str, 
                 country_id: int, created_at: Optional[datetime], country: Optional[CountryHelper], farms: Optional[List['FarmHelper']]):
        self.id = id
        self.phone_number = phone_number
        self.name = name
        self.language = language
        self.country_id = country_id
        self.created_at = created_at
        self.country = country
        self.farms = farms

    def to_dict(self, include_country: bool = False, include_farms: bool = False) -> dict:
        result = {
            'id': self.id,
            'phone_number': self.phone_number,
            'name': self.name,
            'language': self.language,
            'country_id': self.country_id,
            'created_at': self.created_at.isoformat()
        }
        
        if include_country and self.country:
            result['country'] = self.country.to_dict()

        if include_farms and self.farms:
            result['farms'] = [farm.to_dict() for farm in self.farms]
            
        return result

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            phone_number=data['phone_number'].strip() if data.get('phone_number') else None,
            name=data['name'].strip() if data.get('name') else None,
            language=data['language'].strip() if data.get('language') else None,
            country_id=data['country_id'] if data.get('country_id') else None,
            id=data['id'] if data.get('id') else None,
            created_at=data['created_at'] if data.get('created_at') else None,
            country=data['country'] if data.get('country') else None,
            farms=data['farms'] if data.get('farms') else None
        )