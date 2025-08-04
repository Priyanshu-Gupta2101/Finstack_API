from datetime import datetime, timedelta
from typing import Optional
from .farm_helper import FarmHelper

class ScheduleHelper:
    
    def __init__(self, id: Optional[int], days_after_sowing: int, fertilizer: str, 
                 quantity: float, quantity_unit: str, farm_id: int, 
                 created_at: Optional[datetime], farm: Optional[FarmHelper]):
        self.id = id
        self.days_after_sowing = days_after_sowing
        self.fertilizer = fertilizer
        self.quantity = quantity
        self.quantity_unit = quantity_unit
        self.farm_id = farm_id
        self.created_at = created_at
        self.farm = farm
        if self.farm and self.farm.sowing_date:
            self.due_date = self.farm.sowing_date + timedelta(days=self.days_after_sowing)
        
    
    def to_dict(self, include_farm: bool = False, include_due_date: bool = True) -> dict:
        result = {
            'id': self.id,
            'days_after_sowing': self.days_after_sowing,
            'fertilizer': self.fertilizer,
            'quantity': float(self.quantity),
            'quantity_unit': self.quantity_unit,
            'farm_id': self.farm_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_due_date and self.due_date:
            result['due_date'] = self.due_date.isoformat()
            
        if include_farm and self.farm:
            result['farm'] = self.farm.to_dict()
            
        return result
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            days_after_sowing=int(data['days_after_sowing']) if data.get('days_after_sowing') else None,
            fertilizer=data['fertilizer'].strip() if data.get('fertilizer') else None,
            quantity=float(data['quantity']) if data.get('quantity') else None,
            quantity_unit=data['quantity_unit'].strip() if data.get('quantity_unit') else None,
            farm_id=data['farm_id'] if data.get('farm_id') else None,
            id=data['id'] if data.get('id') else None,
            created_at=data['created_at'] if data.get('created_at') else None,
            farm=data['farm'] if data.get('farm') else None
        )