from helpers.response_helper import ResponseHelper
from flask import jsonify
from mappers import ScheduleMapper
from services import ScheduleServices

class ScheduleViews:
    """Views for schdules endpoints"""
    
    def __init__(self):
        self.schedule_services = ScheduleServices()
        self.schedule_mapper = ScheduleMapper()
        self.helper = ResponseHelper()
    
    def create_schedule(self, schedule_data):
        """POST /schedules - Create new schedules"""
        try:
            schedule = self.schedule_services.create_schedule(schedule_data)
            
            response = self.helper.success_response(
                self.schedule_mapper.to_dict(schedule),
                "Schedule created successfully",
                201
            )
            return jsonify(response), 201
            
        except ValueError as e:
            return jsonify(self.helper.error_response(str(e), 400)), 400
        except Exception as e:
            return jsonify(self.helper.error_response("Internal server error", 500)), 500
        
    def get_schedules_due_today(self):
        """GET /schedules/due-today - Get schedules due today"""
        try:
            schedules = self.schedule_services.get_schedules_due_today()
            schedule_dicts = [self.schedule_mapper.to_dict(schedule) for schedule in schedules]
            
            response = self.helper.success_response(
                schedule_dicts,
                f"Found {len(schedules)} schedules due today"
            )
            return jsonify(response), 200
            
        except Exception as e:
            return jsonify(self.helper.error_response("Internal server error", 500)), 500
    
    def get_schedules_due_tomorrow(self):
        """GET /schedules/due-tomorrow - Get schedules due tomorrow"""
        try:
            schedules = self.schedule_services.get_schedules_due_tomorrow()
            schedule_dicts = [self.schedule_mapper.to_dict(schedule) for schedule in schedules]
            
            response = self.helper.success_response(
                schedule_dicts,
                f"Found {len(schedules)} schedules due tomorrow"
            )
            return jsonify(response), 200
            
        except Exception as e:
            return jsonify(self.helper.error_response("Internal server error", 500)), 500
        
    def calculate_bill_view(self, farmer_id, fertilizer_prices):
        """POST /schedules/bill/<farmer_id> - Calculate Bill for farmer"""
        try:
            bill = self.schedule_services.calculate_bill(farmer_id, fertilizer_prices)
            
            response = self.helper.success_response(
                bill,
                "Bill of materials calculated successfully"
            )
            return jsonify(response), 200
            
        except ValueError as e:
            return jsonify(self.helper.error_response(str(e), 400)), 400
        except Exception as e:
            return jsonify(self.helper.error_response("Internal server error", 500)), 500