from .farmer_mapper import FarmerMapper

class FarmMapper:
    """Mapper for Farm data transformations"""
    
    @staticmethod
    def to_dict(farm):
        if not farm:
            return None
        return {
            'id': farm.id,
            'area': float(farm.area),
            'village': farm.village,
            'crop_grown': farm.crop_grown,
            'sowing_date': farm.sowing_date.isoformat(),
            'farmer_id': farm.farmer_id,
            'farmer': FarmerMapper.to_dict(farm.farmer),
            'created_at': farm.created_at.isoformat()
        }
    
    @staticmethod
    def from_request(data):
        return {
            'area': data.get('area'),
            'village': data.get('village', '').strip(),
            'crop_grown': data.get('crop_grown', '').strip(),
            'sowing_date': data.get('sowing_date'),
            'farmer_id': data.get('farmer_id')
        }