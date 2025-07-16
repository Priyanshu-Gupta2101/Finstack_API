from repositories import CountryRepository
from database import app, db
from helpers.response_helper import ResponseHelper
from flask import jsonify, request
from helpers import CountryHelper
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from views import *
from mappers import *
from repositories import AuthRepository
from services import AuthServices

def require_role(required_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            current_user = AuthServices.get_current_user(current_user_id)
            
            if not current_user:
                return jsonify({'error': 'User not found'}), 404
                        
            if current_user.to_dict()['role'] not in required_roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ============== AUTH ROUTES ==============

@app.route('/auth/login', methods=["POST"])
def login():
    """POST /auth/login - Login the user"""
    try:
        if not request.json:
            return jsonify(ResponseHelper.error_response("JSON data required")), 400
        
        data = {
            'email': request.json.get('email'),
            'password': request.json.get('password'),
        }
        
        return AuthViews.login(data)
        
    except ValueError as e:
        return jsonify(ResponseHelper.error_response(str(e))), 400
    except IntegrityError:
        return jsonify(ResponseHelper.error_response("Authentication error")), 409
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error")), 500


@app.route('/auth/register', methods=["POST"])
@jwt_required()
def register():
    """POST /auth/register - Create new user"""
    try:
        if not request.json:
            return jsonify(ResponseHelper.error_response("JSON data required")), 400
        
        current_user_id = get_jwt_identity()
        current_user = AuthServices.get_current_user(current_user_id)
        
        if not current_user:
            return jsonify(ResponseHelper.error_response("User not found")), 404
        
        requested_role = request.json.get('role', 'user')

        
        if current_user.role == 'admin':
            if requested_role not in ['user', 'admin']:
                return jsonify(ResponseHelper.error_response("Insufficient permissions to create this role")), 403
        elif current_user.role == 'super_user':
            if requested_role not in ['user', 'admin', 'super_user']:
                return jsonify(ResponseHelper.error_response("Invalid role specified")), 400
        else:
            return jsonify(ResponseHelper.error_response("Insufficient permissions")), 403
        
        data = {
            'email': request.json.get('email'),
            'password': request.json.get('password'),
            'role': requested_role
        }
        
        return AuthViews.register(data)
        
    except ValueError as e:
        return jsonify(ResponseHelper.error_response(str(e))), 400
    except IntegrityError:
        return jsonify(ResponseHelper.error_response("User already exists")), 409
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error: "+ str(e))), 500


@app.route('/auth/me', methods=["GET"])
@jwt_required()
def get_current_user():
    """GET /auth/me - Get current user profile"""
    try:
        print("HERE")

        user_id = get_jwt_identity()

        print(f"Got identity: {user_id} (type: {type(user_id)})")
        
        if not user_id:
            return jsonify(ResponseHelper.error_response("User ID required")), 400
        
        if isinstance(user_id, str):
            user_id = int(user_id)
        
        return AuthViews.get_current_user(user_id)
        
    except ValueError as e:
        return jsonify(ResponseHelper.error_response(str(e))), 400
    except IntegrityError:
        return jsonify(ResponseHelper.error_response("Authentication error")), 409
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error")), 500


# @app.route('/auth/users/<int:user_id>', methods=["GET"])
# @jwt_required()
# @require_role(['super_user', 'admin'])
# def get_user_by_id(user_id):
#     """GET /auth/users/{user_id} - Get user by ID"""
#     try:
#         return AuthViews.get_user_by_id(user_id)
        
#     except ValueError as e:
#         return jsonify(ResponseHelper.error_response(str(e))), 400
#     except IntegrityError:
#         return jsonify(ResponseHelper.error_response("Database error")), 409
#     except Exception as e:
#         return jsonify(ResponseHelper.error_response("Internal server error")), 500


# @app.route('/auth/users', methods=["GET"])
# @jwt_required()
# @require_role(['super_user', 'admin'])
# def get_all_users():
#     """GET /auth/users - Get all users"""
#     try:
#         skip = int(request.args.get('skip', 0))
#         limit = int(request.args.get('limit', 100))
        
#         if skip < 0:
#             return jsonify(ResponseHelper.error_response("Skip parameter must be non-negative")), 400
#         if limit <= 0 or limit > 1000:
#             return jsonify(ResponseHelper.error_response("Limit parameter must be between 1 and 1000")), 400
        
#         return AuthViews.get_all_users(skip, limit)
        
#     except ValueError as e:
#         return jsonify(ResponseHelper.error_response(str(e))), 400
#     except IntegrityError:
#         return jsonify(ResponseHelper.error_response("Database error")), 409
#     except Exception as e:
#         return jsonify(ResponseHelper.error_response("Internal server error")), 500


# @app.route('/auth/users/<int:user_id>', methods=["PUT"])
# @jwt_required()
# @require_role(['super_user', 'admin'])
# def update_user(user_id):
#     """PUT /auth/users/{user_id} - Update user"""
#     try:
#         if not request.json:
#             return jsonify(ResponseHelper.error_response("JSON data required")), 400
        
#         # Get current user to check their role for role updates
#         current_user_id = get_jwt_identity()
#         current_user = AuthViews.get_current_user(current_user_id)
        
#         data = {
#             'email': request.json.get('email'),
#             'password': request.json.get('password'),
#             'name': request.json.get('name'),
#             'role': request.json.get('role')
#         }
        
#         # If role is being updated, check permissions
#         if data['role'] and current_user.role == 'admin':
#             if data['role'] not in ['user', 'admin']:
#                 return jsonify(ResponseHelper.error_response("Insufficient permissions to assign this role")), 403
        
#         data = {k: v for k, v in data.items() if v is not None}
        
#         return AuthViews.update_user(user_id, data)
        
#     except ValueError as e:
#         return jsonify(ResponseHelper.error_response(str(e))), 400
#     except IntegrityError:
#         return jsonify(ResponseHelper.error_response("Database error")), 409
#     except Exception as e:
#         return jsonify(ResponseHelper.error_response("Internal server error")), 500


# @app.route('/auth/users/<int:user_id>', methods=["DELETE"])
# @jwt_required()
# @require_role(['super_user', 'admin'])
# def delete_user(user_id):
#     """DELETE /auth/users/{user_id} - Delete user"""
#     try:
#         current_user_id = get_jwt_identity()
#         if current_user_id == user_id:
#             return jsonify(ResponseHelper.error_response("Cannot delete your own account")), 400
        
#         return AuthViews.delete_user(user_id)
        
#     except ValueError as e:
#         return jsonify(ResponseHelper.error_response(str(e))), 400
#     except IntegrityError:
#         return jsonify(ResponseHelper.error_response("Database error")), 409
#     except Exception as e:
#         return jsonify(ResponseHelper.error_response("Internal server error")), 500

# ============== COUNTRY ROUTES ==============

@app.route('/countries', methods=['POST'])
@jwt_required()
@require_role(['super_user', 'admin'])
def create_country():
    """POST /countries - Create new country"""
    try:
        if not request.json:
            return jsonify(ResponseHelper.error_response("JSON data required")), 400
        
        data = {
            'name' : request.json.get('name'),
            'code' : request.json.get('code')
        }

        if not data['name']:
            raise ValueError("Name is required")
        
        if not data['code']:
            raise ValueError("Code is required")

        country = CountryRepository.create(CountryHelper.from_dict(data))
        
        response = ResponseHelper.success_response(
            country.to_dict(),
            "Country created successfully",
            201
        )
        return jsonify(response), 201
        
    except ValueError as e:
        return jsonify(ResponseHelper.error_response(str(e), 400)), 400
    except IntegrityError:
        return jsonify(ResponseHelper.error_response("Country already exists", 409)), 409
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error")), 500


@app.route('/countries', methods=['GET'])
@jwt_required()
@require_role(['super_user', 'admin', 'user'])
def get_countries():
    """GET /countries - Get all countries"""
    try:
        countries = CountryRepository.get_all()
        country_dicts = [country.to_dict() for country in countries]
        
        response = ResponseHelper.success_response(
            country_dicts,
            f"Retrieved {len(countries)} countries"
        )
        return jsonify(response), 200
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error")), 500

# ============== FARMER ROUTES ==============

@app.route('/farmers', methods=['POST'])
@jwt_required()
@require_role(['super_user', 'admin'])
def create_farmer():
    """POST /farmers - Create new farmer"""
    try:
        if not request.json:
            return jsonify(ResponseHelper.error_response("JSON data required")), 400
        
        data = {
            "phone_number":request.json.get('phone_number'),
            "name":request.json.get('name'),
            "language":request.json.get('language'),
            "country_id":request.json.get('country_id'),
        }

        return FarmerViews.create_farmer(data)
        
    except ValueError as e:
        return jsonify(ResponseHelper.error_response(str(e))), 400
    except IntegrityError:
        return jsonify(ResponseHelper.error_response("Database error")), 409
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error")), 500


@app.route('/farmers/by-crop', methods=['GET'])
@jwt_required()
@require_role(['super_user', 'admin', 'user'])
def get_farmers_by_crop():
    """GET /farmers/by-crop - Get farmers by crop"""
    try:
        crop_name = request.args.get('crop')
        if not crop_name:
            return jsonify(ResponseHelper.error_response("Crop parameter is required")), 400
        
        return FarmerViews.get_farmers_by_crop(crop_name)
        
    except ValueError as e:
        return jsonify(ResponseHelper.error_response(str(e))), 400
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error")), 500

# ============== FARM ROUTES ==============

@app.route('/farms', methods=['POST'])
@jwt_required()
@require_role(['super_user', 'admin'])
def create_farm():
    """POST /farms - Create new farm"""
    try:
        if not request.json:
            return jsonify(ResponseHelper.error_response("JSON data required")), 400
        
        data = {
            'area':float(request.json.get('area', 0)),
            'village':request.json.get('village'),
            'crop_grown':request.json.get('crop_grown'),
            'sowing_date':request.json.get('sowing_date'),
            'farmer_id':request.json.get('farmer_id'),
        }
        
        return FarmViews.create_farm(data)
        
    except ValueError as e:
        return jsonify(ResponseHelper.error_response(str(e))), 400
    except IntegrityError:
        return jsonify(ResponseHelper.error_response("Database error")), 409
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error")), 500

# ============== SCHEDULE ROUTES ==============

@app.route('/schedules', methods=['POST'])
@jwt_required()
@require_role(['super_user', 'admin'])
def create_schedule():
    """POST /schedules - Create new schedule"""
    try:
        if not request.json:
            return jsonify(ResponseHelper.error_response("JSON data required")), 400
        
        data = {
            'days_after_sowing':request.json.get('days_after_sowing'),
            'fertilizer':request.json.get('fertilizer'),
            'quantity':request.json.get('quantity'),
            'quantity_unit':request.json.get('quantity_unit'),
            'farm_id':request.json.get('farm_id'),
        }
                
        return ScheduleViews.create_schedule(data)
        
    except ValueError as e:
        return jsonify(ResponseHelper.error_response(str(e))), 400
    except IntegrityError:
        return jsonify(ResponseHelper.error_response("Database error")), 409
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error")), 500


@app.route('/schedules/today', methods=['GET'])
@jwt_required()
@require_role(['super_user', 'admin', 'user'])
def get_schedules_due_today():
    """GET /schedules/today - Get schedules due today"""
    try:
        return ScheduleViews.get_schedules_due_today()
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error")), 500


@app.route('/schedules/tomorrow', methods=['GET'])
@jwt_required()
@require_role(['super_user', 'admin', 'user'])
def get_schedules_due_tomorrow():
    """GET /schedules/tomorrow - Get schedules due tomorrow"""
    try:
        return ScheduleViews.get_schedules_due_tomorrow()
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error")), 500


@app.route('/schedules/bill/<int:farmer_id>', methods=['POST'])
@jwt_required()
@require_role(['super_user', 'admin'])
def calculate_bill_of_materials(farmer_id):
    """POST /schedules/bill/{farmer_id} - Calculate bill of materials"""
    try:
        if not request.json or 'fertilizer_prices' not in request.json:
            return jsonify(ResponseHelper.error_response("Fertilizer prices required")), 400
                
        fertilizer_prices = request.json['fertilizer_prices']
        return ScheduleViews.calculate_bill_view(farmer_id, fertilizer_prices)
        
    except ValueError as e:
        return jsonify(ResponseHelper.error_response(str(e))), 400
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error")), 500

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
            AuthViews.register(default_super_user_data)
            print("Default super user created: admin@example.com / admin123")
        except Exception as e:
            print(f"Error creating default super user: {e}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)