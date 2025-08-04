from helpers.response_helper import ResponseHelper
from flask import jsonify, request
from services import FarmServices
from database import app
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from middleware import require_role
from repositories import FarmRepository

"""Views for farm endpoints"""

@app.route('/farms', methods=['POST'])
@jwt_required()
@require_role(['super_user', 'admin'])
def create_farm():
    """POST /farms - Create new farm"""
    try:
        if not request.json:
            return jsonify(ResponseHelper.error_response("JSON data required")), 400
        
        data = {
            'area': float(request.json.get('area', 0)),
            'village': request.json.get('village'),
            'crop_grown': request.json.get('crop_grown'),
            'sowing_date': request.json.get('sowing_date'),
            'farmer_id': request.json.get('farmer_id'),
        }
        
        farm = FarmServices.create_farm(data)
        
        if farm is None:
            return jsonify(ResponseHelper.error_response("Failed to create farm")), 500
        
        response = ResponseHelper.success_response(
            farm.to_dict(include_farmer=True),
            "Farm created successfully",
            201
        )
        return jsonify(response), 201
        
    except ValueError as e:
        return jsonify(ResponseHelper.error_response(str(e))), 400
    except IntegrityError:
        return jsonify(ResponseHelper.error_response("Database error")), 409
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error: "+ str(e))), 500
    

@app.route('/farms', methods=['GET'])
@jwt_required()
@require_role(['super_user', 'admin', 'user'])
def get_all_farms():
    """GET /farms - Get all farms"""
    try:
        farms = FarmRepository.get_all()
        
        if farms is None:
            farms = []
        
        farm_dicts = [farm.to_dict(include_farmer=True) for farm in farms if farm is not None]
        
        response = ResponseHelper.success_response(
            farm_dicts,
            f"Retrieved {len(farm_dicts)} farms",
            200
        )
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error" + str(e))), 500

@app.route('/farms/<int:farm_id>', methods=['GET'])
@jwt_required()
@require_role(['super_user', 'admin', 'user'])
def get_farm_by_id(farm_id):
    """GET /farms/{farm_id} - Get farm details by id"""
    try:
        if farm_id is None:
            return jsonify(ResponseHelper.error_response("Farm id is required")), 400
        
        farm = FarmServices.get_farms_by_id(farm_id)
        
        if farm is None:
            return jsonify(ResponseHelper.error_response("Failed to get farm")), 500
        
        response = ResponseHelper.success_response(
            farm.to_dict(include_farmer=True, include_schedule=True),
            f"Found Farm by id:{farm_id} successfully",
            201
        )
        return jsonify(response), 201
        
    except ValueError as e:
        return jsonify(ResponseHelper.error_response(str(e))), 400
    except IntegrityError:
        return jsonify(ResponseHelper.error_response("Database error")), 409
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error: " + str(e))), 500