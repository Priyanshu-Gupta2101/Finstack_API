from helpers.response_helper import ResponseHelper
from flask import jsonify, request
from repositories import CountryRepository
from helpers import CountryHelper
from database import app
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from middleware import require_role

"""Views for country endpoints"""

@app.route('/countries', methods=['POST'])
@jwt_required()
@require_role(['super_user', 'admin'])
def create_country():
    """POST /countries - Create new country"""
    try:
        if not request.json:
            return jsonify(ResponseHelper.error_response("JSON data required")), 400
        
        data = {
            'name': request.json.get('name'),
            'code': request.json.get('code')
        }

        if not data['name']:
            raise ValueError("Name is required")
        
        if not data['code']:
            raise ValueError("Code is required")

        country = CountryRepository.create(CountryHelper.from_dict(data))
        
        if country is None:
            return jsonify(ResponseHelper.error_response("Failed to create country")), 500
        
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
        return jsonify(ResponseHelper.error_response("Internal server error: " + str(e))), 500


@app.route('/countries', methods=['GET'])
@jwt_required()
@require_role(['super_user', 'admin', 'user'])
def get_countries():
    """GET /countries - Get all countries"""
    try:
        countries = CountryRepository.get_all()
        
        if countries is None:
            countries = []
        
        country_dicts = [country.to_dict() for country in countries if country is not None]
        
        response = ResponseHelper.success_response(
            country_dicts,
            f"Retrieved {len(country_dicts)} countries"
        )
        return jsonify(response), 200
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error" + str(e))), 500