from database import db
from models import Country
from mappers import CountryMapper

class CountryRepository:
    """Repository for Country operations"""
    
    @staticmethod
    def create(country_helper):
        country = CountryMapper.helper_to_model(country_helper)
        db.session.add(country)
        db.session.commit()
        return CountryMapper.model_to_helper(country)
    
    @staticmethod
    def get_by_id(country_id):
        return CountryMapper.model_to_helper(Country.query.get(country_id))
    
    @staticmethod
    def get_by_code(code):
        return CountryMapper.model_to_helper(Country.query.filter_by(code=code).first())
    
    @staticmethod
    def get_all():
        countries = Country.query.all()
        return [CountryMapper.model_to_helper(c) for c in countries]