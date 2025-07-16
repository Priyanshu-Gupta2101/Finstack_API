from helpers import CountryHelper
from models import Country

class CountryMapper:

    @staticmethod
    def model_to_helper(country_model) -> CountryHelper:
        if not country_model:
            return None
            
        return CountryHelper(
            id=country_model.id,
            name=country_model.name,
            code=country_model.code,
            created_at=country_model.created_at
        ) 
    
    @staticmethod
    def helper_to_model(country_helper: CountryHelper) -> Country:
        return Country(
            name=country_helper.name,
            code=country_helper.code
        )

    