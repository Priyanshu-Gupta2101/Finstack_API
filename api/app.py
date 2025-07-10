from repositories import CountryRepository
from database import app, db
from helpers.response_helper import ResponseHelper
from flask import jsonify, request
from helpers import CountryHelper
from sqlalchemy.exc import IntegrityError
from views import *
from mappers import *
    
@app.route('/countries', methods=['POST'])
def create_country():
    try:
        if not request.json:
            return jsonify(ResponseHelper.error_response("JSON data required")), 400
        
        data = {
            'name' : request.json.get('name'),
            'code' : request.json.get('code')
        }

        if not data['name']:
            raise ValueError("Name is reuired")
        
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


@app.route('/countries', methods=['GET'])
def get_countries():
    countries = CountryRepository.get_all()
    country_dicts = [country.to_dict() for country in countries]
    
    response = ResponseHelper.success_response(
        country_dicts,
        f"Retrieved {len(countries)} countries"
    )
    return jsonify(response), 200


@app.route('/farmers', methods=['POST'])
def create_farmer():
    if not request.json:
        return jsonify(ResponseHelper.error_response("JSON data required")), 400
    
    data = {
        "phone_number":request.json.get('phone_number'),
        "name":request.json.get('name'),
        "language":request.json.get('language'),
        "country_id":request.json.get('country_id'),
    }

    return FarmerViews.create_farmer(data)


@app.route('/farmers/by-crop', methods=['GET'])
def get_farmers_by_crop():
    crop_name = request.args.get('crop')
    if not crop_name:
        return jsonify(ResponseHelper.error_response("Crop parameter is required")), 400
    
    return FarmerViews.get_farmers_by_crop(crop_name)


@app.route('/farms', methods=['POST'])
def create_farm():
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


@app.route('/schedules', methods=['POST'])
def create_schedule():
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


@app.route('/schedules/today', methods=['GET'])
def get_schedules_due_today():
    return ScheduleViews.get_schedules_due_today()


@app.route('/schedules/tomorrow', methods=['GET'])
def get_schedules_due_tomorrow():
    return ScheduleViews.get_schedules_due_tomorrow()


@app.route('/schedules/bill/<int:farmer_id>', methods=['POST'])
def calculate_bill_of_materials(farmer_id):
    if not request.json or 'fertilizer_prices' not in request.json:
        return jsonify(ResponseHelper.error_response("Fertilizer prices required")), 400
            
    fertilizer_prices = request.json['fertilizer_prices']
    return ScheduleViews.calculate_bill_view(farmer_id, fertilizer_prices)


@app.route('/', methods=['GET'])
def health_check():
    return jsonify(ResponseHelper.success_response("API is healthy"))

@app.before_request
def create_tables():
    """Create database tables"""
    db.create_all()
    
    if not CountryRepository.get_by_code('IND'):
        CountryRepository.create('India', 'IND')
    if not CountryRepository.get_by_code('USA'):
        CountryRepository.create('United States', 'USA')
    if not CountryRepository.get_by_code('CHN'):
        CountryRepository.create('China', 'CHN')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
