from helpers.response_helper import ResponseHelper
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from services import FarmerServices

class FarmerViews:
    """Views for farmer endpoints"""
    
    @staticmethod
    def create_farmer(farmer_data):
        try:
            farmer = FarmerServices.create_farmer(farmer_data)
            
            response = ResponseHelper.success_response(
                farmer.to_dict(include_country=True),
                "Farmer created successfully",
                201
            )
            return jsonify(response), 201
            
        except ValueError as e:
            return jsonify(ResponseHelper.error_response(str(e), 400)), 400
        except IntegrityError:
            return jsonify(ResponseHelper.error_response("Farmer already exists", 409)), 409
        except Exception as e:
            return jsonify(ResponseHelper.error_response("Internal server error", 500)), 500
    

    @staticmethod
    def get_farmers_by_crop(crop_name):
        try:
            farmers = FarmerServices.get_farmers_by_crop(crop_name)
            farmer_dicts = [farmer.to_dict(include_country=True) for farmer in farmers]
            
            response = ResponseHelper.success_response(
                farmer_dicts,
                f"Found {len(farmers)} farmers growing {crop_name}"
            )
            return jsonify(response), 200
            
        except ValueError as e:
            return jsonify(ResponseHelper.error_response(str(e), 400)), 400
        except Exception as e:
            return jsonify(ResponseHelper.error_response("Internal server error", 500)), 500