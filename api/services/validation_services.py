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