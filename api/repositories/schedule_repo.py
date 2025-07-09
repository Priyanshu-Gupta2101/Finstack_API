from datetime import timedelta
from database import db
from models import Schedule, Farm

class ScheduleRepository:
    """Repository for Schedule operations"""
    
    @staticmethod
    def create(days_after_sowing, fertilizer, quantity, quantity_unit, farm_id):
        schedule = Schedule(
            days_after_sowing=days_after_sowing,
            fertilizer=fertilizer,
            quantity=quantity,
            quantity_unit=quantity_unit,
            farm_id=farm_id
        )
        db.session.add(schedule)
        db.session.commit()
        return schedule
    
    @staticmethod
    def get_schedules_by_date(day):
        schedules = db.session.query(Schedule).join(Farm).all()
        return [
            s for s in schedules
            if s.farm and (s.farm.sowing_date + timedelta(days=s.days_after_sowing)) == day
        ]
    
    @staticmethod
    def get_by_farmer(farmer_id):
        """Get all schedules for a farmer"""
        return db.session.query(Schedule).join(Farm).filter(
            Farm.farmer_id == farmer_id
        ).all()