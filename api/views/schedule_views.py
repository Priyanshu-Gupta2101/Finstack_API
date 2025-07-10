from helpers.response_helper import ResponseHelper
from flask import jsonify
from mappers import ScheduleMapper
from services import ScheduleServices

class ScheduleViews:
    """Views for schdules endpoints"""

    @staticmethod
    def create_schedule(schedule_data):
        """POST /schedules - Create new schedules"""
        try:
            schedule = ScheduleServices.create_schedule(schedule_data)
            
            response = ResponseHelper.success_response(
                schedule.to_dict(include_due_date=True, include_farm=True),
                "Schedule created successfully",
                201
            )
            return jsonify(response), 201
            
        except ValueError as e:
            return jsonify(ResponseHelper.error_response(str(e), 400)), 400
        except Exception as e:
            return jsonify(ResponseHelper.error_response("Internal server error", 500)), 500

    @staticmethod  
    def get_schedules_due_today():
        """GET /schedules/due-today - Get schedules due today"""
        try:
            schedules = ScheduleServices.get_schedules_due_today()
            schedule_dicts = [schedule.to_dict(include_due_date=True, include_farm=True) for schedule in schedules]
            
            response = ResponseHelper.success_response(
                schedule_dicts,
                f"Found {len(schedules)} schedules due today"
            )
            return jsonify(response), 200
            
        except Exception as e:
            return jsonify(ResponseHelper.error_response("Internal server error", 500)), 500
    
    @staticmethod
    def get_schedules_due_tomorrow():
        """GET /schedules/due-tomorrow - Get schedules due tomorrow"""
        try:
            schedules = ScheduleServices.get_schedules_due_tomorrow()
            schedule_dicts = [schedule.to_dict(include_due_date=True, include_farm=True) for schedule in schedules]
            
            response = ResponseHelper.success_response(
                schedule_dicts,
                f"Found {len(schedules)} schedules due tomorrow"
            )
            return jsonify(response), 200
            
        except Exception as e:
            return jsonify(ResponseHelper.error_response("Internal server error", 500)), 500
    
    @staticmethod
    def calculate_bill_view(farmer_id, fertilizer_prices):
        """POST /schedules/bill/<farmer_id> - Calculate Bill for farmer"""
        try:
            bill = ScheduleServices.calculate_bill(farmer_id, fertilizer_prices)
            
            response = ResponseHelper.success_response(
                bill,
                "Bill of materials calculated successfully"
            )
            return jsonify(response), 200
            
        except ValueError as e:
            return jsonify(ResponseHelper.error_response(str(e), 400)), 400
        except Exception as e:
            return jsonify(ResponseHelper.error_response("Internal server error", 500)), 500