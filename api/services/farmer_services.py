from repositories import FarmerRepository, CountryRepository
from .validation_services import ValidationService

class FarmerServices:
    """Service for farmer business logic"""
    
    def __init__(self):
        self.farmer_repo = FarmerRepository()
        self.country_repo = CountryRepository()
        self.validation_service = ValidationService()

    def create_farmer(self, farmer_data):
        if not farmer_data.get('name'):
            raise ValueError("Farmer name is required")
        
        if not farmer_data.get('language'):
            raise ValueError("Language is required")
        
        if not farmer_data.get('country_id'):
            raise ValueError("Country is required")
        
        phone_number = self.validation_service.validate_phone_number(
            farmer_data['phone_number']
        )
        
        country = self.country_repo.get_by_id(farmer_data['country_id'])
        if not country:
            raise ValueError("Invalid country ID")
        
        existing_farmer = self.farmer_repo.get_by_phone_and_country(
            phone_number, farmer_data['country_id']
        )
        if existing_farmer:
            raise ValueError("Farmer with this phone number already exists in this country")
        
        return self.farmer_repo.create(
            phone_number=phone_number,
            name=farmer_data['name'],
            language=farmer_data['language'],
            country_id=farmer_data['country_id']
        )

    def get_farmers_by_crop(self, crop_name):
        if not crop_name:
            raise ValueError("Crop name is required")

        return self.farmer_repo.get_farmers_by_crop(crop_name)

    