from helpers.response_helper import ResponseHelper
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from services import FarmerServices
from database import app
from flask_jwt_extended import jwt_required
from middleware import require_role
from repositories import FarmerRepository

"""Views for farmer endpoints"""

@app.route('/farmers', methods=['POST'])
@jwt_required()
@require_role(['super_user', 'admin'])
def create_farmer():
    """POST /farmers - Create new farmer"""
    try:
        if not request.json:
            return jsonify(ResponseHelper.error_response("JSON data required")), 400
        
        data = {
            "phone_number": request.json.get('phone'),
            "name": request.json.get('name'),
            "language": request.json.get('language'),
            "country_id": request.json.get('country_id'),
        }
        
        farmer = FarmerServices.create_farmer(data)
        
        if farmer is None:
            return jsonify(ResponseHelper.error_response("Failed to create farmer")), 500
        
        response = ResponseHelper.success_response(
            farmer.to_dict(include_country=True),
            "Farmer created successfully",
            201
        )
        return jsonify(response), 201
        
    except ValueError as e:
        return jsonify(ResponseHelper.error_response(str(e))), 400
    except IntegrityError:
        return jsonify(ResponseHelper.error_response("Database error")), 409
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error: " + str(e))), 500
    

@app.route('/farmers', methods=['GET'])
@jwt_required()
@require_role(['super_user', 'admin', 'user'])
def get_all_farmers():
    """GET /farmers - Get all farmer"""
    try:
        farmers = FarmerRepository.get_all()
        
        if farmers is None:
            farmers = []
        
        farmer_dicts = [farmer.to_dict(include_country=True) for farmer in farmers if farmer is not None]
        
        response = ResponseHelper.success_response(
            farmer_dicts,
            f"Retrieved {len(farmer_dicts)} farmers",
            200
        )
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error" + str(e))), 500

@app.route('/farmers/by-crop', methods=['GET'])
@jwt_required()
@require_role(['super_user', 'admin', 'user'])
def get_farmers_by_crop():
    """GET /farmers/by-crop - Get farmers by crop"""
    try:
        crop_name = request.args.get('crop')
        if not crop_name:
            return jsonify(ResponseHelper.error_response("Crop parameter is required")), 400
        
        farmers = FarmerServices.get_farmers_by_crop(crop_name)
        
        if farmers is None:
            farmers = []
        
        farmer_dicts = [farmer.to_dict(include_country=True) for farmer in farmers if farmer is not None]
        
        response = ResponseHelper.success_response(
            farmer_dicts,
            f"Found {len(farmer_dicts)} farmers growing {crop_name}"
        )
        return jsonify(response), 200
        
    except ValueError as e:
        return jsonify(ResponseHelper.error_response(str(e))), 400
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error: " + str(e))), 500
    

@app.route('/farmers/active', methods=['GET'])
@jwt_required()
@require_role(['super_user', 'admin', 'user'])
def get_active_farmers():
    """GET /farmers/active - Get farmers that have a farm i.e they are active take into account sowing date and due dates of the farm for being active"""
    try:
        farmers = FarmerServices.get_active_farmers()
        
        if farmers is None:
            farmers = []
        
        farmer_dicts = [farmer.to_dict(include_country=True) for farmer in farmers if farmer is not None]
        
        response = ResponseHelper.success_response(
            farmer_dicts,
            f"Found {len(farmer_dicts)} farmers that are active"
        )
        return jsonify(response), 200
        
    except ValueError as e:
        return jsonify(ResponseHelper.error_response(str(e))), 400
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error: " + str(e))), 500
    

@app.route('/farmers/<int:farmer_id>', methods=['GET'])
@jwt_required()
@require_role(['super_user', 'admin', 'user'])
def get_farmer_by_id(farmer_id):
    """GET /farmers/{farmer_id} - Get farmer details by id"""
    try:
        if farmer_id is None:
            return jsonify(ResponseHelper.error_response("Farmer id is required")), 400
        
        farmer = FarmerServices.get_farmers_by_id(farmer_id)
        
        if farmer is None:
            return jsonify(ResponseHelper.error_response("Failed to get farmer")), 500
        
        response = ResponseHelper.success_response(
            farmer.to_dict(include_country=True, include_farms=True),
            f"Found Farmer by id:{farmer_id} successfully",
            201
        )
        return jsonify(response), 201
        
    except ValueError as e:
        return jsonify(ResponseHelper.error_response(str(e))), 400
    except IntegrityError:
        return jsonify(ResponseHelper.error_response("Database error")), 409
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error: " + str(e))), 500