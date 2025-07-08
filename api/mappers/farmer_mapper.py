from .country_mapper import CountryMapper

class FarmerMapper:
    """Mapper for Farmer data transformations"""
    
    @staticmethod
    def to_dict(farmer):
        if not farmer:
            return None
        return {
            'id': farmer.id,
            'phone_number': farmer.phone_number,
            'name': farmer.name,
            'language': farmer.language,
            'country_id': farmer.country_id,
            'country': CountryMapper.to_dict(farmer.country),
            'created_at': farmer.created_at.isoformat()
        }
    
    @staticmethod
    def from_request(data):
        return {
            'phone_number': data.get('phone_number', '').strip(),
            'name': data.get('name', '').strip(),
            'language': data.get('language', '').strip(),
            'country_id': data.get('country_id')
        }