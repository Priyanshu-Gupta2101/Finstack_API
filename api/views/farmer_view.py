from helpers.response_helper import ResponseHelper
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from mappers import FarmerMapper
from services import FarmerServices

class FarmerViews:
    """Views for farmer endpoints"""
    
    def __init__(self):
        self.farmer_service = FarmerServices()
        self.farmer_mapper = FarmerMapper()
        self.helper = ResponseHelper()
    
    """POST /farmers - Create new farmer"""
    def create_farmer(self,farmer_data):
        try:
            farmer = self.farmer_service.create_farmer(farmer_data)
            
            response = self.helper.success_response(
                self.farmer_mapper.to_dict(farmer),
                "Farmer created successfully",
                201
            )
            return jsonify(response), 201
            
        except ValueError as e:
            return jsonify(self.helper.error_response(str(e), 400)), 400
        except IntegrityError:
            return jsonify(self.helper.error_response("Farmer already exists", 409)), 409
        except Exception as e:
            return jsonify(self.helper.error_response("Internal server error", 500)), 500
    

    """GET /farmers/by-crop?crop={crop_name} - Get farmers by crop"""
    def get_farmers_by_crop(self, crop_name):
        try:
            farmers = self.farmer_service.get_farmers_by_crop(crop_name)
            farmer_dicts = [self.farmer_mapper.to_dict(farmer) for farmer in farmers]
            
            response = self.helper.success_response(
                farmer_dicts,
                f"Found {len(farmers)} farmers growing {crop_name}"
            )
            return jsonify(response), 200
            
        except ValueError as e:
            return jsonify(self.helper.error_response(str(e), 400)), 400
        except Exception as e:
            return jsonify(self.helper.error_response("Internal server error", 500)), 500