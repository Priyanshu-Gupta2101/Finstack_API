from helpers.response_helper import ResponseHelper
from flask import jsonify
from mappers import FarmMapper
from services import FarmServices

class FarmViews:
    """Views for farm endpoints"""
    
    def __init__(self):
        self.farm_service = FarmServices()
        self.farm_mapper = FarmMapper()
        self.helper = ResponseHelper()
    
    """POST /farms - Create new farm"""
    def create_farm(self,farm_data):
        try:
            farm = self.farm_service.create_farm(farm_data)
            
            response = self.helper.success_response(
                self.farm_mapper.to_dict(farm),
                "Farm created successfully",
                201
            )
            return jsonify(response), 201
            
        except ValueError as e:
            return jsonify(self.helper.error_response(str(e), 400)), 400
        except Exception as e:
            return jsonify(self.helper.error_response("Internal server error", 500)), 500