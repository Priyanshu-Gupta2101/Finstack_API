from datetime import datetime
from typing import Optional
from .farmer_helper import FarmerHelper

class FarmHelper:
    
    def __init__(self, id: Optional[int], area: float, village: str, crop_grown: str, 
                 sowing_date: datetime, farmer_id: int, created_at: datetime,
                 farmer: Optional[FarmerHelper] = None):
        self.id = id
        self.area = area
        self.village = village
        self.crop_grown = crop_grown
        self.sowing_date = sowing_date
        self.farmer_id = farmer_id
        self.created_at = created_at
        self.farmer = farmer
    
    def to_dict(self, include_farmer: bool = False) -> dict:
        result = {
            'id': self.id,
            'area': float(self.area),
            'village': self.village,
            'crop_grown': self.crop_grown,
            'sowing_date': self.sowing_date.isoformat() if self.sowing_date else None,
            'farmer_id': self.farmer_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_farmer and self.farmer:
            result['farmer'] = self.farmer.to_dict()
            
        return result
    
    @classmethod
    def from_dict(cls, data: dict):        
        
        return cls(
            id=None,
            area=float(data.get('area', 0)),
            village=data.get('village'),
            crop_grown=data.get('crop_grown'),
            sowing_date=data.get('sowing_date'),
            farmer_id=data.get('farmer_id'),
            created_at=None
        )