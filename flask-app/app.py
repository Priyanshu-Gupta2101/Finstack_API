from repositories import CountryRepository
from database import app, db
from helpers.response_helper import ResponseHelper
from flask import jsonify
from helpers import CountryHelper
from mappers import *
from repositories import AuthRepository
from services import AuthServices
from views import *

# ============== UTILITY ROUTES ==============

@app.route('/', methods=['GET'])
def health_check():
    """GET / - Health check endpoint"""
    return jsonify(ResponseHelper.success_response("API is working"))

# ============== APPLICATION SETUP ==============

@app.before_request
def create_tables():
    """Create database tables"""
    db.create_all()
    
    if not CountryRepository.get_by_code('IND'):
        CountryRepository.create(CountryHelper.from_dict({
            "name": "India", "code": "IND"
        }))
    if not CountryRepository.get_by_code('USA'):
        CountryRepository.create(CountryHelper.from_dict({
            "name": "United States", "code": "USA"
        }))
    if not CountryRepository.get_by_code('CHN'):
        CountryRepository.create(CountryHelper.from_dict({
            "name": "China", "code": "CHN"
        }))
    
    super_user = AuthRepository.get_by_email('admin@example.com')
    
    if not super_user:
        default_super_user_data = {
            'email': 'admin@example.com',
            'password': 'admin123',
            'role': 'super_user'
        }
        
        try:
            user = AuthServices.create_user(default_super_user_data)
            print("Default super user created: admin@example.com / admin123")
        except Exception as e:
            print(f"Error creating default super user: {str(e)}")
            

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)