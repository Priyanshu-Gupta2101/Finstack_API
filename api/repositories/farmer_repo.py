from database import db
from models import Farmer, Farm
from mappers import FarmerMapper

class FarmerRepository:
    """Repository for Farmer operations"""
    
    @staticmethod
    def create(farmer_helper):
        farmer = FarmerMapper.helper_to_model(farmer_helper)
        db.session.add(farmer)
        db.session.commit()
        return FarmerMapper.model_to_helper(farmer, include_country=True)
    
    @staticmethod
    def get_by_id(farmer_id):
        return FarmerMapper.model_to_helper(Farmer.query.get(farmer_id), include_country=True)
    
    @staticmethod
    def get_by_phone_and_country(phone_number, country_id):
        return FarmerMapper.model_to_helper(Farmer.query.filter_by(
            phone_number=phone_number,
            country_id=country_id
        ).first(), include_country=True)
    
    @staticmethod
    def get_farmers_by_crop(crop_name):
        farmers = db.session.query(Farmer).join(Farm).filter(
            Farm.crop_grown.ilike(f'%{crop_name}%')
        ).distinct().all()

        return [FarmerMapper.model_to_helper(farmer, include_country=True) for farmer in farmers]
    
    @staticmethod
    def get_all_by_country(country_id):
        farmers = Farmer.query.filter_by(country_id=country_id).all()

        return [FarmerMapper.model_to_helper(farmer, include_country=True) for farmer in farmers]
