from repositories import FarmRepository, FarmerRepository
from .validation_services import ValidationService
from helpers import FarmHelper

class FarmServices:
    """Service for farm business logic"""

    @staticmethod
    def create_farm(farm_data):
        if not farm_data['area'] or farm_data['area'] <=0:
            raise ValueError("Valid Area is required")
        
        if not farm_data['village']:
            raise ValueError("Village is required")
        
        if not farm_data['crop_grown']:
            raise ValueError("Crop grown is required")
        
        if not farm_data['farmer_id']:
            raise ValueError("Farmer ID is required")
        
        farmer = FarmerRepository.get_by_id(
            farm_data['farmer_id']
        )

        if not farmer:
            raise ValueError("Invalid farmer ID")
        
        sowing_date = ValidationService.validate_date(farm_data['sowing_date'])

        farm_data['sowing_date'] = sowing_date
        
        farm = FarmRepository.create(FarmHelper.from_dict(farm_data))

        return farm
    