class CountryMapper:
    """Mapper for Country data transformations"""

    @staticmethod
    def to_dict(country):
        if not country:
            return None
        return {
            'id': country.id,
            'name': country.name,
            'code': country.code,
            'created_at': country.created_at.isoformat(),
        }
    
    @staticmethod
    def from_request(data):
        return {
            'name': data.get('name', '').strip(),
            'code': data.get('code', '').strip().upper()
        }
    
    