from helpers import FarmHelper
from mappers import FarmerMapper
from models import Farm

class FarmMapper:
    
    @staticmethod
    def model_to_helper(farm, include_farmer: bool = False, include_country: bool = False) -> FarmHelper:
        if not farm:
            return None
        
        farmer_helper = None
        if include_farmer and farm.farmer:
            farmer_helper = FarmerMapper.model_to_helper(farm.farmer, include_country)
        
        return FarmHelper(
            id=farm.id,
            area=float(farm.area),
            village=farm.village,
            crop_grown=farm.crop_grown,
            sowing_date=farm.sowing_date,
            farmer_id=farm.farmer_id,
            created_at=farm.created_at,
            farmer=farmer_helper
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