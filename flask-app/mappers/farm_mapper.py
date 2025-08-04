from helpers import FarmHelper
from mappers import FarmerMapper
from models import Farm

class FarmMapper:
    
    @staticmethod
    def model_to_helper(farm: Farm, include_farmer: bool = False, include_country: bool = False, include_schedule: bool = False) -> FarmHelper:
        farmer_helper = None
        if include_farmer and farm.farmer:
            farmer_helper = FarmerMapper.model_to_helper(farm.farmer, include_country)

        schedule_helper = None
        if include_schedule and farm.schedule:
            from mappers import ScheduleMapper
            schedule_helper = [ScheduleMapper.model_to_helper(s) for s in farm.schedule]
        
        return FarmHelper(
            id=farm.id,
            area=float(farm.area),
            village=farm.village,
            crop_grown=farm.crop_grown,
            sowing_date=farm.sowing_date,
            farmer_id=farm.farmer_id,
            created_at=farm.created_at,
            farmer=farmer_helper,
            schedule=schedule_helper
        )
    
    @staticmethod
    def helper_to_model(farm_helper: FarmHelper) -> Farm:
        return Farm(
            area= farm_helper.area,
            village= farm_helper.village,
            crop_grown= farm_helper.crop_grown,
            sowing_date= farm_helper.sowing_date,
            farmer_id= farm_helper.farmer_id
        )