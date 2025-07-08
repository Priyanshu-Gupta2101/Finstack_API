from datetime import datetime, timezone

class ResponseHelper:
    """Helper for formatting API responses"""
    
    @staticmethod
    def success_response(data, message="API ops success", status_code=200):
        return {
            'success': True,
            'message': message,
            'data': data,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'status_code': status_code
        }
    
    @staticmethod
    def error_response(message, status_code=400):
        return {
            'success': False,
            'message': message,
            'data': None,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'status_code': status_code
        }