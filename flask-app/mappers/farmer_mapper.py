from helpers import FarmerHelper
from mappers import CountryMapper
from models import Farmer

class FarmerMapper:
    
    @staticmethod
    def model_to_helper(farmer_model, include_country: bool = False) -> FarmerHelper:
        if not farmer_model:
            return None
        
        country_helper = None
        if include_country and farmer_model.country:
            country_helper = CountryMapper.model_to_helper(farmer_model.country)
        
        return FarmerHelper(
            id=farmer_model.id,
            phone_number=farmer_model.phone_number,
            name=farmer_model.name,
            language=farmer_model.language,
            country_id=farmer_model.country_id,
            created_at=farmer_model.created_at,
            country=country_helper
        )
    
    @staticmethod
    def helper_to_model(farmer_helper: FarmerHelper) -> Farmer:
        return Farmer(
            phone_number=farmer_helper.phone_number,
            name=farmer_helper.name,
            language=farmer_helper.language,
            country_id=farmer_helper.country_id
        )