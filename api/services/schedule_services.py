from datetime import datetime, timedelta
from repositories import ScheduleRepository, FarmRepository
from .validation_services import ValidationService
from mappers import ScheduleMapper

class ScheduleServices:
    """Service for scheduling business logic"""

    @staticmethod
    def create_schedule(schedule_data):
        if not schedule_data['days_after_sowing'] or schedule_data['days_after_sowing'] < 0:
            raise ValueError("Valid days after sowing is required")
        
        if not schedule_data['fertilizer']:
            raise ValueError("Fertilizer name is required")
        
        if not schedule_data['quantity'] or schedule_data['quantity'] <= 0:
            raise ValueError("Valid quantity is required")
        
        if not schedule_data['farm_id']:
            raise ValueError("Farm ID is required")
        
        farm = FarmRepository.get_by_id(schedule_data['farm_id'])
        if not farm:
            raise ValueError("Invalid farm ID")
        
        ValidationService.validate_quantity_unit(schedule_data['quantity_unit'])
        
        return ScheduleRepository.create(ScheduleMapper.create_helper_from_dict(schedule_data))
    
    @staticmethod
    def get_schedules_due_today():
        today = datetime.now().date()
        return ScheduleRepository.get_schedules_by_date(today)
    
    @staticmethod
    def get_schedules_due_tomorrow():
        tomorrow = datetime.now().date() + timedelta(days=1)
        return ScheduleRepository.get_schedules_by_date(tomorrow)
    
    @staticmethod
    def calculate_bill(farmer_id, fertilizer_prices):
        schedules = ScheduleRepository.get_by_farmer(farmer_id)
        
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