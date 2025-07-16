from datetime import datetime
import re

class ValidationService:
    """Service for data validation"""
    
    @staticmethod
    def validate_phone_number(phone_number):
        if not phone_number:
            raise ValueError("Phone number is required")
        
        cleaned = re.sub(r'\D', '', phone_number)

        if not re.fullmatch(r'\d{10}', cleaned):
            raise ValueError("Phone number must be exactly 10 digits")
        
        return cleaned
    
    @staticmethod
    def validate_date(date):
        if not date:
            raise ValueError("Date is required")
        try:
            return datetime.strptime(date, '%Y-%m-%d').date()
        except:
            raise ValueError("Date is not in the right format, use Use YYYY-MM-DD")
        
    @staticmethod
    def validate_quantity_unit(unit):
        units = ['ton', 'kg', 'g', 'L', 'mL']
        if unit not in units:
            raise ValueError("Invalid quantity unit type, use ton, kg, g, L, mL")
        return True

    @staticmethod
    def validate_email(email):
        if not email:
            raise ValueError("Email is required")
        
        email = email.strip()
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")
        
        if len(email) > 254:
            raise ValueError("Email address is too long")
        
        if '..' in email:
            raise ValueError("Email cannot contain consecutive dots")
        
        local_part = email.split('@')[0]
        if local_part.startswith('.') or local_part.endswith('.'):
            raise ValueError("Email local part cannot start or end with a dot")
        
        return email