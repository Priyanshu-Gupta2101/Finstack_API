from typing import Optional
from helpers import ScheduleHelper
from models import Schedule
from mappers import FarmMapper

class ScheduleMapper:
    
    @staticmethod
    def model_to_helper(schedule_model: Schedule) -> Optional[ScheduleHelper]:        
        farm_helper = None
        if schedule_model.farm:
            farm_helper = FarmMapper.model_to_helper(schedule_model.farm)
        
        return ScheduleHelper(
            id=schedule_model.id,
            days_after_sowing=schedule_model.days_after_sowing,
            fertilizer=schedule_model.fertilizer,
            quantity=schedule_model.quantity,
            quantity_unit=schedule_model.quantity_unit,
            farm_id=schedule_model.farm_id,
            created_at=schedule_model.created_at,
            farm=farm_helper
        )
    
    @staticmethod
    def helper_to_model(schedule_helper: ScheduleHelper):
        return Schedule(
            days_after_sowing=schedule_helper.days_after_sowing,
            fertilizer=schedule_helper.fertilizer,
            quantity=schedule_helper.quantity,
            quantity_unit=schedule_helper.quantity_unit,
            farm_id=schedule_helper.farm_id
        )