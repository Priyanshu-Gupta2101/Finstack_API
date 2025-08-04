from datetime import timedelta
from database import db
from models import Schedule, Farm
from mappers import ScheduleMapper

class ScheduleRepository:
    """Repository for Schedule operations"""
    
    @staticmethod
    def create(schedule_helper):
        schedule = ScheduleMapper.helper_to_model(schedule_helper)
        db.session.add(schedule)
        db.session.commit()
        return ScheduleMapper.model_to_helper(schedule)
    
    @staticmethod
    def get_schedules_by_date(day):
        schedules = db.session.query(Schedule).join(Farm).all()
        if schedules is not None:
            return [
                ScheduleMapper.model_to_helper(s) for s in schedules
                if s is not None and s.farm and (s.farm.sowing_date + timedelta(days=s.days_after_sowing)) == day
            ]
        return []
    
    @staticmethod
    def get_by_farmer(farmer_id):
        schedules = db.session.query(Schedule).join(Farm).filter(
            Farm.farmer_id == farmer_id
        ).all()
        
        if schedules is not None:
            return [ScheduleMapper.model_to_helper(schedule) for schedule in schedules if schedule is not None]
        return []
    
    @staticmethod
    def get_by_id(schedule_id):
        schedule = Schedule.query.get(schedule_id)
        if schedule is not None:
            return ScheduleMapper.model_to_helper(schedule)
        return None