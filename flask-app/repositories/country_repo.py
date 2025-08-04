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
        country = Country.query.get(country_id)
        if country is not None:
            return CountryMapper.model_to_helper(country)
        return None
    
    @staticmethod
    def get_by_code(code):
        country = Country.query.filter_by(code=code).first()
        if country is not None:
            return CountryMapper.model_to_helper(country)
        return None
    
    @staticmethod
    def get_all():
        countries = Country.query.all()
        if countries is not None:
            return [CountryMapper.model_to_helper(c) for c in countries if c is not None]
        return []