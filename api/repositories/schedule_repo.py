from database import db
from models import Schedule, Farm
from datetime import datetime,timedelta

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
    def get_schedules_due_today():
        """Get all schedules due today"""
        today = datetime.now().date()
        return db.session.query(Schedule).join(Farm).filter(
            db.func.date(Farm.sowing_date + db.func.cast(
                Schedule.days_after_sowing + ' days', db.Interval
            )) == today
        ).all()
    
    @staticmethod
    def get_schedules_due_tomorrow():
        """Get all schedules due tomorrow"""
        tomorrow = datetime.now().date() + timedelta(days=1)
        return db.session.query(Schedule).join(Farm).filter(
            db.func.date(Farm.sowing_date + db.func.cast(
                Schedule.days_after_sowing + ' days', db.Interval
            )) == tomorrow
        ).all()
    
    @staticmethod
    def get_by_farmer(farmer_id):
        """Get all schedules for a farmer"""
        return db.session.query(Schedule).join(Farm).filter(
            Farm.farmer_id == farmer_id
        ).all()