from datetime import datetime
from sched import scheduler
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .farmer_helper import FarmerHelper
    from .schedule_helper import ScheduleHelper

class FarmHelper:
    
    def __init__(self, area: float, village: str, crop_grown: str, 
                 sowing_date: datetime, farmer_id: int, id: Optional[int], created_at: Optional[datetime],
                 farmer: Optional['FarmerHelper'], schedule: Optional[List['ScheduleHelper']]):
        self.id = id
        self.area = area
        self.village = village
        self.crop_grown = crop_grown
        self.sowing_date = sowing_date
        self.farmer_id = farmer_id
        self.created_at = created_at
        self.farmer = farmer
        self.schedule = schedule
    
    def to_dict(self, include_farmer: bool = False, include_schedule: bool = False) -> dict:
        result = {
            'id': self.id,
            'area': float(self.area),
            'village': self.village,
            'crop_grown': self.crop_grown,
            'sowing_date': self.sowing_date.isoformat(),
            'farmer_id': self.farmer_id,
            'created_at': self.created_at.isoformat()
        }
        
        if include_farmer and self.farmer:
            result['farmer'] = self.farmer.to_dict()

        if include_schedule and self.schedule:
            result['schedule'] = [s.to_dict() for s in self.schedule]
            
        return result

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            area=float(data['area']) if data.get('area') else 0.0,
            village=data['village'].strip() if data.get('village') else None,
            crop_grown=data['crop_grown'].strip() if data.get('crop_grown') else None,
            sowing_date=data['sowing_date'],
            farmer_id=data['farmer_id'] if data.get('farmer_id') else None,
            created_at=data['created_at'] if data.get('created_at') else None,
            id=data['id'] if data.get('id') else None,
            farmer=data['farmer'] if data.get('farmer') else None,
            schedule=data['schedule'] if data.get('schedule') else None
        )