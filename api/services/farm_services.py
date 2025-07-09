from repositories import FarmRepository, FarmerRepository
from .validation_services import ValidationService

class FarmServices:
    """Service for farm business logic"""
    
    def __init__(self):
        self.farm_repo = FarmRepository()
        self.farmer_repo = FarmerRepository()
        self.validation_service = ValidationService()   

    def create_farm(self, farm_data):
        if not farm_data.get('area') or farm_data.get('area') <=0:
            raise ValueError("Valid Area is required")
        
        if not farm_data.get('village'):
            raise ValueError("Village is required")
        
        if not farm_data.get('crop_grown'):
            raise ValueError("Crop grown is required")
        
        if not farm_data.get('farmer_id'):
            raise ValueError("Farmer ID is required")
        
        farmer = self.farmer_repo.get_by_id(
            farm_data['farmer_id']
        )

        if not farmer:
            raise ValueError("Invalid farmer ID")
        
        sowing_date = self.validation_service.validate_date(farm_data['sowing_date'])
        
        return self.farm_repo.create(
            area=farm_data['area'],
            village=farm_data['village'],
            crop_grown=farm_data['crop_grown'],
            farmer_id=farm_data['farmer_id'],
            sowing_date=sowing_date
        )
    