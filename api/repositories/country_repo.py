from database import db
from models import Country

class CountryRepository:
    """Repository for Country operations"""
    
    @staticmethod
    def create(name, code):
        country = Country(name=name, code=code)
        db.session.add(country)
        db.session.commit()
        return country
    
    @staticmethod
    def get_by_id(country_id):
        return Country.query.get(country_id)
    
    @staticmethod
    def get_by_code(code):
        return Country.query.filter_by(code=code).first()
    
    @staticmethod
    def get_all():
        return Country.query.all()