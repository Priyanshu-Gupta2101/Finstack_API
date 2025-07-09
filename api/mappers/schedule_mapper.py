from .farm_mapper import FarmMapper

class ScheduleMapper:
    """Mapper for Schedule data transformations"""
    
    @staticmethod
    def to_dict(schedule):
        if not schedule:
            return None
        return {
            'id': schedule.id,
            'days_after_sowing': schedule.days_after_sowing,
            'fertilizer': schedule.fertilizer,
            'quantity': float(schedule.quantity),
            'quantity_unit': schedule.quantity_unit,
            'farm_id': schedule.farm_id,
            'farm': FarmMapper.to_dict(schedule.farm),
            'due_date': schedule.due_date.isoformat(),
            'created_at': schedule.created_at.isoformat()
        }
    
    @staticmethod
    def from_request(data):
        return {
            'days_after_sowing': data.get('days_after_sowing'),
            'fertilizer': data.get('fertilizer', '').strip(),
            'quantity': data.get('quantity'),
            'quantity_unit': data.get('quantity_unit', '').strip(),
            'farm_id': data.get('farm_id')
        }