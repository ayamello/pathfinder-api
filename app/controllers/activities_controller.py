from datetime import datetime, timezone
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required
from app.controllers import create, delete, update
from app.models.activities_model import ActivityModel
from app.exceptions.base_exceptions import NotStringError, WrongKeysError, NotFoundDataError
from sqlalchemy.exc import InvalidRequestError
from app.models.points_model import PointModel


@jwt_required()
def create_activity():
    try:
        data = request.get_json()
    
        validated_data = ActivityModel.validate(**data)

        new_activity = create(validated_data, ActivityModel, '')
        
        point_id = data['point_id']

        point = PointModel.query.get(point_id)

        point.activities.append(new_activity)
            
        current_app.db.session.commit()

        return jsonify(new_activity), 201

    except WrongKeysError as err:
        return jsonify({'error': err.message}), 400

    except NotStringError as err:
        return jsonify({'error': str(err)}), 400

    except NotFoundDataError as err:
        return jsonify({'error': str(err)}), 404


@jwt_required()
def activities_by_point(point_id: int):
    try:
        point = PointModel.query.get(point_id)

        return {'activities': point.activities}, 200

    except AttributeError:
        return {'error': 'Point ID Not Found'}, 404


@jwt_required()
def update_activity(id: int):
    try:
        data = request.get_json()

        data['updated_at'] = datetime.now(timezone.utc)
        
        activity = update(ActivityModel, data, id)

        return activity

    except WrongKeysError as err:
        return jsonify({'error': err.message}), 400

    except InvalidRequestError as err:
        return jsonify({'error': str(err)}), 400
    
    except NotFoundDataError as err:
        return jsonify({'error': str(err)}), 404



@jwt_required()
def delete_activity(id: int):
    try:
        activity = delete(ActivityModel, id)

        return activity
        
    except NotFoundDataError as err:
        return jsonify({'error': str(err)}), 404

