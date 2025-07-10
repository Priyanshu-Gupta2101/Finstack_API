from repositories import FarmerRepository, CountryRepository
from .validation_services import ValidationService
from mappers import FarmerMapper

class FarmerServices:
    """Service for farmer business logic"""

    @staticmethod
    def create_farmer(farmer_data):
        if not farmer_data["name"]:
            raise ValueError("Farmer name is required")
        
        if not farmer_data["language"]:
            raise ValueError("Language is required")
        
        if not farmer_data["country_id"]:
            raise ValueError("Country is required")
        
        phone_number = ValidationService.validate_phone_number(farmer_data["phone_number"])
        
        country = CountryRepository.get_by_id(farmer_data["country_id"])
        if not country:
            raise ValueError("Invalid country ID")
        
        existing_farmer = FarmerRepository.get_by_phone_and_country(
            phone_number, farmer_data["country_id"]
        )
        if existing_farmer:
            raise ValueError("Farmer with this phone number already exists in this country")
        
        farmer_helper = FarmerMapper.create_helper_from_dict(farmer_data)
        
        return FarmerRepository.create(farmer_helper)

    @staticmethod
    def get_farmers_by_crop(crop_name):
        if not crop_name:
            raise ValueError("Crop name is required")

        farmers = FarmerRepository.get_farmers_by_crop(crop_name)

        return [FarmerMapper.model_to_helper(farmer, include_country=True) for farmer in farmers]

    