from models import Farm
from database import db
from mappers import FarmMapper

class FarmRepository:
    """Repository for Farm operations"""
    
    @staticmethod
    def create(farm_helper):
        farm = FarmMapper.helper_to_model(farm_helper)
        db.session.add(farm)
        db.session.commit()
        return FarmMapper.model_to_helper(farm, include_country=True, include_farmer=True)
    
    @staticmethod
    def get_by_id(farm_id):
        return FarmMapper.model_to_helper(Farm.query.get(farm_id), include_country=True, include_farmer=True)
    
    @staticmethod
    def get_by_farmer(farmer_id):
        farms = Farm.query.filter_by(farmer_id=farmer_id).all()

        return [FarmMapper.model_to_helper(farm, include_country=True, include_farmer=True) for farm in farms]