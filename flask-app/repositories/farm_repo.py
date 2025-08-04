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
        farm = Farm.query.get(farm_id)
        if farm is not None:
            return FarmMapper.model_to_helper(farm, include_country=True, include_farmer=True, include_schedule=True)
        return None
    
    @staticmethod
    def get_by_farmer(farmer_id):
        farms = Farm.query.filter_by(farmer_id=farmer_id).all()
        if farms is not None:
            return [FarmMapper.model_to_helper(farm, include_country=True, include_farmer=True) for farm in farms if farm is not None]
        return []
    
    @staticmethod
    def get_all():
        farms = Farm.query.all()
        if farms is not None:
            return [FarmMapper.model_to_helper(farm, include_country=True, include_farmer=True) for farm in farms if farm is not None]
        return []
