from helpers.response_helper import ResponseHelper
from flask import jsonify, request
from services import ScheduleServices
from database import app
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from middleware import require_role

"""Views for schedules endpoints"""

@app.route('/schedules', methods=['POST'])
@jwt_required()
@require_role(['super_user', 'admin'])
def create_schedule():
    """POST /schedules - Create new schedule"""
    try:
        if not request.json:
            return jsonify(ResponseHelper.error_response("JSON data required")), 400
        
        data = {
            'days_after_sowing': request.json.get('days_after_sowing'),
            'fertilizer': request.json.get('fertilizer'),
            'quantity': request.json.get('quantity'),
            'quantity_unit': request.json.get('quantity_unit'),
            'farm_id': request.json.get('farm_id'),
        }
        
        schedule = ScheduleServices.create_schedule(data)
        
        if schedule is None:
            return jsonify(ResponseHelper.error_response("Failed to create schedule")), 500
        
        response = ResponseHelper.success_response(
            schedule.to_dict(include_due_date=True, include_farm=True),
            "Schedule created successfully",
            201
        )
        return jsonify(response), 201
        
    except ValueError as e:
        return jsonify(ResponseHelper.error_response(str(e))), 400
    except IntegrityError:
        return jsonify(ResponseHelper.error_response("Database error")), 409
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error")), 500
    
@app.route('/schedules/<int:schedule_id>', methods=['GET'])
@jwt_required()
@require_role(['super_user', 'admin', 'user'])
def get_schedule_by_id(schedule_id):
    """GET /Schedules/{Schedule_id} - Get Schedule details by id"""
    try:
        if schedule_id is None:
            return jsonify(ResponseHelper.error_response("Schedule id is required")), 400
        
        schedule = ScheduleServices.get_schedule_by_id(schedule_id)
        
        if schedule is None:
            return jsonify(ResponseHelper.error_response("Failed to get Schedule")), 500
        
        response = ResponseHelper.success_response(
            schedule.to_dict(include_due_date=True, include_farm=True),
            f"Found Schedule by id:{schedule_id} successfully",
            201
        )
        return jsonify(response), 201
        
    except ValueError as e:
        return jsonify(ResponseHelper.error_response(str(e))), 400
    except IntegrityError:
        return jsonify(ResponseHelper.error_response("Database error")), 409
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error: " + str(e))), 500


@app.route('/schedules/today', methods=['GET'])
@jwt_required()
@require_role(['super_user', 'admin', 'user'])
def get_schedules_due_today():
    """GET /schedules/today - Get schedules due today"""
    try:
        schedules = ScheduleServices.get_schedules_due_today()
        
        if schedules is None:
            schedules = []
        
        schedule_dicts = [schedule.to_dict(include_due_date=True, include_farm=True) for schedule in schedules if schedule is not None]
        
        response = ResponseHelper.success_response(
            schedule_dicts,
            f"Found {len(schedule_dicts)} schedules due today"
        )
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error")), 500


@app.route('/schedules/tomorrow', methods=['GET'])
@jwt_required()
@require_role(['super_user', 'admin', 'user'])
def get_schedules_due_tomorrow():
    """GET /schedules/tomorrow - Get schedules due tomorrow"""
    try:
        schedules = ScheduleServices.get_schedules_due_tomorrow()
        
        if schedules is None:
            schedules = []
        
        schedule_dicts = [schedule.to_dict(include_due_date=True, include_farm=True) for schedule in schedules if schedule is not None]
        
        response = ResponseHelper.success_response(
            schedule_dicts,
            f"Found {len(schedule_dicts)} schedules due tomorrow"
        )
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error")), 500


@app.route('/schedules/bill/<int:farmer_id>', methods=['POST'])
@jwt_required()
@require_role(['super_user', 'admin'])
def calculate_bill_of_materials(farmer_id):
    """POST /schedules/bill/{farmer_id} - Calculate bill of materials"""
    try:
        if not request.json or 'fertilizer_prices' not in request.json:
            return jsonify(ResponseHelper.error_response("Fertilizer prices required")), 400
                
        fertilizer_prices = request.json['fertilizer_prices']
        
        bill = ScheduleServices.calculate_bill(farmer_id, fertilizer_prices)
        
        if bill is None:
            return jsonify(ResponseHelper.error_response("Failed to calculate bill")), 500
        
        response = ResponseHelper.success_response(
            bill,
            "Bill of materials calculated successfully"
        )
        return jsonify(response), 200
        
    except ValueError as e:
        return jsonify(ResponseHelper.error_response(str(e))), 400
    except Exception as e:
        return jsonify(ResponseHelper.error_response("Internal server error")), 500