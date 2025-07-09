from datetime import datetime, timedelta
from repositories import ScheduleRepository, FarmRepository
from .validation_services import ValidationService

class ScheduleServices:
    """Service for scheduling business logic"""
    
    def __init__(self):
        self.schedule_repo = ScheduleRepository()
        self.farm_repo = FarmRepository()
        self.validation_service = ValidationService()   

    def create_schedule(self, schedule_data):
        if not schedule_data.get('days_after_sowing') or schedule_data['days_after_sowing'] < 0:
            raise ValueError("Valid days after sowing is required")
        
        if not schedule_data.get('fertilizer'):
            raise ValueError("Fertilizer name is required")
        
        if not schedule_data.get('quantity') or schedule_data['quantity'] <= 0:
            raise ValueError("Valid quantity is required")
        
        if not schedule_data.get('farm_id'):
            raise ValueError("Farm ID is required")
        
        farm = self.farm_repo.get_by_id(schedule_data['farm_id'])
        if not farm:
            raise ValueError("Invalid farm ID")
        
        quantity_unit = self.validation_service.validate_quantity_unit(
            schedule_data['quantity_unit']
        )
        
        return self.schedule_repo.create(
            days_after_sowing=schedule_data['days_after_sowing'],
            fertilizer=schedule_data['fertilizer'],
            quantity=schedule_data['quantity'],
            quantity_unit=quantity_unit,
            farm_id=schedule_data['farm_id']
        )
    
    def get_schedules_due_today(self):
        today = datetime.now().date()
        return self.schedule_repo.get_schedules_by_date(today)
    
    def get_schedules_due_tomorrow(self):
        tomorrow = datetime.now().date() + timedelta(days=1)
        return self.schedule_repo.get_schedules_by_date(tomorrow)
    
    def calculate_bill(self, farmer_id, fertilizer_prices):
        schedules = self.schedule_repo.get_by_farmer(farmer_id)
        
        if not schedules:
            raise ValueError("No schedules found for this farmer")
        
        bill = {}
        total_cost = 0
        
        for schedule in schedules:
            fertilizer = schedule.fertilizer
            quantity = float(schedule.quantity)
            unit = schedule.quantity_unit
            
            if unit in ['g']:
                quantity = quantity / 1000 
                standard_unit = 'kg'
            elif unit in ['ton']:
                quantity = quantity * 1000
                standard_unit = 'kg'
            elif unit in ['mL']:
                quantity = quantity / 1000
                standard_unit = 'L'
            else:
                standard_unit = unit
            
            fertilizer_key = f"{fertilizer}_{standard_unit}"
            price_per_unit = fertilizer_prices.get(fertilizer_key, 0)
            
            if fertilizer not in bill:
                bill[fertilizer] = {
                    'total_quantity': 0,
                    'unit': standard_unit,
                    'price_per_unit': price_per_unit,
                    'total_cost': 0,
                    'farms': []
                }
            
            bill[fertilizer]['total_quantity'] += quantity
            bill[fertilizer]['total_cost'] += quantity * price_per_unit
            bill[fertilizer]['farms'].append({
                'farm_id': schedule.farm_id,
                'crop': schedule.farm.crop_grown,
                'quantity': quantity,
                'due_date': schedule.due_date.isoformat()
            })
            
            total_cost += quantity * price_per_unit
        
        return {
            'farmer_id': farmer_id,
            'total_cost': total_cost,
            'fertilizers': bill
        }