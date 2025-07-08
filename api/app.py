from repositories import CountryRepository
from database import app, db
from helpers.response_helper import ResponseHelper
from flask import jsonify, request
from mappers import CountryMapper
from sqlalchemy.exc import IntegrityError
from views import FarmerViews
from mappers import FarmerMapper

farmer_views = FarmerViews()

@app.route('/countries', methods=['POST'])
def create_country():
    try:
        if not request.json:
            return jsonify(ResponseHelper.error_response("JSON data required")), 400
        
        country_data = CountryMapper.from_request(request.json)
        country = CountryRepository.create(country_data['name'], country_data['code'])
        
        response = ResponseHelper.success_response(
            CountryMapper.to_dict(country),
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
    country_dicts = [CountryMapper.to_dict(country) for country in countries]
    
    response = ResponseHelper.success_response(
        country_dicts,
        f"Retrieved {len(countries)} countries"
    )
    return jsonify(response), 200

@app.route('/farmers', methods=['POST'])
def create_farmer():
    if not request.json:
        return jsonify(ResponseHelper.error_response("JSON data required")), 400
    
    farmer_data = FarmerMapper.from_request(request.json)

    return farmer_views.create_farmer(farmer_data)

@app.route('/farmers/by-crop', methods=['GET'])
def get_farmers_by_crop():
    crop_name = request.args.get('crop')
    if not crop_name:
        return jsonify(ResponseHelper.error_response("Crop parameter is required")), 400
    
    return farmer_views.get_farmers_by_crop(crop_name)

# Health check
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
