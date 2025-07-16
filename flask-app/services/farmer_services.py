from repositories import FarmerRepository, CountryRepository
from .validation_services import ValidationService
from helpers import FarmerHelper

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
        
        return FarmerRepository.create(FarmerHelper.from_dict(farmer_data))

    @staticmethod
    def get_farmers_by_crop(crop_name):
        if not crop_name:
            raise ValueError("Crop name is required")

        return FarmerRepository.get_farmers_by_crop(crop_name)

    