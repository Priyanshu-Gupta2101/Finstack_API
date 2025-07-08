from models import Farm
from database import db

class FarmRepository:
    """Repository for Farm operations"""
    
    @staticmethod
    def create(area, village, crop_grown, sowing_date, farmer_id):
        farm = Farm(
            area=area,
            village=village,
            crop_grown=crop_grown,
            sowing_date=sowing_date,
            farmer_id=farmer_id
        )
        db.session.add(farm)
        db.session.commit()
        return farm
    
    @staticmethod
    def get_by_id(farm_id):
        return Farm.query.get(farm_id)
    
    @staticmethod
    def get_by_farmer(farmer_id):
        return Farm.query.filter_by(farmer_id=farmer_id).all()