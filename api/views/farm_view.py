from helpers.response_helper import ResponseHelper
from flask import jsonify
from services import FarmServices

class FarmViews:
    """Views for farm endpoints"""
    
    @staticmethod
    def create_farm(farm_data):
        """POST /farms - Create new farm"""
        try:
            farm = FarmServices.create_farm(farm_data)
            
            response = ResponseHelper.success_response(
                farm.to_dict(include_farmer=True),
                "Farm created successfully",
                201
            )
            return jsonify(response), 201
            
        except ValueError as e:
            return jsonify(ResponseHelper.error_response(str(e), 400)), 400
        except Exception as e:
            return jsonify(ResponseHelper.error_response("Internal server error", 500)), 500