from helpers import ScheduleHelper, FarmHelper
from models import Schedule

class ScheduleMapper:
    
    @staticmethod
    def model_to_helper(schedule_model) -> ScheduleHelper:
        farm_helper = None
        if schedule_model.farm:
            farm_helper = FarmHelper(
                id=schedule_model.farm.id,
                area=schedule_model.farm.area,
                village=schedule_model.farm.village,
                crop_grown=schedule_model.farm.crop_grown,
                sowing_date=schedule_model.farm.sowing_date,
                farmer_id=schedule_model.farm.farmer_id,
                created_at=schedule_model.farm.created_at
            )
        
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
    
    @staticmethod
    def create_helper_from_dict(data: dict) -> ScheduleHelper:
        return ScheduleHelper(
            id=None,
            days_after_sowing=data.get('days_after_sowing'),
            fertilizer=data.get('fertilizer'),
            quantity=data.get('quantity'),
            quantity_unit=data.get('quantity_unit'),
            farm_id=data.get('farm_id'),
            created_at=None,
            farm=None
        )