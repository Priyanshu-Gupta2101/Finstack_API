from database import db
from models import Farmer, Farm

class FarmerRepository:
    """Repository for Farmer operations"""
    
    @staticmethod
    def create(phone_number, name, language, country_id):
        farmer = Farmer(
            phone_number=phone_number,
            name=name,
            language=language,
            country_id=country_id
        )
        db.session.add(farmer)
        db.session.commit()
        return farmer
    
    @staticmethod
    def get_by_id(farmer_id):
        return Farmer.query.get(farmer_id)
    
    @staticmethod
    def get_by_phone_and_country(phone_number, country_id):
        return Farmer.query.filter_by(
            phone_number=phone_number,
            country_id=country_id
        ).first()
    
    @staticmethod
    def get_farmers_by_crop(crop_name):
        """Get all farmers growing a specific crop"""
        return db.session.query(Farmer).join(Farm).filter(
            Farm.crop_grown.ilike(f'%{crop_name}%')
        ).distinct().all()
    
    @staticmethod
    def get_all_by_country(country_id):
        return Farmer.query.filter_by(country_id=country_id).all()
