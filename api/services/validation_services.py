from datetime import datetime
import re

class ValidationService:
    """Service for data validation"""
    
    @staticmethod
    def validate_phone_number(phone_number):
        """Validate phone number format"""
        if not phone_number:
            raise ValueError("Phone number is required")
        
        cleaned = re.sub(r'[^\d+]', '', phone_number)
        
        if not re.match(r'^\+?\d{10,15}$', cleaned):
            raise ValueError("Invalid phone number format")
        
        return cleaned
    
    @staticmethod
    def validate_date(date):
        """Validate and parse datestring"""
        if not date:
            raise ValueError("Date is required")
        try:
            return datetime.strptime(date, '%Y-%m-%d').date()
        except:
            raise ValueError("Date is not in the right format, use Use YYYY-MM-DD")
        
    @staticmethod
    def validate_quantity_unit(unit):
        """Validate quantity units"""
        units = ['ton', 'kg', 'g', 'L', 'mL']
        if unit not in units:
            raise ValueError("Invalid quantity unit type, use ton, kg, g, L, mL")
        return unit
