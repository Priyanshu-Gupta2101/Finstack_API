from helpers import FarmerHelper
from mappers import CountryMapper
from models import Farmer

class FarmerMapper:
    
    @staticmethod
    def model_to_helper(farmer_model: Farmer, include_country: bool = False, include_farms: bool = False) -> FarmerHelper:
        if farmer_model is None:
            return None
        
        country_helper = None
        if include_country and farmer_model.country:
            country_helper = CountryMapper.model_to_helper(farmer_model.country)

        farms = None
        if include_farms and farmer_model.farm and farmer_model.farm != []:
            from mappers import FarmMapper
            farms = [FarmMapper.model_to_helper(f) for f in farmer_model.farm]
        
        return FarmerHelper(
            id=farmer_model.id,
            phone_number=farmer_model.phone_number,
            name=farmer_model.name,
            language=farmer_model.language,
            country_id=farmer_model.country_id,
            created_at=farmer_model.created_at,
            country=country_helper,
            farms=farms
        )
    
    @staticmethod
    def helper_to_model(farmer_helper: FarmerHelper) -> Farmer:

        return Farmer(
            phone_number=farmer_helper.phone_number,
            name=farmer_helper.name,
            language=farmer_helper.language,
            country_id=farmer_helper.country_id
        )